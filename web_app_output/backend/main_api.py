import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "RegleLocation", "description": "Operations for RegleLocation entities"},
        {"name": "RegleLocation Relationships", "description": "Manage RegleLocation relationships"},
        {"name": "Contraintes", "description": "Operations for Contraintes entities"},
        {"name": "Contraintes Relationships", "description": "Manage Contraintes relationships"},
        {"name": "Indisponibilte", "description": "Operations for Indisponibilte entities"},
        {"name": "Indisponibilte Relationships", "description": "Manage Indisponibilte relationships"},
        {"name": "Tarif", "description": "Operations for Tarif entities"},
        {"name": "Tarif Relationships", "description": "Manage Tarif relationships"},
        {"name": "PersonneReferente", "description": "Operations for PersonneReferente entities"},
        {"name": "PersonneReferente Relationships", "description": "Manage PersonneReferente relationships"},
        {"name": "Prestation", "description": "Operations for Prestation entities"},
        {"name": "Prestation Relationships", "description": "Manage Prestation relationships"},
        {"name": "Materiel", "description": "Operations for Materiel entities"},
        {"name": "Materiel Relationships", "description": "Manage Materiel relationships"},
        {"name": "ElementCentre", "description": "Operations for ElementCentre entities"},
        {"name": "ElementCentre Relationships", "description": "Manage ElementCentre relationships"},
        {"name": "Evenement", "description": "Operations for Evenement entities"},
        {"name": "Evenement Relationships", "description": "Manage Evenement relationships"},
        {"name": "Paiement", "description": "Operations for Paiement entities"},
        {"name": "Paiement Relationships", "description": "Manage Paiement relationships"},
        {"name": "Paiement Methods", "description": "Execute Paiement methods"},
        {"name": "CentreDeCongres", "description": "Operations for CentreDeCongres entities"},
        {"name": "CentreDeCongres Relationships", "description": "Manage CentreDeCongres relationships"},
        {"name": "Reservation", "description": "Operations for Reservation entities"},
        {"name": "Reservation Relationships", "description": "Manage Reservation relationships"},
        {"name": "Reservation Methods", "description": "Execute Reservation methods"},
        {"name": "Gestionnaire", "description": "Operations for Gestionnaire entities"},
        {"name": "Gestionnaire Relationships", "description": "Manage Gestionnaire relationships"},
        {"name": "Gestionnaire Methods", "description": "Execute Gestionnaire methods"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["reglelocation_count"] = database.query(RegleLocation).count()
    stats["contraintes_count"] = database.query(Contraintes).count()
    stats["indisponibilte_count"] = database.query(Indisponibilte).count()
    stats["tarif_count"] = database.query(Tarif).count()
    stats["personnereferente_count"] = database.query(PersonneReferente).count()
    stats["prestation_count"] = database.query(Prestation).count()
    stats["materiel_count"] = database.query(Materiel).count()
    stats["elementcentre_count"] = database.query(ElementCentre).count()
    stats["evenement_count"] = database.query(Evenement).count()
    stats["paiement_count"] = database.query(Paiement).count()
    stats["centredecongres_count"] = database.query(CentreDeCongres).count()
    stats["reservation_count"] = database.query(Reservation).count()
    stats["gestionnaire_count"] = database.query(Gestionnaire).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   RegleLocation functions
#
############################################

@app.get("/reglelocation/", response_model=None, tags=["RegleLocation"])
def get_all_reglelocation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(RegleLocation)
        query = query.options(joinedload(RegleLocation.prestation_2))
        query = query.options(joinedload(RegleLocation.materiel_2))
        reglelocation_list = query.all()

        # Serialize with relationships included
        result = []
        for reglelocation_item in reglelocation_list:
            item_dict = reglelocation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if reglelocation_item.prestation_2:
                related_obj = reglelocation_item.prestation_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['prestation_2'] = related_dict
            else:
                item_dict['prestation_2'] = None
            if reglelocation_item.materiel_2:
                related_obj = reglelocation_item.materiel_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['materiel_2'] = related_dict
            else:
                item_dict['materiel_2'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(RegleLocation).all()


@app.get("/reglelocation/count/", response_model=None, tags=["RegleLocation"])
def get_count_reglelocation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of RegleLocation entities"""
    count = database.query(RegleLocation).count()
    return {"count": count}


@app.get("/reglelocation/paginated/", response_model=None, tags=["RegleLocation"])
def get_paginated_reglelocation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of RegleLocation entities"""
    total = database.query(RegleLocation).count()
    reglelocation_list = database.query(RegleLocation).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": reglelocation_list
    }


@app.get("/reglelocation/search/", response_model=None, tags=["RegleLocation"])
def search_reglelocation(
    database: Session = Depends(get_db)
) -> list:
    """Search RegleLocation entities by attributes"""
    query = database.query(RegleLocation)


    results = query.all()
    return results


@app.get("/reglelocation/{reglelocation_id}/", response_model=None, tags=["RegleLocation"])
async def get_reglelocation(reglelocation_id: int, database: Session = Depends(get_db)) -> RegleLocation:
    db_reglelocation = database.query(RegleLocation).filter(RegleLocation.id == reglelocation_id).first()
    if db_reglelocation is None:
        raise HTTPException(status_code=404, detail="RegleLocation not found")

    response_data = {
        "reglelocation": db_reglelocation,
}
    return response_data



@app.post("/reglelocation/", response_model=None, tags=["RegleLocation"])
async def create_reglelocation(reglelocation_data: RegleLocationCreate, database: Session = Depends(get_db)) -> RegleLocation:

    if reglelocation_data.prestation_2 is not None:
        db_prestation_2 = database.query(Prestation).filter(Prestation.id == reglelocation_data.prestation_2).first()
        if not db_prestation_2:
            raise HTTPException(status_code=400, detail="Prestation not found")
    else:
        raise HTTPException(status_code=400, detail="Prestation ID is required")
    if reglelocation_data.materiel_2 is not None:
        db_materiel_2 = database.query(Materiel).filter(Materiel.id == reglelocation_data.materiel_2).first()
        if not db_materiel_2:
            raise HTTPException(status_code=400, detail="Materiel not found")
    else:
        raise HTTPException(status_code=400, detail="Materiel ID is required")

    db_reglelocation = RegleLocation(
        dureeMinimale=reglelocation_data.dureeMinimale,        nbMinimum=reglelocation_data.nbMinimum,        prestation_2_id=reglelocation_data.prestation_2,        materiel_2_id=reglelocation_data.materiel_2        )

    database.add(db_reglelocation)
    database.commit()
    database.refresh(db_reglelocation)




    return db_reglelocation


@app.post("/reglelocation/bulk/", response_model=None, tags=["RegleLocation"])
async def bulk_create_reglelocation(items: list[RegleLocationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple RegleLocation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.prestation_2:
                raise ValueError("Prestation ID is required")
            if not item_data.materiel_2:
                raise ValueError("Materiel ID is required")

            db_reglelocation = RegleLocation(
                dureeMinimale=item_data.dureeMinimale,                nbMinimum=item_data.nbMinimum,                prestation_2_id=item_data.prestation_2,                materiel_2_id=item_data.materiel_2            )
            database.add(db_reglelocation)
            database.flush()  # Get ID without committing
            created_items.append(db_reglelocation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} RegleLocation entities"
    }


@app.delete("/reglelocation/bulk/", response_model=None, tags=["RegleLocation"])
async def bulk_delete_reglelocation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple RegleLocation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reglelocation = database.query(RegleLocation).filter(RegleLocation.id == item_id).first()
        if db_reglelocation:
            database.delete(db_reglelocation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} RegleLocation entities"
    }

@app.put("/reglelocation/{reglelocation_id}/", response_model=None, tags=["RegleLocation"])
async def update_reglelocation(reglelocation_id: int, reglelocation_data: RegleLocationCreate, database: Session = Depends(get_db)) -> RegleLocation:
    db_reglelocation = database.query(RegleLocation).filter(RegleLocation.id == reglelocation_id).first()
    if db_reglelocation is None:
        raise HTTPException(status_code=404, detail="RegleLocation not found")

    setattr(db_reglelocation, 'dureeMinimale', reglelocation_data.dureeMinimale)
    setattr(db_reglelocation, 'nbMinimum', reglelocation_data.nbMinimum)
    if reglelocation_data.prestation_2 is not None:
        db_prestation_2 = database.query(Prestation).filter(Prestation.id == reglelocation_data.prestation_2).first()
        if not db_prestation_2:
            raise HTTPException(status_code=400, detail="Prestation not found")
        setattr(db_reglelocation, 'prestation_2_id', reglelocation_data.prestation_2)
    if reglelocation_data.materiel_2 is not None:
        db_materiel_2 = database.query(Materiel).filter(Materiel.id == reglelocation_data.materiel_2).first()
        if not db_materiel_2:
            raise HTTPException(status_code=400, detail="Materiel not found")
        setattr(db_reglelocation, 'materiel_2_id', reglelocation_data.materiel_2)
    database.commit()
    database.refresh(db_reglelocation)

    return db_reglelocation


@app.delete("/reglelocation/{reglelocation_id}/", response_model=None, tags=["RegleLocation"])
async def delete_reglelocation(reglelocation_id: int, database: Session = Depends(get_db)):
    db_reglelocation = database.query(RegleLocation).filter(RegleLocation.id == reglelocation_id).first()
    if db_reglelocation is None:
        raise HTTPException(status_code=404, detail="RegleLocation not found")
    database.delete(db_reglelocation)
    database.commit()
    return db_reglelocation





############################################
#
#   Contraintes functions
#
############################################

@app.get("/contraintes/", response_model=None, tags=["Contraintes"])
def get_all_contraintes(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Contraintes)
        query = query.options(joinedload(Contraintes.elementcentre_3))
        contraintes_list = query.all()

        # Serialize with relationships included
        result = []
        for contraintes_item in contraintes_list:
            item_dict = contraintes_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if contraintes_item.elementcentre_3:
                related_obj = contraintes_item.elementcentre_3
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre_3'] = related_dict
            else:
                item_dict['elementcentre_3'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Contraintes).all()


@app.get("/contraintes/count/", response_model=None, tags=["Contraintes"])
def get_count_contraintes(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Contraintes entities"""
    count = database.query(Contraintes).count()
    return {"count": count}


@app.get("/contraintes/paginated/", response_model=None, tags=["Contraintes"])
def get_paginated_contraintes(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Contraintes entities"""
    total = database.query(Contraintes).count()
    contraintes_list = database.query(Contraintes).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": contraintes_list
    }


@app.get("/contraintes/search/", response_model=None, tags=["Contraintes"])
def search_contraintes(
    database: Session = Depends(get_db)
) -> list:
    """Search Contraintes entities by attributes"""
    query = database.query(Contraintes)


    results = query.all()
    return results


@app.get("/contraintes/{contraintes_id}/", response_model=None, tags=["Contraintes"])
async def get_contraintes(contraintes_id: int, database: Session = Depends(get_db)) -> Contraintes:
    db_contraintes = database.query(Contraintes).filter(Contraintes.id == contraintes_id).first()
    if db_contraintes is None:
        raise HTTPException(status_code=404, detail="Contraintes not found")

    response_data = {
        "contraintes": db_contraintes,
}
    return response_data



@app.post("/contraintes/", response_model=None, tags=["Contraintes"])
async def create_contraintes(contraintes_data: ContraintesCreate, database: Session = Depends(get_db)) -> Contraintes:

    if contraintes_data.elementcentre_3 is not None:
        db_elementcentre_3 = database.query(ElementCentre).filter(ElementCentre.id == contraintes_data.elementcentre_3).first()
        if not db_elementcentre_3:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
    else:
        raise HTTPException(status_code=400, detail="ElementCentre ID is required")

    db_contraintes = Contraintes(
        joursInterdits=contraintes_data.joursInterdits.value,        dureeMinimale=contraintes_data.dureeMinimale,        elementcentre_3_id=contraintes_data.elementcentre_3        )

    database.add(db_contraintes)
    database.commit()
    database.refresh(db_contraintes)




    return db_contraintes


@app.post("/contraintes/bulk/", response_model=None, tags=["Contraintes"])
async def bulk_create_contraintes(items: list[ContraintesCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Contraintes entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.elementcentre_3:
                raise ValueError("ElementCentre ID is required")

            db_contraintes = Contraintes(
                joursInterdits=item_data.joursInterdits.value,                dureeMinimale=item_data.dureeMinimale,                elementcentre_3_id=item_data.elementcentre_3            )
            database.add(db_contraintes)
            database.flush()  # Get ID without committing
            created_items.append(db_contraintes.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Contraintes entities"
    }


@app.delete("/contraintes/bulk/", response_model=None, tags=["Contraintes"])
async def bulk_delete_contraintes(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Contraintes entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_contraintes = database.query(Contraintes).filter(Contraintes.id == item_id).first()
        if db_contraintes:
            database.delete(db_contraintes)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Contraintes entities"
    }

@app.put("/contraintes/{contraintes_id}/", response_model=None, tags=["Contraintes"])
async def update_contraintes(contraintes_id: int, contraintes_data: ContraintesCreate, database: Session = Depends(get_db)) -> Contraintes:
    db_contraintes = database.query(Contraintes).filter(Contraintes.id == contraintes_id).first()
    if db_contraintes is None:
        raise HTTPException(status_code=404, detail="Contraintes not found")

    setattr(db_contraintes, 'joursInterdits', contraintes_data.joursInterdits.value)
    setattr(db_contraintes, 'dureeMinimale', contraintes_data.dureeMinimale)
    if contraintes_data.elementcentre_3 is not None:
        db_elementcentre_3 = database.query(ElementCentre).filter(ElementCentre.id == contraintes_data.elementcentre_3).first()
        if not db_elementcentre_3:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
        setattr(db_contraintes, 'elementcentre_3_id', contraintes_data.elementcentre_3)
    database.commit()
    database.refresh(db_contraintes)

    return db_contraintes


@app.delete("/contraintes/{contraintes_id}/", response_model=None, tags=["Contraintes"])
async def delete_contraintes(contraintes_id: int, database: Session = Depends(get_db)):
    db_contraintes = database.query(Contraintes).filter(Contraintes.id == contraintes_id).first()
    if db_contraintes is None:
        raise HTTPException(status_code=404, detail="Contraintes not found")
    database.delete(db_contraintes)
    database.commit()
    return db_contraintes





############################################
#
#   Indisponibilte functions
#
############################################

@app.get("/indisponibilte/", response_model=None, tags=["Indisponibilte"])
def get_all_indisponibilte(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Indisponibilte)
        query = query.options(joinedload(Indisponibilte.elementcentre_4))
        indisponibilte_list = query.all()

        # Serialize with relationships included
        result = []
        for indisponibilte_item in indisponibilte_list:
            item_dict = indisponibilte_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if indisponibilte_item.elementcentre_4:
                related_obj = indisponibilte_item.elementcentre_4
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre_4'] = related_dict
            else:
                item_dict['elementcentre_4'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Indisponibilte).all()


@app.get("/indisponibilte/count/", response_model=None, tags=["Indisponibilte"])
def get_count_indisponibilte(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Indisponibilte entities"""
    count = database.query(Indisponibilte).count()
    return {"count": count}


@app.get("/indisponibilte/paginated/", response_model=None, tags=["Indisponibilte"])
def get_paginated_indisponibilte(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Indisponibilte entities"""
    total = database.query(Indisponibilte).count()
    indisponibilte_list = database.query(Indisponibilte).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": indisponibilte_list
    }


@app.get("/indisponibilte/search/", response_model=None, tags=["Indisponibilte"])
def search_indisponibilte(
    database: Session = Depends(get_db)
) -> list:
    """Search Indisponibilte entities by attributes"""
    query = database.query(Indisponibilte)


    results = query.all()
    return results


@app.get("/indisponibilte/{indisponibilte_id}/", response_model=None, tags=["Indisponibilte"])
async def get_indisponibilte(indisponibilte_id: int, database: Session = Depends(get_db)) -> Indisponibilte:
    db_indisponibilte = database.query(Indisponibilte).filter(Indisponibilte.id == indisponibilte_id).first()
    if db_indisponibilte is None:
        raise HTTPException(status_code=404, detail="Indisponibilte not found")

    response_data = {
        "indisponibilte": db_indisponibilte,
}
    return response_data



@app.post("/indisponibilte/", response_model=None, tags=["Indisponibilte"])
async def create_indisponibilte(indisponibilte_data: IndisponibilteCreate, database: Session = Depends(get_db)) -> Indisponibilte:

    if indisponibilte_data.elementcentre_4 is not None:
        db_elementcentre_4 = database.query(ElementCentre).filter(ElementCentre.id == indisponibilte_data.elementcentre_4).first()
        if not db_elementcentre_4:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
    else:
        raise HTTPException(status_code=400, detail="ElementCentre ID is required")

    db_indisponibilte = Indisponibilte(
        dateFin=indisponibilte_data.dateFin,        dateDebut=indisponibilte_data.dateDebut,        motif=indisponibilte_data.motif,        elementcentre_4_id=indisponibilte_data.elementcentre_4        )

    database.add(db_indisponibilte)
    database.commit()
    database.refresh(db_indisponibilte)




    return db_indisponibilte


@app.post("/indisponibilte/bulk/", response_model=None, tags=["Indisponibilte"])
async def bulk_create_indisponibilte(items: list[IndisponibilteCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Indisponibilte entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.elementcentre_4:
                raise ValueError("ElementCentre ID is required")

            db_indisponibilte = Indisponibilte(
                dateFin=item_data.dateFin,                dateDebut=item_data.dateDebut,                motif=item_data.motif,                elementcentre_4_id=item_data.elementcentre_4            )
            database.add(db_indisponibilte)
            database.flush()  # Get ID without committing
            created_items.append(db_indisponibilte.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Indisponibilte entities"
    }


@app.delete("/indisponibilte/bulk/", response_model=None, tags=["Indisponibilte"])
async def bulk_delete_indisponibilte(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Indisponibilte entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_indisponibilte = database.query(Indisponibilte).filter(Indisponibilte.id == item_id).first()
        if db_indisponibilte:
            database.delete(db_indisponibilte)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Indisponibilte entities"
    }

@app.put("/indisponibilte/{indisponibilte_id}/", response_model=None, tags=["Indisponibilte"])
async def update_indisponibilte(indisponibilte_id: int, indisponibilte_data: IndisponibilteCreate, database: Session = Depends(get_db)) -> Indisponibilte:
    db_indisponibilte = database.query(Indisponibilte).filter(Indisponibilte.id == indisponibilte_id).first()
    if db_indisponibilte is None:
        raise HTTPException(status_code=404, detail="Indisponibilte not found")

    setattr(db_indisponibilte, 'dateFin', indisponibilte_data.dateFin)
    setattr(db_indisponibilte, 'dateDebut', indisponibilte_data.dateDebut)
    setattr(db_indisponibilte, 'motif', indisponibilte_data.motif)
    if indisponibilte_data.elementcentre_4 is not None:
        db_elementcentre_4 = database.query(ElementCentre).filter(ElementCentre.id == indisponibilte_data.elementcentre_4).first()
        if not db_elementcentre_4:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
        setattr(db_indisponibilte, 'elementcentre_4_id', indisponibilte_data.elementcentre_4)
    database.commit()
    database.refresh(db_indisponibilte)

    return db_indisponibilte


@app.delete("/indisponibilte/{indisponibilte_id}/", response_model=None, tags=["Indisponibilte"])
async def delete_indisponibilte(indisponibilte_id: int, database: Session = Depends(get_db)):
    db_indisponibilte = database.query(Indisponibilte).filter(Indisponibilte.id == indisponibilte_id).first()
    if db_indisponibilte is None:
        raise HTTPException(status_code=404, detail="Indisponibilte not found")
    database.delete(db_indisponibilte)
    database.commit()
    return db_indisponibilte





############################################
#
#   Tarif functions
#
############################################

@app.get("/tarif/", response_model=None, tags=["Tarif"])
def get_all_tarif(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Tarif)
        query = query.options(joinedload(Tarif.elementcentre_2))
        tarif_list = query.all()

        # Serialize with relationships included
        result = []
        for tarif_item in tarif_list:
            item_dict = tarif_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if tarif_item.elementcentre_2:
                related_obj = tarif_item.elementcentre_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre_2'] = related_dict
            else:
                item_dict['elementcentre_2'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Tarif).all()


@app.get("/tarif/count/", response_model=None, tags=["Tarif"])
def get_count_tarif(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Tarif entities"""
    count = database.query(Tarif).count()
    return {"count": count}


@app.get("/tarif/paginated/", response_model=None, tags=["Tarif"])
def get_paginated_tarif(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Tarif entities"""
    total = database.query(Tarif).count()
    tarif_list = database.query(Tarif).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": tarif_list
    }


@app.get("/tarif/search/", response_model=None, tags=["Tarif"])
def search_tarif(
    database: Session = Depends(get_db)
) -> list:
    """Search Tarif entities by attributes"""
    query = database.query(Tarif)


    results = query.all()
    return results


@app.get("/tarif/{tarif_id}/", response_model=None, tags=["Tarif"])
async def get_tarif(tarif_id: int, database: Session = Depends(get_db)) -> Tarif:
    db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
    if db_tarif is None:
        raise HTTPException(status_code=404, detail="Tarif not found")

    response_data = {
        "tarif": db_tarif,
}
    return response_data



@app.post("/tarif/", response_model=None, tags=["Tarif"])
async def create_tarif(tarif_data: TarifCreate, database: Session = Depends(get_db)) -> Tarif:

    if tarif_data.elementcentre_2 is not None:
        db_elementcentre_2 = database.query(ElementCentre).filter(ElementCentre.id == tarif_data.elementcentre_2).first()
        if not db_elementcentre_2:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
    else:
        raise HTTPException(status_code=400, detail="ElementCentre ID is required")

    db_tarif = Tarif(
        saison=tarif_data.saison.value,        prixParJour=tarif_data.prixParJour,        elementcentre_2_id=tarif_data.elementcentre_2        )

    database.add(db_tarif)
    database.commit()
    database.refresh(db_tarif)




    return db_tarif


@app.post("/tarif/bulk/", response_model=None, tags=["Tarif"])
async def bulk_create_tarif(items: list[TarifCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Tarif entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.elementcentre_2:
                raise ValueError("ElementCentre ID is required")

            db_tarif = Tarif(
                saison=item_data.saison.value,                prixParJour=item_data.prixParJour,                elementcentre_2_id=item_data.elementcentre_2            )
            database.add(db_tarif)
            database.flush()  # Get ID without committing
            created_items.append(db_tarif.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Tarif entities"
    }


@app.delete("/tarif/bulk/", response_model=None, tags=["Tarif"])
async def bulk_delete_tarif(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Tarif entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_tarif = database.query(Tarif).filter(Tarif.id == item_id).first()
        if db_tarif:
            database.delete(db_tarif)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Tarif entities"
    }

@app.put("/tarif/{tarif_id}/", response_model=None, tags=["Tarif"])
async def update_tarif(tarif_id: int, tarif_data: TarifCreate, database: Session = Depends(get_db)) -> Tarif:
    db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
    if db_tarif is None:
        raise HTTPException(status_code=404, detail="Tarif not found")

    setattr(db_tarif, 'saison', tarif_data.saison.value)
    setattr(db_tarif, 'prixParJour', tarif_data.prixParJour)
    if tarif_data.elementcentre_2 is not None:
        db_elementcentre_2 = database.query(ElementCentre).filter(ElementCentre.id == tarif_data.elementcentre_2).first()
        if not db_elementcentre_2:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
        setattr(db_tarif, 'elementcentre_2_id', tarif_data.elementcentre_2)
    database.commit()
    database.refresh(db_tarif)

    return db_tarif


@app.delete("/tarif/{tarif_id}/", response_model=None, tags=["Tarif"])
async def delete_tarif(tarif_id: int, database: Session = Depends(get_db)):
    db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
    if db_tarif is None:
        raise HTTPException(status_code=404, detail="Tarif not found")
    database.delete(db_tarif)
    database.commit()
    return db_tarif





############################################
#
#   PersonneReferente functions
#
############################################

@app.get("/personnereferente/", response_model=None, tags=["PersonneReferente"])
def get_all_personnereferente(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    return database.query(PersonneReferente).all()


@app.get("/personnereferente/count/", response_model=None, tags=["PersonneReferente"])
def get_count_personnereferente(database: Session = Depends(get_db)) -> dict:
    """Get the total count of PersonneReferente entities"""
    count = database.query(PersonneReferente).count()
    return {"count": count}


@app.get("/personnereferente/paginated/", response_model=None, tags=["PersonneReferente"])
def get_paginated_personnereferente(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of PersonneReferente entities"""
    total = database.query(PersonneReferente).count()
    personnereferente_list = database.query(PersonneReferente).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": personnereferente_list
    }


@app.get("/personnereferente/search/", response_model=None, tags=["PersonneReferente"])
def search_personnereferente(
    database: Session = Depends(get_db)
) -> list:
    """Search PersonneReferente entities by attributes"""
    query = database.query(PersonneReferente)


    results = query.all()
    return results


@app.get("/personnereferente/{personnereferente_id}/", response_model=None, tags=["PersonneReferente"])
async def get_personnereferente(personnereferente_id: int, database: Session = Depends(get_db)) -> PersonneReferente:
    db_personnereferente = database.query(PersonneReferente).filter(PersonneReferente.id == personnereferente_id).first()
    if db_personnereferente is None:
        raise HTTPException(status_code=404, detail="PersonneReferente not found")

    response_data = {
        "personnereferente": db_personnereferente,
}
    return response_data



@app.post("/personnereferente/", response_model=None, tags=["PersonneReferente"])
async def create_personnereferente(personnereferente_data: PersonneReferenteCreate, database: Session = Depends(get_db)) -> PersonneReferente:


    db_personnereferente = PersonneReferente(
        nom=personnereferente_data.nom,        prenom=personnereferente_data.prenom,        mail=personnereferente_data.mail        )

    database.add(db_personnereferente)
    database.commit()
    database.refresh(db_personnereferente)




    return db_personnereferente


@app.post("/personnereferente/bulk/", response_model=None, tags=["PersonneReferente"])
async def bulk_create_personnereferente(items: list[PersonneReferenteCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple PersonneReferente entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_personnereferente = PersonneReferente(
                nom=item_data.nom,                prenom=item_data.prenom,                mail=item_data.mail            )
            database.add(db_personnereferente)
            database.flush()  # Get ID without committing
            created_items.append(db_personnereferente.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} PersonneReferente entities"
    }


@app.delete("/personnereferente/bulk/", response_model=None, tags=["PersonneReferente"])
async def bulk_delete_personnereferente(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple PersonneReferente entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_personnereferente = database.query(PersonneReferente).filter(PersonneReferente.id == item_id).first()
        if db_personnereferente:
            database.delete(db_personnereferente)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} PersonneReferente entities"
    }

@app.put("/personnereferente/{personnereferente_id}/", response_model=None, tags=["PersonneReferente"])
async def update_personnereferente(personnereferente_id: int, personnereferente_data: PersonneReferenteCreate, database: Session = Depends(get_db)) -> PersonneReferente:
    db_personnereferente = database.query(PersonneReferente).filter(PersonneReferente.id == personnereferente_id).first()
    if db_personnereferente is None:
        raise HTTPException(status_code=404, detail="PersonneReferente not found")

    setattr(db_personnereferente, 'nom', personnereferente_data.nom)
    setattr(db_personnereferente, 'prenom', personnereferente_data.prenom)
    setattr(db_personnereferente, 'mail', personnereferente_data.mail)
    database.commit()
    database.refresh(db_personnereferente)

    return db_personnereferente


@app.delete("/personnereferente/{personnereferente_id}/", response_model=None, tags=["PersonneReferente"])
async def delete_personnereferente(personnereferente_id: int, database: Session = Depends(get_db)):
    db_personnereferente = database.query(PersonneReferente).filter(PersonneReferente.id == personnereferente_id).first()
    if db_personnereferente is None:
        raise HTTPException(status_code=404, detail="PersonneReferente not found")
    database.delete(db_personnereferente)
    database.commit()
    return db_personnereferente





############################################
#
#   Prestation functions
#
############################################

@app.get("/prestation/", response_model=None, tags=["Prestation"])
def get_all_prestation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Prestation)
        query = query.options(joinedload(Prestation.reglelocation_1))
        query = query.options(joinedload(Prestation.centredecongres_3))
        prestation_list = query.all()

        # Serialize with relationships included
        result = []
        for prestation_item in prestation_list:
            item_dict = prestation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if prestation_item.reglelocation_1:
                related_obj = prestation_item.reglelocation_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reglelocation_1'] = related_dict
            else:
                item_dict['reglelocation_1'] = None
            if prestation_item.centredecongres_3:
                related_obj = prestation_item.centredecongres_3
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['centredecongres_3'] = related_dict
            else:
                item_dict['centredecongres_3'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Prestation).all()


@app.get("/prestation/count/", response_model=None, tags=["Prestation"])
def get_count_prestation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Prestation entities"""
    count = database.query(Prestation).count()
    return {"count": count}


@app.get("/prestation/paginated/", response_model=None, tags=["Prestation"])
def get_paginated_prestation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Prestation entities"""
    total = database.query(Prestation).count()
    prestation_list = database.query(Prestation).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": prestation_list
    }


@app.get("/prestation/search/", response_model=None, tags=["Prestation"])
def search_prestation(
    database: Session = Depends(get_db)
) -> list:
    """Search Prestation entities by attributes"""
    query = database.query(Prestation)


    results = query.all()
    return results


@app.get("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def get_prestation(prestation_id: int, database: Session = Depends(get_db)) -> Prestation:
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")

    response_data = {
        "prestation": db_prestation,
}
    return response_data



@app.post("/prestation/", response_model=None, tags=["Prestation"])
async def create_prestation(prestation_data: PrestationCreate, database: Session = Depends(get_db)) -> Prestation:

    if prestation_data.centredecongres_3 is not None:
        db_centredecongres_3 = database.query(CentreDeCongres).filter(CentreDeCongres.id == prestation_data.centredecongres_3).first()
        if not db_centredecongres_3:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
    else:
        raise HTTPException(status_code=400, detail="CentreDeCongres ID is required")

    db_prestation = Prestation(
        nom=prestation_data.nom,        estGlobale=prestation_data.estGlobale,        nbMaxParticipant=prestation_data.nbMaxParticipant,        description=prestation_data.description,        centredecongres_3_id=prestation_data.centredecongres_3        )

    database.add(db_prestation)
    database.commit()
    database.refresh(db_prestation)




    return db_prestation


@app.post("/prestation/bulk/", response_model=None, tags=["Prestation"])
async def bulk_create_prestation(items: list[PrestationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Prestation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.centredecongres_3:
                raise ValueError("CentreDeCongres ID is required")

            db_prestation = Prestation(
                nom=item_data.nom,                estGlobale=item_data.estGlobale,                nbMaxParticipant=item_data.nbMaxParticipant,                description=item_data.description,                centredecongres_3_id=item_data.centredecongres_3            )
            database.add(db_prestation)
            database.flush()  # Get ID without committing
            created_items.append(db_prestation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Prestation entities"
    }


@app.delete("/prestation/bulk/", response_model=None, tags=["Prestation"])
async def bulk_delete_prestation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Prestation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_prestation = database.query(Prestation).filter(Prestation.id == item_id).first()
        if db_prestation:
            database.delete(db_prestation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Prestation entities"
    }

@app.put("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def update_prestation(prestation_id: int, prestation_data: PrestationCreate, database: Session = Depends(get_db)) -> Prestation:
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")

    setattr(db_prestation, 'nom', prestation_data.nom)
    setattr(db_prestation, 'estGlobale', prestation_data.estGlobale)
    setattr(db_prestation, 'nbMaxParticipant', prestation_data.nbMaxParticipant)
    setattr(db_prestation, 'description', prestation_data.description)
    if prestation_data.centredecongres_3 is not None:
        db_centredecongres_3 = database.query(CentreDeCongres).filter(CentreDeCongres.id == prestation_data.centredecongres_3).first()
        if not db_centredecongres_3:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
        setattr(db_prestation, 'centredecongres_3_id', prestation_data.centredecongres_3)
    database.commit()
    database.refresh(db_prestation)

    return db_prestation


@app.delete("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def delete_prestation(prestation_id: int, database: Session = Depends(get_db)):
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")
    database.delete(db_prestation)
    database.commit()
    return db_prestation





############################################
#
#   Materiel functions
#
############################################

@app.get("/materiel/", response_model=None, tags=["Materiel"])
def get_all_materiel(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Materiel)
        query = query.options(joinedload(Materiel.centredecongres_2))
        query = query.options(joinedload(Materiel.reglelocation))
        materiel_list = query.all()

        # Serialize with relationships included
        result = []
        for materiel_item in materiel_list:
            item_dict = materiel_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if materiel_item.centredecongres_2:
                related_obj = materiel_item.centredecongres_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['centredecongres_2'] = related_dict
            else:
                item_dict['centredecongres_2'] = None
            if materiel_item.reglelocation:
                related_obj = materiel_item.reglelocation
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reglelocation'] = related_dict
            else:
                item_dict['reglelocation'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Materiel).all()


@app.get("/materiel/count/", response_model=None, tags=["Materiel"])
def get_count_materiel(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Materiel entities"""
    count = database.query(Materiel).count()
    return {"count": count}


@app.get("/materiel/paginated/", response_model=None, tags=["Materiel"])
def get_paginated_materiel(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Materiel entities"""
    total = database.query(Materiel).count()
    materiel_list = database.query(Materiel).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": materiel_list
    }


@app.get("/materiel/search/", response_model=None, tags=["Materiel"])
def search_materiel(
    database: Session = Depends(get_db)
) -> list:
    """Search Materiel entities by attributes"""
    query = database.query(Materiel)


    results = query.all()
    return results


@app.get("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def get_materiel(materiel_id: int, database: Session = Depends(get_db)) -> Materiel:
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")

    response_data = {
        "materiel": db_materiel,
}
    return response_data



@app.post("/materiel/", response_model=None, tags=["Materiel"])
async def create_materiel(materiel_data: MaterielCreate, database: Session = Depends(get_db)) -> Materiel:

    if materiel_data.centredecongres_2 is not None:
        db_centredecongres_2 = database.query(CentreDeCongres).filter(CentreDeCongres.id == materiel_data.centredecongres_2).first()
        if not db_centredecongres_2:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
    else:
        raise HTTPException(status_code=400, detail="CentreDeCongres ID is required")

    db_materiel = Materiel(
        nom=materiel_data.nom,        quantiteDisponible=materiel_data.quantiteDisponible,        description=materiel_data.description,        centredecongres_2_id=materiel_data.centredecongres_2        )

    database.add(db_materiel)
    database.commit()
    database.refresh(db_materiel)




    return db_materiel


@app.post("/materiel/bulk/", response_model=None, tags=["Materiel"])
async def bulk_create_materiel(items: list[MaterielCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Materiel entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.centredecongres_2:
                raise ValueError("CentreDeCongres ID is required")

            db_materiel = Materiel(
                nom=item_data.nom,                quantiteDisponible=item_data.quantiteDisponible,                description=item_data.description,                centredecongres_2_id=item_data.centredecongres_2            )
            database.add(db_materiel)
            database.flush()  # Get ID without committing
            created_items.append(db_materiel.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Materiel entities"
    }


@app.delete("/materiel/bulk/", response_model=None, tags=["Materiel"])
async def bulk_delete_materiel(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Materiel entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_materiel = database.query(Materiel).filter(Materiel.id == item_id).first()
        if db_materiel:
            database.delete(db_materiel)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Materiel entities"
    }

@app.put("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def update_materiel(materiel_id: int, materiel_data: MaterielCreate, database: Session = Depends(get_db)) -> Materiel:
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")

    setattr(db_materiel, 'nom', materiel_data.nom)
    setattr(db_materiel, 'quantiteDisponible', materiel_data.quantiteDisponible)
    setattr(db_materiel, 'description', materiel_data.description)
    if materiel_data.centredecongres_2 is not None:
        db_centredecongres_2 = database.query(CentreDeCongres).filter(CentreDeCongres.id == materiel_data.centredecongres_2).first()
        if not db_centredecongres_2:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
        setattr(db_materiel, 'centredecongres_2_id', materiel_data.centredecongres_2)
    database.commit()
    database.refresh(db_materiel)

    return db_materiel


@app.delete("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def delete_materiel(materiel_id: int, database: Session = Depends(get_db)):
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")
    database.delete(db_materiel)
    database.commit()
    return db_materiel





############################################
#
#   ElementCentre functions
#
############################################

@app.get("/elementcentre/", response_model=None, tags=["ElementCentre"])
def get_all_elementcentre(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ElementCentre)
        query = query.options(joinedload(ElementCentre.centredecongres_1))
        query = query.options(joinedload(ElementCentre.contraintes))
        elementcentre_list = query.all()

        # Serialize with relationships included
        result = []
        for elementcentre_item in elementcentre_list:
            item_dict = elementcentre_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if elementcentre_item.centredecongres_1:
                related_obj = elementcentre_item.centredecongres_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['centredecongres_1'] = related_dict
            else:
                item_dict['centredecongres_1'] = None
            if elementcentre_item.contraintes:
                related_obj = elementcentre_item.contraintes
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['contraintes'] = related_dict
            else:
                item_dict['contraintes'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            indisponibilte_list = database.query(Indisponibilte).filter(Indisponibilte.elementcentre_4_id == elementcentre_item.id).all()
            item_dict['indisponibilte'] = []
            for indisponibilte_obj in indisponibilte_list:
                indisponibilte_dict = indisponibilte_obj.__dict__.copy()
                indisponibilte_dict.pop('_sa_instance_state', None)
                item_dict['indisponibilte'].append(indisponibilte_dict)
            tarif_list = database.query(Tarif).filter(Tarif.elementcentre_2_id == elementcentre_item.id).all()
            item_dict['tarif_1'] = []
            for tarif_obj in tarif_list:
                tarif_dict = tarif_obj.__dict__.copy()
                tarif_dict.pop('_sa_instance_state', None)
                item_dict['tarif_1'].append(tarif_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ElementCentre).all()


@app.get("/elementcentre/count/", response_model=None, tags=["ElementCentre"])
def get_count_elementcentre(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ElementCentre entities"""
    count = database.query(ElementCentre).count()
    return {"count": count}


@app.get("/elementcentre/paginated/", response_model=None, tags=["ElementCentre"])
def get_paginated_elementcentre(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ElementCentre entities"""
    total = database.query(ElementCentre).count()
    elementcentre_list = database.query(ElementCentre).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": elementcentre_list
        }

    result = []
    for elementcentre_item in elementcentre_list:
        indisponibilte_ids = database.query(Indisponibilte.id).filter(Indisponibilte.elementcentre_4_id == elementcentre_item.id).all()
        tarif_1_ids = database.query(Tarif.id).filter(Tarif.elementcentre_2_id == elementcentre_item.id).all()
        item_data = {
            "elementcentre": elementcentre_item,
            "indisponibilte_ids": [x[0] for x in indisponibilte_ids],            "tarif_1_ids": [x[0] for x in tarif_1_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/elementcentre/search/", response_model=None, tags=["ElementCentre"])
def search_elementcentre(
    database: Session = Depends(get_db)
) -> list:
    """Search ElementCentre entities by attributes"""
    query = database.query(ElementCentre)


    results = query.all()
    return results


@app.get("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def get_elementcentre(elementcentre_id: int, database: Session = Depends(get_db)) -> ElementCentre:
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    indisponibilte_ids = database.query(Indisponibilte.id).filter(Indisponibilte.elementcentre_4_id == db_elementcentre.id).all()
    tarif_1_ids = database.query(Tarif.id).filter(Tarif.elementcentre_2_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "indisponibilte_ids": [x[0] for x in indisponibilte_ids],        "tarif_1_ids": [x[0] for x in tarif_1_ids]}
    return response_data



@app.post("/elementcentre/", response_model=None, tags=["ElementCentre"])
async def create_elementcentre(elementcentre_data: ElementCentreCreate, database: Session = Depends(get_db)) -> ElementCentre:

    if elementcentre_data.centredecongres_1 is not None:
        db_centredecongres_1 = database.query(CentreDeCongres).filter(CentreDeCongres.id == elementcentre_data.centredecongres_1).first()
        if not db_centredecongres_1:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
    else:
        raise HTTPException(status_code=400, detail="CentreDeCongres ID is required")

    db_elementcentre = ElementCentre(
        description=elementcentre_data.description,        nom=elementcentre_data.nom,        capaciteMax=elementcentre_data.capaciteMax,        centredecongres_1_id=elementcentre_data.centredecongres_1        )

    database.add(db_elementcentre)
    database.commit()
    database.refresh(db_elementcentre)

    if elementcentre_data.indisponibilte:
        # Validate that all Indisponibilte IDs exist
        for indisponibilte_id in elementcentre_data.indisponibilte:
            db_indisponibilte = database.query(Indisponibilte).filter(Indisponibilte.id == indisponibilte_id).first()
            if not db_indisponibilte:
                raise HTTPException(status_code=400, detail=f"Indisponibilte with id {indisponibilte_id} not found")

        # Update the related entities with the new foreign key
        database.query(Indisponibilte).filter(Indisponibilte.id.in_(elementcentre_data.indisponibilte)).update(
            {Indisponibilte.elementcentre_4_id: db_elementcentre.id}, synchronize_session=False
        )
        database.commit()
    if elementcentre_data.tarif_1:
        # Validate that all Tarif IDs exist
        for tarif_id in elementcentre_data.tarif_1:
            db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
            if not db_tarif:
                raise HTTPException(status_code=400, detail=f"Tarif with id {tarif_id} not found")

        # Update the related entities with the new foreign key
        database.query(Tarif).filter(Tarif.id.in_(elementcentre_data.tarif_1)).update(
            {Tarif.elementcentre_2_id: db_elementcentre.id}, synchronize_session=False
        )
        database.commit()



    indisponibilte_ids = database.query(Indisponibilte.id).filter(Indisponibilte.elementcentre_4_id == db_elementcentre.id).all()
    tarif_1_ids = database.query(Tarif.id).filter(Tarif.elementcentre_2_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "indisponibilte_ids": [x[0] for x in indisponibilte_ids],        "tarif_1_ids": [x[0] for x in tarif_1_ids]    }
    return response_data


@app.post("/elementcentre/bulk/", response_model=None, tags=["ElementCentre"])
async def bulk_create_elementcentre(items: list[ElementCentreCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ElementCentre entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.centredecongres_1:
                raise ValueError("CentreDeCongres ID is required")

            db_elementcentre = ElementCentre(
                description=item_data.description,                nom=item_data.nom,                capaciteMax=item_data.capaciteMax,                centredecongres_1_id=item_data.centredecongres_1            )
            database.add(db_elementcentre)
            database.flush()  # Get ID without committing
            created_items.append(db_elementcentre.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ElementCentre entities"
    }


@app.delete("/elementcentre/bulk/", response_model=None, tags=["ElementCentre"])
async def bulk_delete_elementcentre(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ElementCentre entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == item_id).first()
        if db_elementcentre:
            database.delete(db_elementcentre)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ElementCentre entities"
    }

@app.put("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def update_elementcentre(elementcentre_id: int, elementcentre_data: ElementCentreCreate, database: Session = Depends(get_db)) -> ElementCentre:
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    setattr(db_elementcentre, 'description', elementcentre_data.description)
    setattr(db_elementcentre, 'nom', elementcentre_data.nom)
    setattr(db_elementcentre, 'capaciteMax', elementcentre_data.capaciteMax)
    if elementcentre_data.centredecongres_1 is not None:
        db_centredecongres_1 = database.query(CentreDeCongres).filter(CentreDeCongres.id == elementcentre_data.centredecongres_1).first()
        if not db_centredecongres_1:
            raise HTTPException(status_code=400, detail="CentreDeCongres not found")
        setattr(db_elementcentre, 'centredecongres_1_id', elementcentre_data.centredecongres_1)
    if elementcentre_data.indisponibilte is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Indisponibilte).filter(Indisponibilte.elementcentre_4_id == db_elementcentre.id).update(
            {Indisponibilte.elementcentre_4_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if elementcentre_data.indisponibilte:
            # Validate that all IDs exist
            for indisponibilte_id in elementcentre_data.indisponibilte:
                db_indisponibilte = database.query(Indisponibilte).filter(Indisponibilte.id == indisponibilte_id).first()
                if not db_indisponibilte:
                    raise HTTPException(status_code=400, detail=f"Indisponibilte with id {indisponibilte_id} not found")

            # Update the related entities with the new foreign key
            database.query(Indisponibilte).filter(Indisponibilte.id.in_(elementcentre_data.indisponibilte)).update(
                {Indisponibilte.elementcentre_4_id: db_elementcentre.id}, synchronize_session=False
            )
    if elementcentre_data.tarif_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Tarif).filter(Tarif.elementcentre_2_id == db_elementcentre.id).update(
            {Tarif.elementcentre_2_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if elementcentre_data.tarif_1:
            # Validate that all IDs exist
            for tarif_id in elementcentre_data.tarif_1:
                db_tarif = database.query(Tarif).filter(Tarif.id == tarif_id).first()
                if not db_tarif:
                    raise HTTPException(status_code=400, detail=f"Tarif with id {tarif_id} not found")

            # Update the related entities with the new foreign key
            database.query(Tarif).filter(Tarif.id.in_(elementcentre_data.tarif_1)).update(
                {Tarif.elementcentre_2_id: db_elementcentre.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_elementcentre)

    indisponibilte_ids = database.query(Indisponibilte.id).filter(Indisponibilte.elementcentre_4_id == db_elementcentre.id).all()
    tarif_1_ids = database.query(Tarif.id).filter(Tarif.elementcentre_2_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "indisponibilte_ids": [x[0] for x in indisponibilte_ids],        "tarif_1_ids": [x[0] for x in tarif_1_ids]    }
    return response_data


@app.delete("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def delete_elementcentre(elementcentre_id: int, database: Session = Depends(get_db)):
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")
    database.delete(db_elementcentre)
    database.commit()
    return db_elementcentre





############################################
#
#   Evenement functions
#
############################################

@app.get("/evenement/", response_model=None, tags=["Evenement"])
def get_all_evenement(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Evenement)
        query = query.options(joinedload(Evenement.personnereferente))
        evenement_list = query.all()

        # Serialize with relationships included
        result = []
        for evenement_item in evenement_list:
            item_dict = evenement_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if evenement_item.personnereferente:
                related_obj = evenement_item.personnereferente
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['personnereferente'] = related_dict
            else:
                item_dict['personnereferente'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Evenement).all()


@app.get("/evenement/count/", response_model=None, tags=["Evenement"])
def get_count_evenement(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Evenement entities"""
    count = database.query(Evenement).count()
    return {"count": count}


@app.get("/evenement/paginated/", response_model=None, tags=["Evenement"])
def get_paginated_evenement(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Evenement entities"""
    total = database.query(Evenement).count()
    evenement_list = database.query(Evenement).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": evenement_list
    }


@app.get("/evenement/search/", response_model=None, tags=["Evenement"])
def search_evenement(
    database: Session = Depends(get_db)
) -> list:
    """Search Evenement entities by attributes"""
    query = database.query(Evenement)


    results = query.all()
    return results


@app.get("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def get_evenement(evenement_id: int, database: Session = Depends(get_db)) -> Evenement:
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")

    response_data = {
        "evenement": db_evenement,
}
    return response_data



@app.post("/evenement/", response_model=None, tags=["Evenement"])
async def create_evenement(evenement_data: EvenementCreate, database: Session = Depends(get_db)) -> Evenement:

    if evenement_data.personnereferente is not None:
        db_personnereferente = database.query(PersonneReferente).filter(PersonneReferente.id == evenement_data.personnereferente).first()
        if not db_personnereferente:
            raise HTTPException(status_code=400, detail="PersonneReferente not found")
    else:
        raise HTTPException(status_code=400, detail="PersonneReferente ID is required")

    db_evenement = Evenement(
        nom=evenement_data.nom,        nbParticipantPrevus=evenement_data.nbParticipantPrevus,        description=evenement_data.description,        personnereferente_id=evenement_data.personnereferente        )

    database.add(db_evenement)
    database.commit()
    database.refresh(db_evenement)




    return db_evenement


@app.post("/evenement/bulk/", response_model=None, tags=["Evenement"])
async def bulk_create_evenement(items: list[EvenementCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Evenement entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.personnereferente:
                raise ValueError("PersonneReferente ID is required")

            db_evenement = Evenement(
                nom=item_data.nom,                nbParticipantPrevus=item_data.nbParticipantPrevus,                description=item_data.description,                personnereferente_id=item_data.personnereferente            )
            database.add(db_evenement)
            database.flush()  # Get ID without committing
            created_items.append(db_evenement.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Evenement entities"
    }


@app.delete("/evenement/bulk/", response_model=None, tags=["Evenement"])
async def bulk_delete_evenement(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Evenement entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_evenement = database.query(Evenement).filter(Evenement.id == item_id).first()
        if db_evenement:
            database.delete(db_evenement)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Evenement entities"
    }

@app.put("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def update_evenement(evenement_id: int, evenement_data: EvenementCreate, database: Session = Depends(get_db)) -> Evenement:
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")

    setattr(db_evenement, 'nom', evenement_data.nom)
    setattr(db_evenement, 'nbParticipantPrevus', evenement_data.nbParticipantPrevus)
    setattr(db_evenement, 'description', evenement_data.description)
    if evenement_data.personnereferente is not None:
        db_personnereferente = database.query(PersonneReferente).filter(PersonneReferente.id == evenement_data.personnereferente).first()
        if not db_personnereferente:
            raise HTTPException(status_code=400, detail="PersonneReferente not found")
        setattr(db_evenement, 'personnereferente_id', evenement_data.personnereferente)
    database.commit()
    database.refresh(db_evenement)

    return db_evenement


@app.delete("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def delete_evenement(evenement_id: int, database: Session = Depends(get_db)):
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")
    database.delete(db_evenement)
    database.commit()
    return db_evenement





############################################
#
#   Paiement functions
#
############################################

@app.get("/paiement/", response_model=None, tags=["Paiement"])
def get_all_paiement(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    return database.query(Paiement).all()


@app.get("/paiement/count/", response_model=None, tags=["Paiement"])
def get_count_paiement(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Paiement entities"""
    count = database.query(Paiement).count()
    return {"count": count}


@app.get("/paiement/paginated/", response_model=None, tags=["Paiement"])
def get_paginated_paiement(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Paiement entities"""
    total = database.query(Paiement).count()
    paiement_list = database.query(Paiement).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": paiement_list
    }


@app.get("/paiement/search/", response_model=None, tags=["Paiement"])
def search_paiement(
    database: Session = Depends(get_db)
) -> list:
    """Search Paiement entities by attributes"""
    query = database.query(Paiement)


    results = query.all()
    return results


@app.get("/paiement/{paiement_id}/", response_model=None, tags=["Paiement"])
async def get_paiement(paiement_id: int, database: Session = Depends(get_db)) -> Paiement:
    db_paiement = database.query(Paiement).filter(Paiement.id == paiement_id).first()
    if db_paiement is None:
        raise HTTPException(status_code=404, detail="Paiement not found")

    response_data = {
        "paiement": db_paiement,
}
    return response_data



@app.post("/paiement/", response_model=None, tags=["Paiement"])
async def create_paiement(paiement_data: PaiementCreate, database: Session = Depends(get_db)) -> Paiement:


    db_paiement = Paiement(
        reference=paiement_data.reference,        dateTransaction=paiement_data.dateTransaction,        montant=paiement_data.montant        )

    database.add(db_paiement)
    database.commit()
    database.refresh(db_paiement)




    return db_paiement


@app.post("/paiement/bulk/", response_model=None, tags=["Paiement"])
async def bulk_create_paiement(items: list[PaiementCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Paiement entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_paiement = Paiement(
                reference=item_data.reference,                dateTransaction=item_data.dateTransaction,                montant=item_data.montant            )
            database.add(db_paiement)
            database.flush()  # Get ID without committing
            created_items.append(db_paiement.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Paiement entities"
    }


@app.delete("/paiement/bulk/", response_model=None, tags=["Paiement"])
async def bulk_delete_paiement(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Paiement entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_paiement = database.query(Paiement).filter(Paiement.id == item_id).first()
        if db_paiement:
            database.delete(db_paiement)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Paiement entities"
    }

@app.put("/paiement/{paiement_id}/", response_model=None, tags=["Paiement"])
async def update_paiement(paiement_id: int, paiement_data: PaiementCreate, database: Session = Depends(get_db)) -> Paiement:
    db_paiement = database.query(Paiement).filter(Paiement.id == paiement_id).first()
    if db_paiement is None:
        raise HTTPException(status_code=404, detail="Paiement not found")

    setattr(db_paiement, 'reference', paiement_data.reference)
    setattr(db_paiement, 'dateTransaction', paiement_data.dateTransaction)
    setattr(db_paiement, 'montant', paiement_data.montant)
    database.commit()
    database.refresh(db_paiement)

    return db_paiement


@app.delete("/paiement/{paiement_id}/", response_model=None, tags=["Paiement"])
async def delete_paiement(paiement_id: int, database: Session = Depends(get_db)):
    db_paiement = database.query(Paiement).filter(Paiement.id == paiement_id).first()
    if db_paiement is None:
        raise HTTPException(status_code=404, detail="Paiement not found")
    database.delete(db_paiement)
    database.commit()
    return db_paiement



############################################
#   Paiement Method Endpoints
############################################




@app.post("/paiement/methods/method/", response_model=None, tags=["Paiement Methods"])
async def paiement_method(
    database: Session = Depends(get_db)
):
    """
    Execute the method class method on Paiement.
    This method operates on all Paiement entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Paiement",
            "method": "method",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   CentreDeCongres functions
#
############################################

@app.get("/centredecongres/", response_model=None, tags=["CentreDeCongres"])
def get_all_centredecongres(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(CentreDeCongres)
        centredecongres_list = query.all()

        # Serialize with relationships included
        result = []
        for centredecongres_item in centredecongres_list:
            item_dict = centredecongres_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            materiel_list = database.query(Materiel).filter(Materiel.centredecongres_2_id == centredecongres_item.id).all()
            item_dict['materiel_1'] = []
            for materiel_obj in materiel_list:
                materiel_dict = materiel_obj.__dict__.copy()
                materiel_dict.pop('_sa_instance_state', None)
                item_dict['materiel_1'].append(materiel_dict)
            prestation_list = database.query(Prestation).filter(Prestation.centredecongres_3_id == centredecongres_item.id).all()
            item_dict['prestation_1'] = []
            for prestation_obj in prestation_list:
                prestation_dict = prestation_obj.__dict__.copy()
                prestation_dict.pop('_sa_instance_state', None)
                item_dict['prestation_1'].append(prestation_dict)
            elementcentre_list = database.query(ElementCentre).filter(ElementCentre.centredecongres_1_id == centredecongres_item.id).all()
            item_dict['elementcentre_1'] = []
            for elementcentre_obj in elementcentre_list:
                elementcentre_dict = elementcentre_obj.__dict__.copy()
                elementcentre_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre_1'].append(elementcentre_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(CentreDeCongres).all()


@app.get("/centredecongres/count/", response_model=None, tags=["CentreDeCongres"])
def get_count_centredecongres(database: Session = Depends(get_db)) -> dict:
    """Get the total count of CentreDeCongres entities"""
    count = database.query(CentreDeCongres).count()
    return {"count": count}


@app.get("/centredecongres/paginated/", response_model=None, tags=["CentreDeCongres"])
def get_paginated_centredecongres(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of CentreDeCongres entities"""
    total = database.query(CentreDeCongres).count()
    centredecongres_list = database.query(CentreDeCongres).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": centredecongres_list
        }

    result = []
    for centredecongres_item in centredecongres_list:
        materiel_1_ids = database.query(Materiel.id).filter(Materiel.centredecongres_2_id == centredecongres_item.id).all()
        prestation_1_ids = database.query(Prestation.id).filter(Prestation.centredecongres_3_id == centredecongres_item.id).all()
        elementcentre_1_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == centredecongres_item.id).all()
        item_data = {
            "centredecongres": centredecongres_item,
            "materiel_1_ids": [x[0] for x in materiel_1_ids],            "prestation_1_ids": [x[0] for x in prestation_1_ids],            "elementcentre_1_ids": [x[0] for x in elementcentre_1_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/centredecongres/search/", response_model=None, tags=["CentreDeCongres"])
def search_centredecongres(
    database: Session = Depends(get_db)
) -> list:
    """Search CentreDeCongres entities by attributes"""
    query = database.query(CentreDeCongres)


    results = query.all()
    return results


@app.get("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentreDeCongres"])
async def get_centredecongres(centredecongres_id: int, database: Session = Depends(get_db)) -> CentreDeCongres:
    db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentreDeCongres not found")

    materiel_1_ids = database.query(Materiel.id).filter(Materiel.centredecongres_2_id == db_centredecongres.id).all()
    prestation_1_ids = database.query(Prestation.id).filter(Prestation.centredecongres_3_id == db_centredecongres.id).all()
    elementcentre_1_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "materiel_1_ids": [x[0] for x in materiel_1_ids],        "prestation_1_ids": [x[0] for x in prestation_1_ids],        "elementcentre_1_ids": [x[0] for x in elementcentre_1_ids]}
    return response_data



@app.post("/centredecongres/", response_model=None, tags=["CentreDeCongres"])
async def create_centredecongres(centredecongres_data: CentreDeCongresCreate, database: Session = Depends(get_db)) -> CentreDeCongres:


    db_centredecongres = CentreDeCongres(
        adresse=centredecongres_data.adresse,        description=centredecongres_data.description,        nom=centredecongres_data.nom        )

    database.add(db_centredecongres)
    database.commit()
    database.refresh(db_centredecongres)

    if centredecongres_data.materiel_1:
        # Validate that all Materiel IDs exist
        for materiel_id in centredecongres_data.materiel_1:
            db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
            if not db_materiel:
                raise HTTPException(status_code=400, detail=f"Materiel with id {materiel_id} not found")

        # Update the related entities with the new foreign key
        database.query(Materiel).filter(Materiel.id.in_(centredecongres_data.materiel_1)).update(
            {Materiel.centredecongres_2_id: db_centredecongres.id}, synchronize_session=False
        )
        database.commit()
    if centredecongres_data.prestation_1:
        # Validate that all Prestation IDs exist
        for prestation_id in centredecongres_data.prestation_1:
            db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
            if not db_prestation:
                raise HTTPException(status_code=400, detail=f"Prestation with id {prestation_id} not found")

        # Update the related entities with the new foreign key
        database.query(Prestation).filter(Prestation.id.in_(centredecongres_data.prestation_1)).update(
            {Prestation.centredecongres_3_id: db_centredecongres.id}, synchronize_session=False
        )
        database.commit()
    if centredecongres_data.elementcentre_1:
        # Validate that all ElementCentre IDs exist
        for elementcentre_id in centredecongres_data.elementcentre_1:
            db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
            if not db_elementcentre:
                raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

        # Update the related entities with the new foreign key
        database.query(ElementCentre).filter(ElementCentre.id.in_(centredecongres_data.elementcentre_1)).update(
            {ElementCentre.centredecongres_1_id: db_centredecongres.id}, synchronize_session=False
        )
        database.commit()



    materiel_1_ids = database.query(Materiel.id).filter(Materiel.centredecongres_2_id == db_centredecongres.id).all()
    prestation_1_ids = database.query(Prestation.id).filter(Prestation.centredecongres_3_id == db_centredecongres.id).all()
    elementcentre_1_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "materiel_1_ids": [x[0] for x in materiel_1_ids],        "prestation_1_ids": [x[0] for x in prestation_1_ids],        "elementcentre_1_ids": [x[0] for x in elementcentre_1_ids]    }
    return response_data


@app.post("/centredecongres/bulk/", response_model=None, tags=["CentreDeCongres"])
async def bulk_create_centredecongres(items: list[CentreDeCongresCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple CentreDeCongres entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_centredecongres = CentreDeCongres(
                adresse=item_data.adresse,                description=item_data.description,                nom=item_data.nom            )
            database.add(db_centredecongres)
            database.flush()  # Get ID without committing
            created_items.append(db_centredecongres.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} CentreDeCongres entities"
    }


@app.delete("/centredecongres/bulk/", response_model=None, tags=["CentreDeCongres"])
async def bulk_delete_centredecongres(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple CentreDeCongres entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == item_id).first()
        if db_centredecongres:
            database.delete(db_centredecongres)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} CentreDeCongres entities"
    }

@app.put("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentreDeCongres"])
async def update_centredecongres(centredecongres_id: int, centredecongres_data: CentreDeCongresCreate, database: Session = Depends(get_db)) -> CentreDeCongres:
    db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentreDeCongres not found")

    setattr(db_centredecongres, 'adresse', centredecongres_data.adresse)
    setattr(db_centredecongres, 'description', centredecongres_data.description)
    setattr(db_centredecongres, 'nom', centredecongres_data.nom)
    if centredecongres_data.materiel_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Materiel).filter(Materiel.centredecongres_2_id == db_centredecongres.id).update(
            {Materiel.centredecongres_2_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if centredecongres_data.materiel_1:
            # Validate that all IDs exist
            for materiel_id in centredecongres_data.materiel_1:
                db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
                if not db_materiel:
                    raise HTTPException(status_code=400, detail=f"Materiel with id {materiel_id} not found")

            # Update the related entities with the new foreign key
            database.query(Materiel).filter(Materiel.id.in_(centredecongres_data.materiel_1)).update(
                {Materiel.centredecongres_2_id: db_centredecongres.id}, synchronize_session=False
            )
    if centredecongres_data.prestation_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Prestation).filter(Prestation.centredecongres_3_id == db_centredecongres.id).update(
            {Prestation.centredecongres_3_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if centredecongres_data.prestation_1:
            # Validate that all IDs exist
            for prestation_id in centredecongres_data.prestation_1:
                db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
                if not db_prestation:
                    raise HTTPException(status_code=400, detail=f"Prestation with id {prestation_id} not found")

            # Update the related entities with the new foreign key
            database.query(Prestation).filter(Prestation.id.in_(centredecongres_data.prestation_1)).update(
                {Prestation.centredecongres_3_id: db_centredecongres.id}, synchronize_session=False
            )
    if centredecongres_data.elementcentre_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ElementCentre).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).update(
            {ElementCentre.centredecongres_1_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if centredecongres_data.elementcentre_1:
            # Validate that all IDs exist
            for elementcentre_id in centredecongres_data.elementcentre_1:
                db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
                if not db_elementcentre:
                    raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

            # Update the related entities with the new foreign key
            database.query(ElementCentre).filter(ElementCentre.id.in_(centredecongres_data.elementcentre_1)).update(
                {ElementCentre.centredecongres_1_id: db_centredecongres.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_centredecongres)

    materiel_1_ids = database.query(Materiel.id).filter(Materiel.centredecongres_2_id == db_centredecongres.id).all()
    prestation_1_ids = database.query(Prestation.id).filter(Prestation.centredecongres_3_id == db_centredecongres.id).all()
    elementcentre_1_ids = database.query(ElementCentre.id).filter(ElementCentre.centredecongres_1_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "materiel_1_ids": [x[0] for x in materiel_1_ids],        "prestation_1_ids": [x[0] for x in prestation_1_ids],        "elementcentre_1_ids": [x[0] for x in elementcentre_1_ids]    }
    return response_data


@app.delete("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentreDeCongres"])
async def delete_centredecongres(centredecongres_id: int, database: Session = Depends(get_db)):
    db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentreDeCongres not found")
    database.delete(db_centredecongres)
    database.commit()
    return db_centredecongres





############################################
#
#   Reservation functions
#
############################################

@app.get("/reservation/", response_model=None, tags=["Reservation"])
def get_all_reservation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Reservation)
        query = query.options(joinedload(Reservation.evenement))
        query = query.options(joinedload(Reservation.paiement))
        query = query.options(joinedload(Reservation.tarif))
        reservation_list = query.all()

        # Serialize with relationships included
        result = []
        for reservation_item in reservation_list:
            item_dict = reservation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if reservation_item.evenement:
                related_obj = reservation_item.evenement
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['evenement'] = related_dict
            else:
                item_dict['evenement'] = None
            if reservation_item.paiement:
                related_obj = reservation_item.paiement
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['paiement'] = related_dict
            else:
                item_dict['paiement'] = None
            if reservation_item.tarif:
                related_obj = reservation_item.tarif
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['tarif'] = related_dict
            else:
                item_dict['tarif'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            materiel_list = database.query(Materiel).filter(Materiel.reservation_4_id == reservation_item.id).all()
            item_dict['materiel'] = []
            for materiel_obj in materiel_list:
                materiel_dict = materiel_obj.__dict__.copy()
                materiel_dict.pop('_sa_instance_state', None)
                item_dict['materiel'].append(materiel_dict)
            prestation_list = database.query(Prestation).filter(Prestation.reservation_5_id == reservation_item.id).all()
            item_dict['prestation'] = []
            for prestation_obj in prestation_list:
                prestation_dict = prestation_obj.__dict__.copy()
                prestation_dict.pop('_sa_instance_state', None)
                item_dict['prestation'].append(prestation_dict)
            elementcentre_list = database.query(ElementCentre).filter(ElementCentre.reservation_3_id == reservation_item.id).all()
            item_dict['elementcentre'] = []
            for elementcentre_obj in elementcentre_list:
                elementcentre_dict = elementcentre_obj.__dict__.copy()
                elementcentre_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre'].append(elementcentre_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Reservation).all()


@app.get("/reservation/count/", response_model=None, tags=["Reservation"])
def get_count_reservation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Reservation entities"""
    count = database.query(Reservation).count()
    return {"count": count}


@app.get("/reservation/paginated/", response_model=None, tags=["Reservation"])
def get_paginated_reservation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Reservation entities"""
    total = database.query(Reservation).count()
    reservation_list = database.query(Reservation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": reservation_list
        }

    result = []
    for reservation_item in reservation_list:
        materiel_ids = database.query(Materiel.id).filter(Materiel.reservation_4_id == reservation_item.id).all()
        prestation_ids = database.query(Prestation.id).filter(Prestation.reservation_5_id == reservation_item.id).all()
        elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.reservation_3_id == reservation_item.id).all()
        item_data = {
            "reservation": reservation_item,
            "materiel_ids": [x[0] for x in materiel_ids],            "prestation_ids": [x[0] for x in prestation_ids],            "elementcentre_ids": [x[0] for x in elementcentre_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/reservation/search/", response_model=None, tags=["Reservation"])
def search_reservation(
    database: Session = Depends(get_db)
) -> list:
    """Search Reservation entities by attributes"""
    query = database.query(Reservation)


    results = query.all()
    return results


@app.get("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def get_reservation(reservation_id: int, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    materiel_ids = database.query(Materiel.id).filter(Materiel.reservation_4_id == db_reservation.id).all()
    prestation_ids = database.query(Prestation.id).filter(Prestation.reservation_5_id == db_reservation.id).all()
    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.reservation_3_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "materiel_ids": [x[0] for x in materiel_ids],        "prestation_ids": [x[0] for x in prestation_ids],        "elementcentre_ids": [x[0] for x in elementcentre_ids]}
    return response_data



@app.post("/reservation/", response_model=None, tags=["Reservation"])
async def create_reservation(reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:

    if reservation_data.tarif is not None:
        db_tarif = database.query(Tarif).filter(Tarif.id == reservation_data.tarif).first()
        if not db_tarif:
            raise HTTPException(status_code=400, detail="Tarif not found")
    else:
        raise HTTPException(status_code=400, detail="Tarif ID is required")

    db_reservation = Reservation(
        dateCreation=reservation_data.dateCreation,        coutTotal=reservation_data.coutTotal,        dateFin=reservation_data.dateFin,        dateDebut=reservation_data.dateDebut,        Statut=reservation_data.Statut.value,        delaiDeConfirmation=reservation_data.delaiDeConfirmation,        tarif_id=reservation_data.tarif        )

    database.add(db_reservation)
    database.commit()
    database.refresh(db_reservation)

    if reservation_data.materiel:
        # Validate that all Materiel IDs exist
        for materiel_id in reservation_data.materiel:
            db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
            if not db_materiel:
                raise HTTPException(status_code=400, detail=f"Materiel with id {materiel_id} not found")

        # Update the related entities with the new foreign key
        database.query(Materiel).filter(Materiel.id.in_(reservation_data.materiel)).update(
            {Materiel.reservation_4_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()
    if reservation_data.prestation:
        # Validate that all Prestation IDs exist
        for prestation_id in reservation_data.prestation:
            db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
            if not db_prestation:
                raise HTTPException(status_code=400, detail=f"Prestation with id {prestation_id} not found")

        # Update the related entities with the new foreign key
        database.query(Prestation).filter(Prestation.id.in_(reservation_data.prestation)).update(
            {Prestation.reservation_5_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()
    if reservation_data.elementcentre:
        # Validate that all ElementCentre IDs exist
        for elementcentre_id in reservation_data.elementcentre:
            db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
            if not db_elementcentre:
                raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

        # Update the related entities with the new foreign key
        database.query(ElementCentre).filter(ElementCentre.id.in_(reservation_data.elementcentre)).update(
            {ElementCentre.reservation_3_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()



    materiel_ids = database.query(Materiel.id).filter(Materiel.reservation_4_id == db_reservation.id).all()
    prestation_ids = database.query(Prestation.id).filter(Prestation.reservation_5_id == db_reservation.id).all()
    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.reservation_3_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "materiel_ids": [x[0] for x in materiel_ids],        "prestation_ids": [x[0] for x in prestation_ids],        "elementcentre_ids": [x[0] for x in elementcentre_ids]    }
    return response_data


@app.post("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_create_reservation(items: list[ReservationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Reservation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.tarif:
                raise ValueError("Tarif ID is required")

            db_reservation = Reservation(
                dateCreation=item_data.dateCreation,                coutTotal=item_data.coutTotal,                dateFin=item_data.dateFin,                dateDebut=item_data.dateDebut,                Statut=item_data.Statut.value,                delaiDeConfirmation=item_data.delaiDeConfirmation,                tarif_id=item_data.tarif            )
            database.add(db_reservation)
            database.flush()  # Get ID without committing
            created_items.append(db_reservation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Reservation entities"
    }


@app.delete("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_delete_reservation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Reservation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == item_id).first()
        if db_reservation:
            database.delete(db_reservation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Reservation entities"
    }

@app.put("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def update_reservation(reservation_id: int, reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    setattr(db_reservation, 'dateCreation', reservation_data.dateCreation)
    setattr(db_reservation, 'coutTotal', reservation_data.coutTotal)
    setattr(db_reservation, 'dateFin', reservation_data.dateFin)
    setattr(db_reservation, 'dateDebut', reservation_data.dateDebut)
    setattr(db_reservation, 'Statut', reservation_data.Statut.value)
    setattr(db_reservation, 'delaiDeConfirmation', reservation_data.delaiDeConfirmation)
    if reservation_data.tarif is not None:
        db_tarif = database.query(Tarif).filter(Tarif.id == reservation_data.tarif).first()
        if not db_tarif:
            raise HTTPException(status_code=400, detail="Tarif not found")
        setattr(db_reservation, 'tarif_id', reservation_data.tarif)
    if reservation_data.materiel is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Materiel).filter(Materiel.reservation_4_id == db_reservation.id).update(
            {Materiel.reservation_4_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.materiel:
            # Validate that all IDs exist
            for materiel_id in reservation_data.materiel:
                db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
                if not db_materiel:
                    raise HTTPException(status_code=400, detail=f"Materiel with id {materiel_id} not found")

            # Update the related entities with the new foreign key
            database.query(Materiel).filter(Materiel.id.in_(reservation_data.materiel)).update(
                {Materiel.reservation_4_id: db_reservation.id}, synchronize_session=False
            )
    if reservation_data.prestation is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Prestation).filter(Prestation.reservation_5_id == db_reservation.id).update(
            {Prestation.reservation_5_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.prestation:
            # Validate that all IDs exist
            for prestation_id in reservation_data.prestation:
                db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
                if not db_prestation:
                    raise HTTPException(status_code=400, detail=f"Prestation with id {prestation_id} not found")

            # Update the related entities with the new foreign key
            database.query(Prestation).filter(Prestation.id.in_(reservation_data.prestation)).update(
                {Prestation.reservation_5_id: db_reservation.id}, synchronize_session=False
            )
    if reservation_data.elementcentre is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ElementCentre).filter(ElementCentre.reservation_3_id == db_reservation.id).update(
            {ElementCentre.reservation_3_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.elementcentre:
            # Validate that all IDs exist
            for elementcentre_id in reservation_data.elementcentre:
                db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
                if not db_elementcentre:
                    raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

            # Update the related entities with the new foreign key
            database.query(ElementCentre).filter(ElementCentre.id.in_(reservation_data.elementcentre)).update(
                {ElementCentre.reservation_3_id: db_reservation.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_reservation)

    materiel_ids = database.query(Materiel.id).filter(Materiel.reservation_4_id == db_reservation.id).all()
    prestation_ids = database.query(Prestation.id).filter(Prestation.reservation_5_id == db_reservation.id).all()
    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.reservation_3_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "materiel_ids": [x[0] for x in materiel_ids],        "prestation_ids": [x[0] for x in prestation_ids],        "elementcentre_ids": [x[0] for x in elementcentre_ids]    }
    return response_data


@app.delete("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def delete_reservation(reservation_id: int, database: Session = Depends(get_db)):
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    database.delete(db_reservation)
    database.commit()
    return db_reservation



############################################
#   Reservation Method Endpoints
############################################




@app.post("/reservation/{reservation_id}/methods/confirmer/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_confirmer(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the confirmer method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Add your docstring here."""
            # Add your implementation here
            pass


        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "confirmer",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/modifier/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_modifier(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the modifier method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Add your docstring here."""
            # Add your implementation here
            pass


        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "modifier",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/calculerCout/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_calculerCout(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCout method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Add your docstring here."""
            # Add your implementation here
            pass


        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "calculerCout",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/annuler/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_annuler(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the annuler method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Add your docstring here."""
            # Add your implementation here
            pass


        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "annuler",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Gestionnaire functions
#
############################################

@app.get("/gestionnaire/", response_model=None, tags=["Gestionnaire"])
def get_all_gestionnaire(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Gestionnaire)
        gestionnaire_list = query.all()

        # Serialize with relationships included
        result = []
        for gestionnaire_item in gestionnaire_list:
            item_dict = gestionnaire_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            centredecongres_list = database.query(CentreDeCongres).filter(CentreDeCongres.gestionnaire_1_id == gestionnaire_item.id).all()
            item_dict['centredecongres'] = []
            for centredecongres_obj in centredecongres_list:
                centredecongres_dict = centredecongres_obj.__dict__.copy()
                centredecongres_dict.pop('_sa_instance_state', None)
                item_dict['centredecongres'].append(centredecongres_dict)
            reservation_list = database.query(Reservation).filter(Reservation.gestionnaire_id == gestionnaire_item.id).all()
            item_dict['reservation'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['reservation'].append(reservation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Gestionnaire).all()


@app.get("/gestionnaire/count/", response_model=None, tags=["Gestionnaire"])
def get_count_gestionnaire(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Gestionnaire entities"""
    count = database.query(Gestionnaire).count()
    return {"count": count}


@app.get("/gestionnaire/paginated/", response_model=None, tags=["Gestionnaire"])
def get_paginated_gestionnaire(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Gestionnaire entities"""
    total = database.query(Gestionnaire).count()
    gestionnaire_list = database.query(Gestionnaire).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": gestionnaire_list
        }

    result = []
    for gestionnaire_item in gestionnaire_list:
        centredecongres_ids = database.query(CentreDeCongres.id).filter(CentreDeCongres.gestionnaire_1_id == gestionnaire_item.id).all()
        reservation_ids = database.query(Reservation.id).filter(Reservation.gestionnaire_id == gestionnaire_item.id).all()
        item_data = {
            "gestionnaire": gestionnaire_item,
            "centredecongres_ids": [x[0] for x in centredecongres_ids],            "reservation_ids": [x[0] for x in reservation_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/gestionnaire/search/", response_model=None, tags=["Gestionnaire"])
def search_gestionnaire(
    database: Session = Depends(get_db)
) -> list:
    """Search Gestionnaire entities by attributes"""
    query = database.query(Gestionnaire)


    results = query.all()
    return results


@app.get("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def get_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)) -> Gestionnaire:
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    centredecongres_ids = database.query(CentreDeCongres.id).filter(CentreDeCongres.gestionnaire_1_id == db_gestionnaire.id).all()
    reservation_ids = database.query(Reservation.id).filter(Reservation.gestionnaire_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "centredecongres_ids": [x[0] for x in centredecongres_ids],        "reservation_ids": [x[0] for x in reservation_ids]}
    return response_data



@app.post("/gestionnaire/", response_model=None, tags=["Gestionnaire"])
async def create_gestionnaire(gestionnaire_data: GestionnaireCreate, database: Session = Depends(get_db)) -> Gestionnaire:


    db_gestionnaire = Gestionnaire(
        motDePass=gestionnaire_data.motDePass,        nom=gestionnaire_data.nom,        prenom=gestionnaire_data.prenom,        email=gestionnaire_data.email        )

    database.add(db_gestionnaire)
    database.commit()
    database.refresh(db_gestionnaire)

    if gestionnaire_data.centredecongres:
        # Validate that all CentreDeCongres IDs exist
        for centredecongres_id in gestionnaire_data.centredecongres:
            db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
            if not db_centredecongres:
                raise HTTPException(status_code=400, detail=f"CentreDeCongres with id {centredecongres_id} not found")

        # Update the related entities with the new foreign key
        database.query(CentreDeCongres).filter(CentreDeCongres.id.in_(gestionnaire_data.centredecongres)).update(
            {CentreDeCongres.gestionnaire_1_id: db_gestionnaire.id}, synchronize_session=False
        )
        database.commit()
    if gestionnaire_data.reservation:
        # Validate that all Reservation IDs exist
        for reservation_id in gestionnaire_data.reservation:
            db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
            if not db_reservation:
                raise HTTPException(status_code=400, detail=f"Reservation with id {reservation_id} not found")

        # Update the related entities with the new foreign key
        database.query(Reservation).filter(Reservation.id.in_(gestionnaire_data.reservation)).update(
            {Reservation.gestionnaire_id: db_gestionnaire.id}, synchronize_session=False
        )
        database.commit()



    centredecongres_ids = database.query(CentreDeCongres.id).filter(CentreDeCongres.gestionnaire_1_id == db_gestionnaire.id).all()
    reservation_ids = database.query(Reservation.id).filter(Reservation.gestionnaire_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "centredecongres_ids": [x[0] for x in centredecongres_ids],        "reservation_ids": [x[0] for x in reservation_ids]    }
    return response_data


@app.post("/gestionnaire/bulk/", response_model=None, tags=["Gestionnaire"])
async def bulk_create_gestionnaire(items: list[GestionnaireCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Gestionnaire entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_gestionnaire = Gestionnaire(
                motDePass=item_data.motDePass,                nom=item_data.nom,                prenom=item_data.prenom,                email=item_data.email            )
            database.add(db_gestionnaire)
            database.flush()  # Get ID without committing
            created_items.append(db_gestionnaire.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Gestionnaire entities"
    }


@app.delete("/gestionnaire/bulk/", response_model=None, tags=["Gestionnaire"])
async def bulk_delete_gestionnaire(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Gestionnaire entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == item_id).first()
        if db_gestionnaire:
            database.delete(db_gestionnaire)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Gestionnaire entities"
    }

@app.put("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def update_gestionnaire(gestionnaire_id: int, gestionnaire_data: GestionnaireCreate, database: Session = Depends(get_db)) -> Gestionnaire:
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    setattr(db_gestionnaire, 'motDePass', gestionnaire_data.motDePass)
    setattr(db_gestionnaire, 'nom', gestionnaire_data.nom)
    setattr(db_gestionnaire, 'prenom', gestionnaire_data.prenom)
    setattr(db_gestionnaire, 'email', gestionnaire_data.email)
    if gestionnaire_data.centredecongres is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(CentreDeCongres).filter(CentreDeCongres.gestionnaire_1_id == db_gestionnaire.id).update(
            {CentreDeCongres.gestionnaire_1_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if gestionnaire_data.centredecongres:
            # Validate that all IDs exist
            for centredecongres_id in gestionnaire_data.centredecongres:
                db_centredecongres = database.query(CentreDeCongres).filter(CentreDeCongres.id == centredecongres_id).first()
                if not db_centredecongres:
                    raise HTTPException(status_code=400, detail=f"CentreDeCongres with id {centredecongres_id} not found")

            # Update the related entities with the new foreign key
            database.query(CentreDeCongres).filter(CentreDeCongres.id.in_(gestionnaire_data.centredecongres)).update(
                {CentreDeCongres.gestionnaire_1_id: db_gestionnaire.id}, synchronize_session=False
            )
    if gestionnaire_data.reservation is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Reservation).filter(Reservation.gestionnaire_id == db_gestionnaire.id).update(
            {Reservation.gestionnaire_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if gestionnaire_data.reservation:
            # Validate that all IDs exist
            for reservation_id in gestionnaire_data.reservation:
                db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
                if not db_reservation:
                    raise HTTPException(status_code=400, detail=f"Reservation with id {reservation_id} not found")

            # Update the related entities with the new foreign key
            database.query(Reservation).filter(Reservation.id.in_(gestionnaire_data.reservation)).update(
                {Reservation.gestionnaire_id: db_gestionnaire.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_gestionnaire)

    centredecongres_ids = database.query(CentreDeCongres.id).filter(CentreDeCongres.gestionnaire_1_id == db_gestionnaire.id).all()
    reservation_ids = database.query(Reservation.id).filter(Reservation.gestionnaire_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "centredecongres_ids": [x[0] for x in centredecongres_ids],        "reservation_ids": [x[0] for x in reservation_ids]    }
    return response_data


@app.delete("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def delete_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)):
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")
    database.delete(db_gestionnaire)
    database.commit()
    return db_gestionnaire



############################################
#   Gestionnaire Method Endpoints
############################################




@app.post("/gestionnaire/{gestionnaire_id}/methods/seConnecter/", response_model=None, tags=["Gestionnaire Methods"])
async def execute_gestionnaire_seConnecter(
    gestionnaire_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the seConnecter method on a Gestionnaire instance.
    """
    # Retrieve the entity from the database
    _gestionnaire_object = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if _gestionnaire_object is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_gestionnaire_object):
            """Add your docstring here."""
            # Add your implementation here
            pass


        result = await wrapper(_gestionnaire_object)
        # Commit DB
        database.commit()
        database.refresh(_gestionnaire_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "gestionnaire_id": gestionnaire_id,
            "method": "seConnecter",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



