# Gestion d'un Centre de Congres

## Presentation du projet

Ce depot contient une application web de gestion d'un centre de congres. Elle permet d'administrer les principales ressources du centre, d'organiser les reservations, de suivre les evenements, de gerer les prestations et le materiel, puis de manipuler les donnees metier via une interface web et une API REST.

L'application a ete generee avec l'outil **BESSER** dans le cadre d'un **projet academique realise en binome**. Le travail s'appuie sur une demarche de modelisation UML, suivie d'une generation assistee de l'architecture logicielle, puis d'une phase d'adaptation et d'exploitation de l'application produite.

L'objectif global du projet est de proposer une solution centralisee pour la gestion d'un centre de congres, en structurant les donnees autour des reservations, des espaces, des equipements, des contraintes et des interactions entre les differents acteurs du systeme.

## Objectifs academiques

Ce projet a ete concu pour repondre a plusieurs objectifs pedagogiques :

- modeliser un besoin metier reel a l'aide de diagrammes UML ;
- identifier les acteurs, les cas d'utilisation et les regles de gestion ;
- concevoir les relations entre les entites du domaine ;
- generer une application a partir d'un modele avec BESSER ;
- manipuler une architecture separee en frontend et backend ;
- produire une documentation claire pour presenter le travail realise.

## Apercu technique

- **Frontend** : React + TypeScript + Vite
- **Backend** : FastAPI + SQLAlchemy
- **Base de donnees** : SQLite
- **Generation du projet** : BESSER
- **Documentation API** : `http://localhost:8000/docs`
- **Orchestration possible** : Docker Compose

## Description fonctionnelle

L'application couvre plusieurs besoins de gestion lies au fonctionnement d'un centre de congres.

Elle permet notamment :

- de gerer les gestionnaires responsables du systeme ;
- de definir un ou plusieurs centres de congres ;
- d'administrer les elements composant le centre ;
- d'enregistrer et suivre des reservations ;
- d'associer des evenements aux reservations ;
- de rattacher du materiel et des prestations aux reservations ;
- de gerer les contraintes, les regles de location et les indisponibilites ;
- de suivre certains objets de gestion comme les tarifs, paiements et personnes referentes ;
- d'exposer toutes ces donnees a travers une API REST CRUD.

## Architecture du projet

Le projet est organise autour de deux parties principales :

- un **frontend** qui fournit l'interface utilisateur pour consulter et manipuler les donnees ;
- un **backend** qui expose l'API REST, applique la logique de persistence et gere la base de donnees.

Le backend est construit avec FastAPI et SQLAlchemy. Il genere des points d'entree CRUD pour les entites metier principales et initialise automatiquement une base SQLite locale.

Le frontend est construit avec React, TypeScript et Vite. Il propose plusieurs pages, chacune associee a une entite ou a un ensemble fonctionnel du domaine, afin de faciliter la navigation et la gestion des donnees.

## Structure du depot

```text
.
├── web_app_output/
│   ├── backend/                         # API FastAPI + logique de persistence SQLAlchemy
│   ├── frontend/                        # Interface web React + TypeScript + Vite
│   └── docker-compose.yml               # Lancement conteneurise du frontend et du backend
├── CapturesDeL'interface de L'app/      # Captures d'ecran de l'application
├── Diagramme de classe/                 # Diagramme de classe UML
├── Diagramme de cas d'utilisation/      # Diagramme de cas d'utilisation UML
├── Diagramme de sequence/               # Diagrammes de sequence UML
├── Diagramme d'etat/                    # Diagramme d'etat UML
└── Diagramme d'objet/                   # Diagrammes d'objet UML
```

## Installation et execution

### Prerequis

Avant de lancer le projet, il faut disposer de :

- Python 3.11 ou version compatible ;
- Node.js 20 ou version compatible ;
- npm ;
- Docker et Docker Compose si vous souhaitez un lancement conteneurise.

## Lancement en local

### 1. Lancer le backend

Depuis le dossier `web_app_output/backend` :

```bash
cd web_app_output/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main_api.py
```

Une fois demarre, le backend est accessible a l'adresse :

- API : `http://localhost:8000`
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

### 2. Lancer le frontend

Depuis le dossier `web_app_output/frontend` :

```bash
cd web_app_output/frontend
npm install
npm run dev
```

Le frontend est alors disponible sur :

- Interface web : `http://localhost:3000`

### 3. Lancer le projet avec Docker

Depuis le dossier `web_app_output` :

```bash
cd web_app_output
docker-compose up --build
```

Cette commande permet de lancer le frontend et le backend dans des conteneurs, avec une configuration prete a l'emploi.

## Configuration

Le projet utilise notamment les variables suivantes :

- `DATABASE_URL` pour definir l'emplacement de la base de donnees du backend ;
- `VITE_API_URL` pour indiquer au frontend l'URL de l'API.

Par defaut :

- le backend initialise une base SQLite dans `web_app_output/backend/data/Class_Diagram.db` ;
- le frontend consomme l'API sur `http://localhost:8000`.

## Entites metier principales

Le domaine metier du projet repose sur plusieurs entites importantes :

- `Gestionnaire` : represente l'utilisateur ou responsable qui administre le systeme ;
- `CentreDeCongres` : represente la structure principale a gerer ;
- `ElementCentre` : represente un element composant le centre, comme un espace ou une ressource structurelle ;
- `Reservation` : represente une demande ou une operation de reservation ;
- `Evenement` : represente l'activite ou l'evenement organise dans le centre ;
- `Materiel` : represente les equipements mobilisables ;
- `Prestation` : represente les services associes a une reservation ;
- `Contraintes` : represente les regles ou restrictions applicables ;
- `Tarif` : represente les informations de cout ou de tarification ;
- `Paiement` : represente le suivi financier lie a certaines operations ;
- `PersonneReferente` : represente un contact associe a une reservation ou un contexte de gestion ;
- `Indisponibilte` : represente une periode ou une ressource non disponible ;
- `RegleLocation` : represente une regle appliquee au processus de location ou de reservation.

## API REST

Le backend expose une API REST generee autour des entites metier. Pour chaque entite, on retrouve generalement :

- des routes de consultation ;
- des routes de creation ;
- des routes de modification ;
- des routes de suppression ;
- parfois des routes de comptage, de pagination ou de gestion des relations.

Cette API sert de couche de communication entre l'interface frontend et la base de donnees. Elle peut egalement etre testee directement depuis Swagger via `http://localhost:8000/docs`.

## Captures de l'interface

Les captures suivantes illustrent plusieurs ecrans significatifs de l'application. Elles permettent de visualiser concretement les modules disponibles et leur role fonctionnel.

### Interface gestionnaire

<img src="./CapturesDeL'interface de L'app/Interface gestionnaire.png" alt="Interface gestionnaire" width="900" />

Cette interface correspond a un ecran de gestion lie au profil du gestionnaire. Elle joue un role central dans l'administration de l'application, car elle donne acces aux donnees principales, aux operations de consultation et aux differents modules metier. Dans le cadre du projet, cet ecran symbolise la partie pilotage du systeme, c'est-a-dire l'endroit depuis lequel un responsable peut naviguer, controler les informations et organiser les actions de gestion.

### Interface centre de congres

<img src="./CapturesDeL'interface de L'app/centre de congres.png" alt="Centre de congres" width="900" />

Cette vue permet de manipuler les informations generales associees au centre de congres. Elle sert a representer la structure principale autour de laquelle s'articulent les autres entites du domaine. On y retrouve typiquement les donnees d'identification, les informations de structure et les liaisons avec d'autres objets metier. Cette page est importante car elle ancre le modele dans son contexte reel : toutes les reservations, ressources et contraintes gravitent autour du centre.

### Interface evenement

<img src="./CapturesDeL'interface de L'app/Interface Evenement.png" alt="Interface evenement" width="900" />

Cette page est dediee a la gestion des evenements. Elle permet de consulter les evenements existants, d'en ajouter de nouveaux et d'assurer leur suivi. Dans une application de centre de congres, l'evenement constitue souvent la finalite de la reservation : un espace n'est pas reserve de maniere abstraite, il l'est pour accueillir une activite, une conference, une reunion ou toute autre manifestation. Cet ecran sert donc a structurer ces usages.

### Interface element du centre

<img src="./CapturesDeL'interface de L'app/interface element centre.png" alt="Interface element centre" width="900" />

Cette interface est consacree aux elements composant le centre de congres. Ces elements peuvent representer des salles, zones, espaces ou composants internes utiles a l'organisation du centre. Leur gestion est essentielle, car une reservation porte souvent sur des elements precis. Cet ecran facilite donc la description des ressources structurelles disponibles et leur rattachement au reste du systeme.

### Interface contraintes sur les elements

<img src="./CapturesDeL'interface de L'app/interface contrainte element.png" alt="Interface contraintes et element" width="900" />

Cette vue illustre la gestion des contraintes appliquees aux elements du centre. Les contraintes permettent d'introduire des regles de gestion realistes : limitation d'usage, incompatibilites, capacites, restrictions temporelles ou obligations specifiques. Cette partie est importante dans un projet academique de modelisation, car elle montre que le systeme ne se limite pas a stocker des donnees, mais qu'il prend aussi en compte les conditions qui encadrent leur utilisation.

### Interface reservation et elements

<img src="./CapturesDeL'interface de L'app/interface reservation element.png" alt="Interface reservation element" width="900" />

Cette capture montre la relation entre les reservations et les elements du centre. Elle permet de comprendre comment une reservation mobilise concretement certaines ressources du centre. Cette page rend visible l'association entre la demande utilisateur et les espaces concernes. Elle aide ainsi a eviter les conflits d'affectation et a assurer une meilleure organisation des ressources.

### Interface reservation et materiel

<img src="./CapturesDeL'interface de L'app/interface reservation materiel.png" alt="Interface reservation materiel" width="900" />

Cette interface traite l'association entre une reservation et le materiel necessaire. Dans un centre de congres, il ne suffit pas de reserver un espace ; il faut aussi pouvoir mobiliser les equipements adaptes, comme du mobilier, du materiel technique ou des ressources logistiques. Cet ecran montre donc comment l'application relie les besoins operationnels d'une reservation aux moyens materiels disponibles.

### Interface materiel

<img src="./CapturesDeL'interface de L'app/interface materiel.png" alt="Interface materiel" width="900" />

Cette page est consacree a la gestion du materiel disponible. Elle permet de centraliser les equipements du centre, d'en suivre l'existence et de les associer ensuite aux reservations. Dans la logique metier du projet, le materiel joue un role complementaire a celui des espaces : il contribue directement a la qualite et a la faisabilite d'un evenement. Cet ecran aide donc a maintenir une vision claire des ressources mobilisables.

### Interface reservation et prestations

<img src="./CapturesDeL'interface de L'app/ace reservation prestation.png" alt="Interface reservation prestation" width="900" />

Cette vue permet d'associer des prestations a une reservation. Les prestations representent des services complementaires qui enrichissent l'offre du centre de congres, par exemple des services techniques, logistiques ou organisationnels. Cette fonctionnalite donne une dimension plus complete a l'application, car elle montre que la gestion ne porte pas uniquement sur des ressources physiques, mais aussi sur des services fournis autour de l'evenement.

## Diagrammes UML

Les diagrammes UML constituent une partie essentielle du projet. Ils permettent de presenter la conception fonctionnelle et structurelle du systeme, tout en montrant la demarche de modelisation suivie avant ou pendant la generation de l'application avec BESSER.

### Diagramme de classe

<img src="./Diagramme de classe/Diagramme de classe.png" alt="Diagramme de classe" width="900" />

Le diagramme de classe decrit la structure statique du systeme. Il met en evidence les classes metier principales, leurs attributs, leurs associations et la nature des relations qui les unissent. Dans ce projet, il permet de comprendre comment des classes comme `Reservation`, `CentreDeCongres`, `Evenement`, `Gestionnaire`, `Materiel`, `Prestation` ou `Contraintes` s'articulent entre elles.

Il s'agit d'un diagramme fondamental, car il sert de base a la comprehension globale du domaine metier. Il montre :

- quelles sont les entites principales du systeme ;
- quelles informations chaque entite transporte ;
- quelles dependances existent entre les objets ;
- comment la logique de reservation est reliee aux espaces, aux services et aux ressources.

Dans le cadre du projet academique, ce diagramme joue aussi un role methodologique fort : il traduit la conceptualisation du probleme avant son implementation, puis sert de support a la generation de l'application via BESSER.

### Diagramme de cas d'utilisation

<img src="./Diagramme de cas d'utilisation/Diagramme de cas d'utlisation.png" alt="Diagramme de cas d'utilisation" width="900" />

Le diagramme de cas d'utilisation presente le systeme du point de vue des acteurs. Il met l'accent sur les fonctionnalites offertes et sur les interactions possibles avec l'application. Il permet de visualiser les grands services rendus par le systeme, comme la configuration du centre, la creation d'une reservation, la confirmation d'une reservation, l'annulation d'une reservation, la consultation des disponibilites ou encore le suivi statistique.

Ce diagramme est important, car il donne une lecture fonctionnelle du projet. Il repond a la question : **qu'est-ce que le systeme doit permettre de faire ?**

### Diagramme d'etat

<img src="./Diagramme d'etat/Diagramme d'etats.png" alt="Diagramme d'etat" width="900" />

Le diagramme d'etat montre l'evolution d'un objet au cours de son cycle de vie. Dans ce projet, il est particulierement utile pour comprendre les changements d'etat lies au processus de reservation. Il permet de suivre les transitions possibles entre differentes situations, comme la creation, la confirmation, l'annulation ou les cas conditionnes par certaines regles metier.

Ce diagramme apporte une vision dynamique complementaire au diagramme de classe. Il montre non seulement quelles sont les entites du systeme, mais aussi comment elles evoluent dans le temps.

### Diagrammes de sequence

Les diagrammes de sequence decrivent l'ordre chronologique des interactions entre les acteurs, l'interface et les composants metier. Ils sont utiles pour comprendre le deroulement exact d'un scenario.

#### Creation d'une reservation

<img src="./Diagramme de sequence/Creerne reservation Diagramme de sequence.png" alt="Diagramme de sequence creation reservation" width="900" />

Ce diagramme detaille le scenario de creation d'une reservation. Il montre les messages echanges entre les differents participants du systeme et l'ordre dans lequel les actions sont executees. Il aide a comprendre comment une demande initiale devient une reservation effectivement enregistree dans le systeme.

#### Confirmation d'une reservation

<img src="./Diagramme de sequence/Confirmer une reservation Diagramme de sequence.png" alt="Diagramme de sequence confirmation reservation" width="900" />

Ce diagramme de sequence illustre les etapes necessaires a la confirmation d'une reservation. Il met en lumiere les verifications, les validations et les mises a jour qui transforment une reservation en une reservation confirmee. Il est particulierement utile pour visualiser les points de controle metier.

#### Annulation d'une reservation

<img src="./Diagramme de sequence/Annuler une reservation Diagramme de sequence.png" alt="Diagramme de sequence annulation reservation" width="900" />

Ce diagramme montre le deroulement d'une annulation. Il decrit comment le systeme reagit a cette action, quelles verifications sont effectuees et comment l'etat final de la reservation est impacte. Il permet de mieux comprendre la gestion des exceptions ou des cas particuliers lies au temps ou aux regles de gestion.

### Diagrammes d'objet

Les diagrammes d'objet offrent une photographie concrete du systeme a un instant donne. Contrairement au diagramme de classe, qui reste abstrait, ils montrent des instances reelles et les liens effectifs entre elles dans des scenarios precis.

#### Scenario 1 - Configurer un centre de congres

<img src="./Diagramme d'objet/Scénario 1 — Configurer un centre de congrès DO.png" alt="Diagramme d'objet scenario 1" width="900" />

Ce diagramme illustre les objets mobilises lorsqu'on configure un centre de congres. Il permet de voir quelles instances sont impliquees et comment elles sont reliees au moment de la mise en place de la structure generale du centre.

#### Scenario 2 - Creer une reservation

<img src="./Diagramme d'objet/Scénario 2 — Créer une réservation DO.png" alt="Diagramme d'objet scenario 2" width="900" />

Ce diagramme represente un etat concret du systeme pendant la creation d'une reservation. Il montre les objets instancies a ce moment-la et la maniere dont la reservation s'insere dans l'ensemble du modele.

#### Scenario 3 - Confirmer une reservation

<img src="./Diagramme d'objet/Scénario 3 — Confirmer une réservation DO.png" alt="Diagramme d'objet scenario 3" width="900" />

Ce schema montre les objets presents lors de la confirmation d'une reservation. Il permet de mieux comprendre quelles relations doivent deja exister pour que l'operation soit coherente et completement validee.

#### Scenario 4 - Annuler une reservation apres delai

<img src="./Diagramme d'objet/Scenario 4 Annuler une reservation apres delai DO.png" alt="Diagramme d'objet scenario 4" width="900" />

Ce diagramme correspond a un cas plus specifique : l'annulation d'une reservation apres depassement d'un delai. Il permet d'illustrer l'impact des regles metier sur les objets du systeme dans une situation contrainte.

#### Scenario 5 - Consulter les disponibilites

<img src="./Diagramme d'objet/Scenario 5 Consulter disponibiltés.png" alt="Diagramme d'objet scenario 5" width="900" />

Ce diagramme montre les objets manipules lorsqu'un utilisateur consulte les disponibilites. Il donne une lecture concrete des ressources, dates ou liens necessaires pour determiner si une reservation peut etre envisagee.

#### Scenario 6 - Consulter les statistiques

<img src="./Diagramme d'objet/Scenario 6 Consulter stats.png" alt="Diagramme d'objet scenario 6" width="900" />

Ce diagramme illustre le contexte de consultation statistique. Il aide a comprendre quelles instances du modele contribuent a la production d'informations de synthese, utiles pour le pilotage ou l'evaluation de l'activite du centre.

## Interet de l'utilisation de BESSER

Le recours a BESSER dans ce projet presente un interet pedagogique et technique important. L'outil permet de partir d'une modelisation du domaine pour produire une base d'application exploitable. Cette approche met en valeur la transition entre la conception et l'implementation.

Dans ce projet, BESSER a notamment permis :

- de structurer la generation du backend et du frontend ;
- de materialiser rapidement les entites et les routes CRUD ;
- de mettre en coherence les modeles UML et l'application produite ;
- de se concentrer ensuite sur l'analyse, la comprehension et la documentation du systeme genere.

## Conclusion

Ce projet de gestion d'un centre de congres illustre une demarche complete de conception logicielle dans un contexte academique. Il combine la modelisation UML, la generation assistee avec BESSER, l'exploitation d'une architecture web moderne et la documentation des fonctionnalites obtenues.

Il constitue a la fois une application de gestion et un support d'apprentissage sur la modelisation, l'architecture logicielle, les API REST et la transformation d'un modele conceptuel en application exploitable.

## Notes complementaires

- Le backend initialise automatiquement la base SQLite dans `web_app_output/backend/data/Class_Diagram.db`.
- Le frontend consomme l'API via la variable `VITE_API_URL`.
- Le projet contient plusieurs diagrammes UML permettant de documenter le domaine metier et la conception.
- La documentation interactive de l'API est disponible via FastAPI.
