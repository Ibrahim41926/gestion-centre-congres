from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class StatutReservation(Enum):
    ANNULEE = "ANNULEE"
    MODIFIEE = "MODIFIEE"
    EN_ATTENTE = "EN_ATTENTE"
    EXPIREE = "EXPIREE"
    CONFIRMEE = "CONFIRMEE"

class jourSemaine(Enum):
    MARDI = "MARDI"
    JOUR_FERIE = "JOUR_FERIE"
    DIMANCHE = "DIMANCHE"
    LUNDI = "LUNDI"
    JEUDI = "JEUDI"
    SAMEDI = "SAMEDI"
    VENDREDI = "VENDREDI"
    MERCREDI = "MERCREDI"

class Saison(Enum):
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"

############################################
# Classes are defined here
############################################
class RegleLocationCreate(BaseModel):
    dureeMinimale: int
    nbMinimum: int
    prestation_2: int  # 1:1 Relationship (mandatory)
    materiel_2: int  # 1:1 Relationship (mandatory)


class ContraintesCreate(BaseModel):
    joursInterdits: jourSemaine
    dureeMinimale: int
    elementcentre_3: int  # 1:1 Relationship (mandatory)


class IndisponibilteCreate(BaseModel):
    dateFin: date
    dateDebut: date
    motif: str
    elementcentre_4: int  # N:1 Relationship (mandatory)


class TarifCreate(BaseModel):
    saison: Saison
    prixParJour: float
    elementcentre_2: int  # N:1 Relationship (mandatory)


class PersonneReferenteCreate(BaseModel):
    nom: str
    prenom: str
    mail: str


class PrestationCreate(BaseModel):
    nom: str
    estGlobale: str
    nbMaxParticipant: int
    description: str
    reglelocation_1: Optional[int] = None  # 1:1 Relationship (optional)
    centredecongres_3: int  # N:1 Relationship (mandatory)


class MaterielCreate(BaseModel):
    nom: str
    quantiteDisponible: str
    description: str
    centredecongres_2: int  # N:1 Relationship (mandatory)
    reglelocation: Optional[int] = None  # 1:1 Relationship (optional)


class ElementCentreCreate(BaseModel):
    description: str
    nom: str
    capaciteMax: int
    centredecongres_1: int  # N:1 Relationship (mandatory)
    contraintes: Optional[int] = None  # 1:1 Relationship (optional)
    indisponibilte: Optional[List[int]] = None  # 1:N Relationship
    tarif_1: Optional[List[int]] = None  # 1:N Relationship


class EvenementCreate(BaseModel):
    nom: str
    nbParticipantPrevus: int
    description: str
    personnereferente: int  # 1:1 Relationship (mandatory)


class PaiementCreate(BaseModel):
    reference: str
    dateTransaction: date
    montant: float


class CentreDeCongresCreate(BaseModel):
    adresse: str
    description: str
    nom: str
    materiel_1: Optional[List[int]] = None  # 1:N Relationship
    prestation_1: Optional[List[int]] = None  # 1:N Relationship
    elementcentre_1: Optional[List[int]] = None  # 1:N Relationship


class ReservationCreate(BaseModel):
    dateCreation: date
    coutTotal: float
    dateFin: date
    dateDebut: date
    Statut: StatutReservation
    delaiDeConfirmation: int
    materiel: Optional[List[int]] = None  # 1:N Relationship
    prestation: Optional[List[int]] = None  # 1:N Relationship
    elementcentre: Optional[List[int]] = None  # 1:N Relationship
    evenement: int  # 1:1 Relationship (mandatory)
    paiement: Optional[int] = None  # 1:1 Relationship (optional)
    tarif: int  # 1:1 Relationship (mandatory)


class GestionnaireCreate(BaseModel):
    motDePass: str
    nom: str
    prenom: str
    email: str
    centredecongres: Optional[List[int]] = None  # 1:N Relationship
    reservation: Optional[List[int]] = None  # 1:N Relationship


