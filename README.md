# Gestion d'un Centre de Congres

## Presentation du projet

CE README NOUS SERT DE RAPPORT.

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

## Description rapide du projet et de ses contraintes

Le projet porte sur la gestion numerique d'un centre de congres. Il vise a centraliser les informations necessaires a l'administration du centre, a la planification des evenements et a la gestion des ressources associees aux reservations.

Les principales contraintes prises en compte dans le projet sont les suivantes :

- la disponibilite des espaces et des ressources ;
- les contraintes appliquees aux elements du centre ;
- les regles de location et d'utilisation ;
- la coherence entre reservation, evenement, materiel et prestations ;
- la prise en compte d'etats metier comme la creation, la confirmation ou l'annulation ;
- la necessite de structurer le projet selon une demarche UML avant generation de l'application.

## Presentation des acteurs

Les acteurs qui interagissent avec le systeme sont principalement :

- **Le gestionnaire** : acteur principal de l'application. Il consulte les donnees, cree et modifie les entites du systeme, suit les reservations et organise les ressources du centre.
- **Le centre de congres comme cadre organisationnel** : meme s'il ne s'agit pas d'un acteur humain, il constitue le contexte central du systeme autour duquel gravitent les reservations, les evenements et les ressources.
- **Les entites de support metier** : reservation, evenement, materiel, prestations, contraintes, paiements et personnes referentes interviennent comme objets du domaine manipules par le gestionnaire.

Dans une lecture UML stricte, le gestionnaire est l'acteur humain central visible dans les cas d'utilisation. Les autres elements structurent surtout le domaine metier du systeme.

## Architecture du projet

Le projet est organise autour de deux parties principales :

- un **frontend** qui fournit l'interface utilisateur pour consulter et manipuler les donnees ;
- un **backend** qui expose l'API REST, applique la logique de persistence et gere la base de donnees.

Le backend est construit avec FastAPI et SQLAlchemy. Il genere des points d'entree CRUD pour les entites metier principales et initialise automatiquement une base SQLite locale.

Le frontend est construit avec React, TypeScript et Vite. Il propose plusieurs pages, chacune associee a une entite ou a un ensemble fonctionnel du domaine, afin de faciliter la navigation et la gestion des donnees.

## Description de l'architecture generale, des packages, de leurs roles et interfaces

L'architecture generale repose sur une separation claire entre presentation, logique d'acces aux donnees et persistence.

### Package `web_app_output/backend`

Ce package contient la partie serveur de l'application.

Son role principal est :

- d'exposer les routes API ;
- de definir les modeles de donnees ;
- de gerer les sessions de base de donnees ;
- de fournir les operations CRUD sur les entites metier.

Ses interfaces principales sont :

- les endpoints HTTP exposes par FastAPI ;
- la documentation interactive Swagger ;
- les schemas Pydantic servant d'interface de validation entre clients et backend.

Fichiers importants :

- `main_api.py` : point d'entree principal de l'API, declaration des routes, middleware, gestion de session et operations CRUD ;
- `sql_alchemy.py` : definition des classes ORM et des relations entre les entites ;
- `pydantic_classes.py` : schemas de validation et de serialisation utilises par l'API ;
- `requirements.txt` : dependances Python du backend ;
- `Dockerfile` : conteneurisation du backend.

### Package `web_app_output/frontend`

Ce package contient l'interface utilisateur de l'application.

Son role principal est :

- d'afficher les pages de gestion ;
- d'appeler l'API backend ;
- de presenter les entites metier de facon exploitable par un utilisateur.

Ses interfaces principales sont :

- les pages React accessibles via le routage ;
- les composants reutilisables d'affichage ;
- les requetes HTTP vers l'API backend.

Fichiers et sous-packages importants :

- `src/App.tsx` : configuration des routes principales de l'application ;
- `src/pages/` : pages correspondant aux entites du domaine ;
- `src/components/` : composants reutilisables d'interface ;
- `src/contexts/` : gestion du contexte global, notamment pour les tables ;
- `package.json` : dependances et scripts du frontend ;
- `vite.config.ts` : configuration de Vite ;
- `Dockerfile` : conteneurisation du frontend.

### Package `CapturesDeL'interface de L'app`

Ce package documentaire regroupe les captures d'ecran de l'interface. Il sert a illustrer les modules disponibles et a appuyer la presentation du projet.

### Packages de diagrammes UML

Les dossiers `Diagramme de classe`, `Diagramme de cas d'utilisation`, `Diagramme de sequence`, `Diagramme d'etat` et `Diagramme d'objet` constituent la partie documentaire UML du projet.

Leur role est :

- de presenter la conception ;
- de justifier les choix de modelisation ;
- d'expliquer le fonctionnement statique et dynamique du systeme ;
- de faire le lien entre analyse UML et code genere.

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

## Presentation des fonctionnalites attendues du systeme

Les fonctionnalites attendues du systeme sont visibles a travers le diagramme de cas d'utilisation et les ecrans de l'application. Les principales sont :

- configurer un centre de congres ;
- gerer les elements du centre ;
- creer une reservation ;
- confirmer une reservation ;
- annuler une reservation ;
- consulter les disponibilites ;
- consulter les statistiques ;
- gerer les ressources associees comme le materiel, les prestations et les contraintes.

Ces fonctionnalites traduisent les besoins principaux du domaine metier et structurent l'ensemble du projet.

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

#### Explication des cardinalites du diagramme de classe

Les cardinalites indiquent combien d'instances d'une classe peuvent etre associees a combien d'instances d'une autre classe. Elles sont essentielles pour comprendre les contraintes structurelles du modele.

Voici l'interpretation des cardinalites definies dans le code UML :

- `Gestionnaire "1" --> "1..*" CentreDeCongres` : un gestionnaire gere au moins un centre de congres, et potentiellement plusieurs. Chaque centre de congres est rattache a un seul gestionnaire dans ce modele.
- `Gestionnaire "1" --> "0..*" Reservation` : un gestionnaire peut ne creer aucune reservation ou en gerer plusieurs. Chaque reservation est associee a un seul gestionnaire.
- `CentreDeCongres "1" *-- "1..*" ElementCentre` : un centre de congres contient obligatoirement un ou plusieurs elements. Chaque element appartient a un seul centre. La composition indique ici une relation forte de dependance structurelle.
- `ElementCentre "1" *-- "0..1" Contrainte` : un element du centre peut n'avoir aucune contrainte ou au maximum une seule contrainte associee. Une contrainte est ici liee a un seul element dans ce modele.
- `ElementCentre "1" *-- "0..*" Indisponibilite` : un element peut avoir zero, une ou plusieurs periodes d'indisponibilite. Chaque indisponibilite concerne un seul element.
- `ElementCentre "1" *-- "1..*" Tarif` : chaque element doit avoir au moins un tarif, et peut en avoir plusieurs. Chaque tarif est associe a un seul element.
- `CentreDeCongres "1" o-- "0..*" Materiel` : un centre peut disposer d'aucun materiel ou de plusieurs materiels. Chaque materiel est rattache a un centre dans cette modelisation. L'agregation montre une relation plus souple que la composition.
- `CentreDeCongres "1" o-- "0..*" Prestation` : un centre peut proposer zero, une ou plusieurs prestations. Chaque prestation est rattachee a un centre dans le modele.
- `Materiel "1" *-- "0..1" RegleLocation` : un materiel peut ne pas avoir de regle de location ou en avoir une seule.
- `Prestation "1" *-- "0..1" RegleLocation` : une prestation peut egalement ne pas avoir de regle de location ou en avoir une seule.
- `Evenement "1" --> "1" PersonneReferente` : chaque evenement a exactement une personne referente, et chaque association consideree ici relie un evenement a une seule personne referente.
- `Reservation "1" --> "1" Evenement` : chaque reservation concerne exactement un evenement, et dans ce modele une reservation ne peut pas exister sans evenement associe.
- `Reservation "1" --> "1..*" ElementCentre` : une reservation doit porter sur au moins un element du centre, et peut en concerner plusieurs.
- `Reservation "1" --> "0..*" Materiel` : une reservation peut ne mobiliser aucun materiel ou plusieurs materiels selon le besoin.
- `Reservation "1" --> "0..*" Prestation` : une reservation peut ne comporter aucune prestation ou en inclure plusieurs.
- `Reservation "1" --> "1" StatutReservation` : chaque reservation possede exactement un statut a un instant donne, comme `EN_ATTENTE`, `CONFIRMEE` ou `ANNULEE`.
- `Reservation "1" --> "0..1" Paiement` : une reservation peut ne pas encore avoir de paiement, ou etre liee a un paiement unique.
- `Reservation "1" --> "1" Tarif` : chaque reservation applique exactement un tarif dans le modele retenu.

#### Lecture fonctionnelle des cardinalites

Ces cardinalites montrent plusieurs choix de conception importants :

- un centre de congres ne peut pas etre vide dans le modele, puisqu'il doit contenir au moins un `ElementCentre` ;
- une reservation ne peut pas etre abstraite : elle doit etre liee a un `Evenement`, a au moins un `ElementCentre`, a un `StatutReservation` et a un `Tarif` ;
- le materiel, les prestations, les paiements et certaines contraintes sont optionnels selon le contexte ;
- les relations de composition signalent des dependances fortes, alors que les agregations representent des associations plus souples.

Autrement dit, les cardinalites permettent de distinguer :

- ce qui est **obligatoire** dans le systeme ;
- ce qui est **optionnel** ;
- ce qui peut exister en **un seul exemplaire** ;
- ce qui peut exister en **plusieurs occurrences**.

### Diagramme de cas d'utilisation

<img src="./Diagramme de cas d'utilisation/Diagramme de cas d'utlisation.png" alt="Diagramme de cas d'utilisation" width="900" />

Le diagramme de cas d'utilisation presente le systeme du point de vue des acteurs. Il met l'accent sur les fonctionnalites offertes et sur les interactions possibles avec l'application. Il permet de visualiser les grands services rendus par le systeme, comme la configuration du centre, la creation d'une reservation, la confirmation d'une reservation, l'annulation d'une reservation, la consultation des disponibilites ou encore le suivi statistique.

Ce diagramme est important, car il donne une lecture fonctionnelle du projet. Il repond a la question : **qu'est-ce que le systeme doit permettre de faire ?**

Les cas d'utilisation identifies dans le projet permettent donc :

- d'identifier clairement les attentes fonctionnelles ;
- de relier les besoins du gestionnaire aux services du systeme ;
- de structurer les scenarios qui seront ensuite approfondis dans les diagrammes de sequence et d'etat.

### Diagramme d'etat

<img src="./Diagramme d'etat/Diagramme d'etats.png" alt="Diagramme d'etat" width="900" />

Le diagramme d'etat montre l'evolution d'un objet au cours de son cycle de vie. Dans ce projet, il est particulierement utile pour comprendre les changements d'etat lies au processus de reservation. Il permet de suivre les transitions possibles entre differentes situations, comme la creation, la confirmation, l'annulation ou les cas conditionnes par certaines regles metier.

Ce diagramme apporte une vision dynamique complementaire au diagramme de classe. Il montre non seulement quelles sont les entites du systeme, mais aussi comment elles evoluent dans le temps.

## Presentation detaillee des diagrammes d'etat

Le diagramme d'etat detaille la maniere dont une reservation evolue pendant son cycle de vie. On peut l'interpreter de la facon suivante :

- un etat initial correspond a la creation ou a l'enregistrement de la reservation ;
- des transitions permettent ensuite de passer vers un etat confirme si les conditions sont satisfaites ;
- des transitions alternatives permettent d'annuler la reservation selon certaines situations ;
- les changements d'etat sont conditionnes par des regles metier, des validations ou des contraintes temporelles.

Ce diagramme est essentiel pour comprendre la dynamique interne du systeme, car il montre comment une simple donnee devient un objet metier evolutif soumis a des regles de gestion.

### Diagrammes de sequence

Les diagrammes de sequence decrivent l'ordre chronologique des interactions entre les acteurs, l'interface et les composants metier. Ils sont utiles pour comprendre le deroulement exact d'un scenario.

## Explication du fonctionnement dynamique de chaque fonctionnalite

Le fonctionnement dynamique du systeme est principalement represente par les diagrammes de sequence et le diagramme d'etat.

- la **creation d'une reservation** suit un enchainement d'actions allant de la saisie de la demande jusqu'a son enregistrement dans le systeme ;
- la **confirmation d'une reservation** ajoute une logique de validation et de changement d'etat ;
- l'**annulation d'une reservation** introduit une logique de controle, notamment selon les delais ou les conditions prevues ;
- la **consultation des disponibilites** mobilise les objets necessaires pour verifier si une ressource ou un espace peut etre reserve ;
- la **consultation des statistiques** s'appuie sur les objets du domaine pour produire une vue synthetique de l'activite.

Les diagrammes de sequence montrent l'ordre des messages, tandis que le diagramme d'etat montre la transformation interne de l'objet reservation.

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

## Description package par package des diagrammes de classe qui les constituent

Le projet ne separe pas explicitement le diagramme de classe en plusieurs fichiers UML par package, mais la structure du code permet d'en proposer une lecture par grands ensembles.

### Package backend - lecture du diagramme de classe

Dans le backend, le diagramme de classe se concretise surtout a travers les modeles ORM et les schemas Pydantic.

- `sql_alchemy.py` correspond a la traduction des classes metier persistantes ;
- `pydantic_classes.py` represente les interfaces de donnees echangees avec l'API ;
- `main_api.py` exploite ces classes pour fournir les comportements CRUD.

Les classes principales du diagramme y sont reliees par des associations qui traduisent les relations metier :

- une reservation peut etre liee a un evenement ;
- un centre de congres contient ou reference des elements ;
- une reservation peut mobiliser du materiel et des prestations ;
- des contraintes et regles de location encadrent certaines relations.

### Package frontend - lecture du diagramme de classe

Le frontend ne reprend pas le diagramme de classe UML au sens strict, mais il en propose une projection fonctionnelle a travers ses pages et composants.

- chaque page du dossier `src/pages/` correspond a une entite ou un sous-domaine ;
- les composants du dossier `src/components/` assurent l'affichage, la navigation et la manipulation des donnees ;
- le routage dans `App.tsx` constitue l'interface d'acces aux differents modules du domaine.

On peut donc lire le frontend comme une traduction visuelle et interactive des classes et relations definies au niveau metier.

### Package documentaire UML

Les packages de diagrammes constituent le support theorique de la conception :

- le diagramme de classe porte la structure statique ;
- le diagramme de cas d'utilisation porte les besoins fonctionnels ;
- les diagrammes de sequence portent les scenarios dynamiques ;
- le diagramme d'etat porte l'evolution temporelle des objets ;
- les diagrammes d'objet portent des instantanes concrets du systeme.

## Interet de l'utilisation de BESSER

Le recours a BESSER dans ce projet presente un interet pedagogique et technique important. L'outil permet de partir d'une modelisation du domaine pour produire une base d'application exploitable. Cette approche met en valeur la transition entre la conception et l'implementation.

Dans ce projet, BESSER a notamment permis :

- de structurer la generation du backend et du frontend ;
- de materialiser rapidement les entites et les routes CRUD ;
- de mettre en coherence les modeles UML et l'application produite ;
- de se concentrer ensuite sur l'analyse, la comprehension et la documentation du systeme genere.

## Analyse et commentaires du code genere par BESSER

Le code genere par BESSER fournit une base de travail solide pour un projet academique, car il transforme directement la modelisation en artefacts logiciels exploitables.

### Points positifs du code genere

- il met rapidement en place une architecture exploitable ;
- il genere un backend CRUD complet avec FastAPI ;
- il structure les modeles de donnees de facon coherente avec la modelisation ;
- il permet d'obtenir un frontend navigable relie aux principales entites ;
- il facilite la demonstration du passage entre UML et implementation.

### Observations sur le backend genere

Le fichier `main_api.py` montre une generation tres large de routes REST. Cette approche est utile pour couvrir rapidement les besoins CRUD, mais elle produit aussi un fichier volumineux. Le code est donc fonctionnel, mais sa taille peut rendre la maintenance manuelle plus difficile si le projet grandit fortement.

Les schemas et modeles sont clairement separes entre `pydantic_classes.py` et `sql_alchemy.py`, ce qui est un bon point en termes de lisibilite architecturale. Cette separation clarifie le role de chaque couche :

- les modeles ORM pour la persistence ;
- les schemas Pydantic pour les entrees et sorties API ;
- les routes FastAPI pour l'exposition des services.

### Observations sur le frontend genere

Le frontend propose une structure simple et comprehensible :

- un routage centralise ;
- une page par entite principale ;
- des composants de tableau et de visualisation reutilisables.

Cette organisation est bien adaptee a un projet de demonstration ou a un prototype de gestion. Elle met l'accent sur l'accessibilite des donnees plutot que sur une logique front-end tres complexe.

### Limites et pistes d'amelioration

Le code genere constitue une bonne base, mais il peut etre complete par :

- une meilleure modularisation de certaines routes backend ;
- l'ajout d'une logique metier plus explicite dans certaines methodes encore vides ;
- une gestion plus poussee de l'authentification et des droits ;
- des validations metier plus approfondies ;
- des tests automatises plus nombreux ;
- une standardisation plus poussee du style et de la documentation du code.

Dans l'ensemble, le code genere par BESSER est pertinent pour illustrer une approche de generation dirigee par les modeles. Il montre bien comment une modelisation UML peut servir de point de depart a une application web complete.

## Conclusion

Ce projet de gestion d'un centre de congres illustre une demarche complete de conception logicielle dans un contexte academique. Il combine la modelisation UML, la generation assistee avec BESSER, l'exploitation d'une architecture web moderne et la documentation des fonctionnalites obtenues.

Il constitue a la fois une application de gestion et un support d'apprentissage sur la modelisation, l'architecture logicielle, les API REST et la transformation d'un modele conceptuel en application exploitable.

## Notes complementaires

- Le backend initialise automatiquement la base SQLite dans `web_app_output/backend/data/Class_Diagram.db`.
- Le frontend consomme l'API via la variable `VITE_API_URL`.
- Le projet contient plusieurs diagrammes UML permettant de documenter le domaine metier et la conception.
- La documentation interactive de l'API est disponible via FastAPI.
