import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class StatutReservation(enum.Enum):
    ANNULEE = "ANNULEE"
    MODIFIEE = "MODIFIEE"
    EN_ATTENTE = "EN_ATTENTE"
    EXPIREE = "EXPIREE"
    CONFIRMEE = "CONFIRMEE"

class jourSemaine(enum.Enum):
    MARDI = "MARDI"
    JOUR_FERIE = "JOUR_FERIE"
    DIMANCHE = "DIMANCHE"
    LUNDI = "LUNDI"
    JEUDI = "JEUDI"
    SAMEDI = "SAMEDI"
    VENDREDI = "VENDREDI"
    MERCREDI = "MERCREDI"

class Saison(enum.Enum):
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"


# Tables definition for many-to-many relationships

# Tables definition
class RegleLocation(Base):
    __tablename__ = "reglelocation"
    id: Mapped[int] = mapped_column(primary_key=True)
    nbMinimum: Mapped[int] = mapped_column(Integer)
    dureeMinimale: Mapped[int] = mapped_column(Integer)
    materiel_2_id: Mapped[int] = mapped_column(ForeignKey("materiel.id"), unique=True)
    prestation_2_id: Mapped[int] = mapped_column(ForeignKey("prestation.id"), unique=True)

class Contraintes(Base):
    __tablename__ = "contraintes"
    id: Mapped[int] = mapped_column(primary_key=True)
    dureeMinimale: Mapped[int] = mapped_column(Integer)
    joursInterdits: Mapped[jourSemaine] = mapped_column(Enum(jourSemaine))
    elementcentre_3_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"), unique=True)

class Indisponibilte(Base):
    __tablename__ = "indisponibilte"
    id: Mapped[int] = mapped_column(primary_key=True)
    dateDebut: Mapped[dt_date] = mapped_column(Date)
    dateFin: Mapped[dt_date] = mapped_column(Date)
    motif: Mapped[str] = mapped_column(String(100))
    elementcentre_4_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"))

class Tarif(Base):
    __tablename__ = "tarif"
    id: Mapped[int] = mapped_column(primary_key=True)
    saison: Mapped[Saison] = mapped_column(Enum(Saison))
    prixParJour: Mapped[float] = mapped_column(Float)
    elementcentre_2_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"))

class PersonneReferente(Base):
    __tablename__ = "personnereferente"
    id: Mapped[int] = mapped_column(primary_key=True)
    prenom: Mapped[str] = mapped_column(String(100))
    mail: Mapped[str] = mapped_column(String(100))
    nom: Mapped[str] = mapped_column(String(100))

class Prestation(Base):
    __tablename__ = "prestation"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    estGlobale: Mapped[str] = mapped_column(String(100))
    nbMaxParticipant: Mapped[int] = mapped_column(Integer)
    centredecongres_3_id: Mapped[int] = mapped_column(ForeignKey("centredecongres.id"))
    reservation_5_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"))

class Materiel(Base):
    __tablename__ = "materiel"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    quantiteDisponible: Mapped[str] = mapped_column(String(100))
    reservation_4_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"))
    centredecongres_2_id: Mapped[int] = mapped_column(ForeignKey("centredecongres.id"))

class ElementCentre(Base):
    __tablename__ = "elementcentre"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    capaciteMax: Mapped[int] = mapped_column(Integer)
    reservation_3_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"))
    centredecongres_1_id: Mapped[int] = mapped_column(ForeignKey("centredecongres.id"))

class Evenement(Base):
    __tablename__ = "evenement"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    nbParticipantPrevus: Mapped[int] = mapped_column(Integer)
    personnereferente_id: Mapped[int] = mapped_column(ForeignKey("personnereferente.id"), unique=True)
    reservation_2_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), unique=True)

class Paiement(Base):
    __tablename__ = "paiement"
    id: Mapped[int] = mapped_column(primary_key=True)
    montant: Mapped[float] = mapped_column(Float)
    dateTransaction: Mapped[dt_date] = mapped_column(Date)
    reference: Mapped[str] = mapped_column(String(100))
    reservation_1_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), unique=True)

class CentreDeCongres(Base):
    __tablename__ = "centredecongres"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    adresse: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    gestionnaire_1_id: Mapped[int] = mapped_column(ForeignKey("gestionnaire.id"))

class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    dateCreation: Mapped[dt_date] = mapped_column(Date)
    dateDebut: Mapped[dt_date] = mapped_column(Date)
    dateFin: Mapped[dt_date] = mapped_column(Date)
    delaiDeConfirmation: Mapped[int] = mapped_column(Integer)
    coutTotal: Mapped[float] = mapped_column(Float)
    Statut: Mapped[StatutReservation] = mapped_column(Enum(StatutReservation))
    tarif_id: Mapped[int] = mapped_column(ForeignKey("tarif.id"), unique=True)
    gestionnaire_id: Mapped[int] = mapped_column(ForeignKey("gestionnaire.id"))

class Gestionnaire(Base):
    __tablename__ = "gestionnaire"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    motDePass: Mapped[str] = mapped_column(String(100))


#--- Relationships of the reglelocation table
RegleLocation.materiel_2: Mapped["Materiel"] = relationship("Materiel", back_populates="reglelocation", foreign_keys=[RegleLocation.materiel_2_id])
RegleLocation.prestation_2: Mapped["Prestation"] = relationship("Prestation", back_populates="reglelocation_1", foreign_keys=[RegleLocation.prestation_2_id])

#--- Relationships of the contraintes table
Contraintes.elementcentre_3: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="contraintes", foreign_keys=[Contraintes.elementcentre_3_id])

#--- Relationships of the indisponibilte table
Indisponibilte.elementcentre_4: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="indisponibilte", foreign_keys=[Indisponibilte.elementcentre_4_id])

#--- Relationships of the tarif table
Tarif.reservation_6: Mapped["Reservation"] = relationship("Reservation", back_populates="tarif", foreign_keys=[Reservation.tarif_id])
Tarif.elementcentre_2: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="tarif_1", foreign_keys=[Tarif.elementcentre_2_id])

#--- Relationships of the personnereferente table
PersonneReferente.evenement_1: Mapped["Evenement"] = relationship("Evenement", back_populates="personnereferente", foreign_keys=[Evenement.personnereferente_id])

#--- Relationships of the prestation table
Prestation.centredecongres_3: Mapped["CentreDeCongres"] = relationship("CentreDeCongres", back_populates="prestation_1", foreign_keys=[Prestation.centredecongres_3_id])
Prestation.reservation_5: Mapped["Reservation"] = relationship("Reservation", back_populates="prestation", foreign_keys=[Prestation.reservation_5_id])
Prestation.reglelocation_1: Mapped["RegleLocation"] = relationship("RegleLocation", back_populates="prestation_2", foreign_keys=[RegleLocation.prestation_2_id])

#--- Relationships of the materiel table
Materiel.reservation_4: Mapped["Reservation"] = relationship("Reservation", back_populates="materiel", foreign_keys=[Materiel.reservation_4_id])
Materiel.centredecongres_2: Mapped["CentreDeCongres"] = relationship("CentreDeCongres", back_populates="materiel_1", foreign_keys=[Materiel.centredecongres_2_id])
Materiel.reglelocation: Mapped["RegleLocation"] = relationship("RegleLocation", back_populates="materiel_2", foreign_keys=[RegleLocation.materiel_2_id])

#--- Relationships of the elementcentre table
ElementCentre.indisponibilte: Mapped[List["Indisponibilte"]] = relationship("Indisponibilte", back_populates="elementcentre_4", foreign_keys=[Indisponibilte.elementcentre_4_id])
ElementCentre.contraintes: Mapped["Contraintes"] = relationship("Contraintes", back_populates="elementcentre_3", foreign_keys=[Contraintes.elementcentre_3_id])
ElementCentre.tarif_1: Mapped[List["Tarif"]] = relationship("Tarif", back_populates="elementcentre_2", foreign_keys=[Tarif.elementcentre_2_id])
ElementCentre.reservation_3: Mapped["Reservation"] = relationship("Reservation", back_populates="elementcentre", foreign_keys=[ElementCentre.reservation_3_id])
ElementCentre.centredecongres_1: Mapped["CentreDeCongres"] = relationship("CentreDeCongres", back_populates="elementcentre_1", foreign_keys=[ElementCentre.centredecongres_1_id])

#--- Relationships of the evenement table
Evenement.personnereferente: Mapped["PersonneReferente"] = relationship("PersonneReferente", back_populates="evenement_1", foreign_keys=[Evenement.personnereferente_id])
Evenement.reservation_2: Mapped["Reservation"] = relationship("Reservation", back_populates="evenement", foreign_keys=[Evenement.reservation_2_id])

#--- Relationships of the paiement table
Paiement.reservation_1: Mapped["Reservation"] = relationship("Reservation", back_populates="paiement", foreign_keys=[Paiement.reservation_1_id])

#--- Relationships of the centredecongres table
CentreDeCongres.gestionnaire_1: Mapped["Gestionnaire"] = relationship("Gestionnaire", back_populates="centredecongres", foreign_keys=[CentreDeCongres.gestionnaire_1_id])
CentreDeCongres.prestation_1: Mapped[List["Prestation"]] = relationship("Prestation", back_populates="centredecongres_3", foreign_keys=[Prestation.centredecongres_3_id])
CentreDeCongres.materiel_1: Mapped[List["Materiel"]] = relationship("Materiel", back_populates="centredecongres_2", foreign_keys=[Materiel.centredecongres_2_id])
CentreDeCongres.elementcentre_1: Mapped[List["ElementCentre"]] = relationship("ElementCentre", back_populates="centredecongres_1", foreign_keys=[ElementCentre.centredecongres_1_id])

#--- Relationships of the reservation table
Reservation.paiement: Mapped["Paiement"] = relationship("Paiement", back_populates="reservation_1", foreign_keys=[Paiement.reservation_1_id])
Reservation.tarif: Mapped["Tarif"] = relationship("Tarif", back_populates="reservation_6", foreign_keys=[Reservation.tarif_id])
Reservation.evenement: Mapped["Evenement"] = relationship("Evenement", back_populates="reservation_2", foreign_keys=[Evenement.reservation_2_id])
Reservation.elementcentre: Mapped[List["ElementCentre"]] = relationship("ElementCentre", back_populates="reservation_3", foreign_keys=[ElementCentre.reservation_3_id])
Reservation.materiel: Mapped[List["Materiel"]] = relationship("Materiel", back_populates="reservation_4", foreign_keys=[Materiel.reservation_4_id])
Reservation.gestionnaire: Mapped["Gestionnaire"] = relationship("Gestionnaire", back_populates="reservation", foreign_keys=[Reservation.gestionnaire_id])
Reservation.prestation: Mapped[List["Prestation"]] = relationship("Prestation", back_populates="reservation_5", foreign_keys=[Prestation.reservation_5_id])

#--- Relationships of the gestionnaire table
Gestionnaire.centredecongres: Mapped[List["CentreDeCongres"]] = relationship("CentreDeCongres", back_populates="gestionnaire_1", foreign_keys=[CentreDeCongres.gestionnaire_1_id])
Gestionnaire.reservation: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="gestionnaire", foreign_keys=[Reservation.gestionnaire_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)