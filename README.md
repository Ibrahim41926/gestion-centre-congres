# Gestion Centre de Congres

Application web de gestion d'un centre de congres avec interface d'administration, backend REST et base SQLite. Le projet permet de gerer les reservations, evenements, prestations, materiels, contraintes, paiements et les principales entites metier du centre.

## Apercu

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + SQLAlchemy
- Base de donnees: SQLite
- Documentation API: `http://localhost:8000/docs`

## Fonctionnalites

- Gestion des gestionnaires
- Gestion des centres de congres et de leurs elements
- Gestion des reservations et des evenements
- Gestion du materiel, des prestations et des contraintes
- Gestion des tarifs, paiements et indisponibilites
- API REST CRUD auto-generee pour les entites metier

## Structure du projet

```text
.
├── web_app_output/
│   ├── backend/         # API FastAPI + SQLAlchemy
│   ├── frontend/        # Interface React + Vite
│   └── docker-compose.yml
├── CapturesDeL'interface de L'app/   # Captures d'ecran de l'application
├── Diagramme de classe/
├── Diagramme de cas d'utilisation/
├── Diagramme de sequence/
├── Diagramme d'etat/
└── Diagramme d'objet/
```

## Lancement en local

### 1. Backend

```bash
cd web_app_output/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main_api.py
```

API disponible sur `http://localhost:8000`  
Documentation Swagger sur `http://localhost:8000/docs`

### 2. Frontend

```bash
cd web_app_output/frontend
npm install
npm run dev
```

Interface disponible sur `http://localhost:3000`

### 3. Avec Docker

```bash
cd web_app_output
docker-compose up --build
```

## Entites principales

- `Gestionnaire`
- `CentreDeCongres`
- `ElementCentre`
- `Reservation`
- `Evenement`
- `Materiel`
- `Prestation`
- `Contraintes`
- `Tarif`
- `Paiement`
- `PersonneReferente`
- `Indisponibilte`
- `RegleLocation`

## Captures de l'interface

### Tableau de bord gestionnaire

<img src="./CapturesDeL'interface de L'app/Interface gestionnaire.png" alt="Interface gestionnaire" width="900" />

Cette interface sert de point d'entree pour l'administration. Elle permet au gestionnaire de consulter les donnees, naviguer entre les modules metier et lancer les operations principales de gestion.

### Centre de congres

<img src="./CapturesDeL'interface de L'app/centre de congres.png" alt="Centre de congres" width="900" />

Cette vue permet de gerer les informations du centre de congres: identification du centre, configuration generale et consultation des donnees associees a sa structure.

### Evenements

<img src="./CapturesDeL'interface de L'app/Interface Evenement.png" alt="Interface evenement" width="900" />

Cette page est utilisee pour consulter, ajouter, modifier ou supprimer les evenements organises dans le centre. Elle centralise les informations utiles au suivi des activites planifiees.

### Elements du centre

<img src="./CapturesDeL'interface de L'app/interface element centre.png" alt="Interface element centre" width="900" />

Cette interface affiche les elements constitutifs du centre, par exemple les espaces ou ressources internes. Elle aide a structurer le centre et a rattacher les reservations aux bons elements.

### Contraintes et elements

<img src="./CapturesDeL'interface de L'app/interface contrainte element.png" alt="Interface contraintes et element" width="900" />

Cette vue permet de definir et visualiser les contraintes appliquees aux elements du centre. Elle sert a controler les regles d'utilisation, les limitations et les conditions de reservation.

### Reservations et elements

<img src="./CapturesDeL'interface de L'app/interface reservation element.png" alt="Interface reservation element" width="900" />

Cette page permet d'associer une reservation aux elements du centre concernes. Elle facilite la planification des espaces reserves pour un evenement ou une activite.

### Reservations et materiel

<img src="./CapturesDeL'interface de L'app/interface reservation materiel.png" alt="Interface reservation materiel" width="900" />

Cette interface sert a rattacher du materiel a une reservation. Elle permet de suivre les besoins logistiques et de preparer les ressources necessaires pour chaque reservation.

### Materiel

<img src="./CapturesDeL'interface de L'app/interface materiel.png" alt="Interface materiel" width="900" />

Cette vue est dediee a la gestion du materiel disponible dans le centre. On peut y consulter les equipements, leur etat et leur disponibilite pour les futures reservations.

### Reservations et prestations

<img src="./CapturesDeL'interface de L'app/ace reservation prestation.png" alt="Interface reservation prestation" width="900" />

Cette page permet d'associer des prestations a une reservation, par exemple des services complementaires. Elle aide a construire une offre complete en fonction des besoins du client ou de l'evenement.

## Diagrammes UML

### Diagramme de classe

<img src="./Diagramme de classe/Diagramme de classe.png" alt="Diagramme de classe" width="900" />

Le diagramme de classe presente la structure statique du systeme. Il montre les principales classes metier comme `Reservation`, `CentreDeCongres`, `Evenement`, `Materiel`, `Prestation` et `Gestionnaire`, ainsi que leurs attributs, associations et dependances. Il sert a comprendre l'organisation globale de l'application et la facon dont les entites collaborent entre elles.

### Diagramme de cas d'utilisation

<img src="./Diagramme de cas d'utilisation/Diagramme de cas d'utlisation.png" alt="Diagramme de cas d'utilisation" width="900" />

Ce diagramme decrit les interactions entre les acteurs et le systeme. Il met en evidence les fonctionnalites offertes, comme configurer un centre, creer ou confirmer une reservation, consulter des disponibilites ou suivre des statistiques.

### Diagramme d'etat

<img src="./Diagramme d'etat/Diagramme d'etats.png" alt="Diagramme d'etat" width="900" />

Le diagramme d'etat explique le cycle de vie d'une reservation ou d'un objet metier similaire. Il montre les transitions possibles entre les differents etats, par exemple la creation, la confirmation, l'annulation ou les cas de blocage selon les regles de gestion.

### Diagrammes de sequence

#### Creer une reservation

<img src="./Diagramme de sequence/Creerne reservation Diagramme de sequence.png" alt="Diagramme de sequence creation reservation" width="900" />

Ce diagramme montre l'enchainement des messages lors de la creation d'une reservation. Il precise l'ordre des appels entre l'utilisateur, l'interface, la logique metier et les donnees persistantes.

#### Confirmer une reservation

<img src="./Diagramme de sequence/Confirmer une reservation Diagramme de sequence.png" alt="Diagramme de sequence confirmation reservation" width="900" />

Ce diagramme detaille le processus de confirmation d'une reservation. Il aide a visualiser les verifications, les validations et les mises a jour declenchees au moment de la confirmation.

#### Annuler une reservation

<img src="./Diagramme de sequence/Annuler une reservation Diagramme de sequence.png" alt="Diagramme de sequence annulation reservation" width="900" />

Ce diagramme decrit les interactions necessaires pour annuler une reservation. Il met en avant les controles a effectuer, les regles de delai et l'impact sur l'etat de la reservation.

### Diagrammes d'objet

#### Scenario 1 - Configurer un centre de congres

<img src="./Diagramme d'objet/Scénario 1 — Configurer un centre de congrès DO.png" alt="Diagramme d'objet scenario 1" width="900" />

Ce diagramme d'objet illustre un instant precis du systeme pendant la configuration d'un centre de congres. Il montre des instances concretes et les liens reels entre les objets concernes.

#### Scenario 2 - Creer une reservation

<img src="./Diagramme d'objet/Scénario 2 — Créer une réservation DO.png" alt="Diagramme d'objet scenario 2" width="900" />

Ce schema represente les objets manipules lors de la creation d'une reservation. Il permet de voir quelles donnees sont instanciees et comment elles sont reliees au moment de l'action.

#### Scenario 3 - Confirmer une reservation

<img src="./Diagramme d'objet/Scénario 3 — Confirmer une réservation DO.png" alt="Diagramme d'objet scenario 3" width="900" />

Ce diagramme montre l'etat concret des objets apres ou pendant la confirmation d'une reservation. Il aide a verifier la coherence des relations entre reservation, gestionnaire et ressources associees.

#### Scenario 4 - Annuler une reservation apres delai

<img src="./Diagramme d'objet/Scenario 4 Annuler une reservation apres delai DO.png" alt="Diagramme d'objet scenario 4" width="900" />

Ce diagramme met en scene le cas d'annulation apres depassement d'un delai. Il sert a visualiser l'effet des regles metier sur les objets deja engages dans le processus de reservation.

#### Scenario 5 - Consulter les disponibilites

<img src="./Diagramme d'objet/Scenario 5 Consulter disponibiltés.png" alt="Diagramme d'objet scenario 5" width="900" />

Ce diagramme represente les objets mobilises pour consulter les disponibilites. Il montre les informations necessaires pour determiner si un espace ou une ressource peut etre reserve.

#### Scenario 6 - Consulter les statistiques

<img src="./Diagramme d'objet/Scenario 6 Consulter stats.png" alt="Diagramme d'objet scenario 6" width="900" />

Ce diagramme illustre les objets utilises pour produire des statistiques de gestion. Il permet de comprendre quelles entites alimentent les indicateurs et les vues de synthese.

## Notes

- Le backend initialise automatiquement la base SQLite dans `web_app_output/backend/data/Class_Diagram.db`.
- Le frontend consomme l'API via la variable `VITE_API_URL`.
- Le projet contient egalement plusieurs diagrammes UML pour documenter le domaine metier et la conception.
