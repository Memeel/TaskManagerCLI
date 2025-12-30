# TaskManager - Gestionnaire de Tâches en CLI

## Auteurs (Groupe 4)

- Rayene ABBASSI
- Amira BALTI
- Adam BOUZID
- Luis RODRIGUES DE OLIVEIRA
- Mélina WANG

## Description du Projet

Dans le cadre des séances *codecamp*, nous avions pour mission de produire en équipe un logiciel simple de gestion de tâches avec une interface en ligne de commande (CLI). 

Le système permet de gérer des tâches avec les fonctionnalités suivantes :
- Ajout de nouvelles tâches (avec étiquettes, statut et dépendances)
- Modification de tâches existantes (description et statut)
- Suppression de tâches
- Gestion des étiquettes (ajout/suppression)
- Gestion des dépendances entre tâches
- Suivi de l'historique des modifications
- Affichage de la liste des tâches

Chaque tâche possède :
- Un **identifiant unique** (ID numérique auto-incrémenté)
- Une **description**
- Une liste d'**étiquettes**
- Un **statut** (started, suspended, completed, cancelled)
- Une **dépendance** optionnelle (ID d'une autre tâche)

## Architecture du Code

Le projet est organisé en plusieurs modules pour une meilleure séparation des responsabilités :

- **`task.py`** : Point d'entrée principal du programme (exécutable)
- **`core.py`** : Logique métier - implémentation des fonctions de gestion des tâches
- **`commands.py`** : Interface entre la ligne de commande et la logique métier
- **`options.py`** : Analyseur de ligne de commande (utilise `argparse`)

## Installation et Utilisation

### Prérequis
- Python 3.10 ou supérieur
- Aucune dépendance externe (utilise uniquement la bibliothèque standard Python)

### Utilisation

Le programme s'utilise avec la syntaxe suivante :
```bash
python src/task.py <fichier_taches> <commande> [arguments]
```

#### Commandes disponibles

1. **Ajouter une tâche**
   ```bash
   python src/task.py lestaches.txt add <description de la tâche> [options]
   ```
   Exemple :
   ```bash
   python src/task.py lestaches.txt add "Faire les courses"
   python src/task.py lestaches.txt add "Faire les courses" -l "étiquette" -s "started"
   python src/task.py lestaches.txt add "Faire les courses" -l "étiquette1" "étiquette2" -s "completed"
   # Le programme demandera interactivement si la tâche dépend d'une autre
   ```

2. **Modifier une tâche**
   ```bash
   python src/task.py lestaches.txt modify <id> [options]
   ```
   Exemple :
   ```bash
   python src/task.py lestaches.txt modify 1 -d "Faire les courses au supermarché"
   python src/task.py lestaches.txt modify 1 -s "completed"
   ```

3. **Supprimer une tâche**
   ```bash
   python src/task.py lestaches.txt rm <id>
   ```
   Exemple :
   ```bash
   python src/task.py lestaches.txt rm 1
   ```

4. **Ajouter une option (Etiquette ou Dépendance)**
   ```bash
   python src/task.py lestaches.txt add_options <id> [-l <étiquette(s)>] [-d <id_dépendance>]
   ```
   Exemple :
   ```bash
   # Ajouter une étiquette
   python src/task.py lestaches.txt add_options 1 -l "urgent"

   # Ajouter une dépendance (la tâche 2 dépendra de la tâche 1)
   python src/task.py lestaches.txt add_options 2 -d 1
   ```

5. **Supprimer une étiquette**
   ```bash
   python src/task.py lestaches.txt rmLabel <id>
   ```
   La suppression se fait en deux temps, dans un premier on entre l'identifiant de la tâche à modifier, et dans un second temps, on choisit l'étiquette à supprimer en suivant les consignes affichées
   
   Exemple :
   ```bash
   >>> python src/task.py lestaches.txt rmLabel 1
   Étiquettes de la tâche :
   0: étiquette 1
   1: étiquette 2
   2: étiquette 3
   Entrez le numéro de l'étiquette à supprimer : 1
   ```

6. **Supprimer toutes les étiquettes**
   ```bash
   python src/task.py lestaches.txt clearLabel <id>
   ```
   Exemple :
   ```bash
   python src/task.py lestaches.txt clearLabel 1
   ```

7. **Supprimer une dépendance**
   ```bash
   python src/task.py lestaches.txt rmDep <id>
   ```
   Exemple :
   ```bash
   python src/task.py lestaches.txt rmDep 1
   ```

8. **Afficher toutes les tâches**
   ```bash
   python src/task.py lestaches.txt show
   ```

## Format de Fichier

Les tâches sont stockées dans un fichier texte avec le format structuré suivant :
```
ID;Description;Etiquette 1,Etiquette 2;Statut;ID_Dépendance
```

Exemple de contenu de fichier :
```
1;Réviser pour l'examen;Important;started;None 
2;Acheter des stylos;None;suspended;1
```

Un fichier `historique.txt` est également généré automatiquement pour tracer les actions.

## Fonctionnalités Implémentées

Le projet intègre les fonctionnalités suivantes, développées par niveaux successifs :

### Fonctionnalités de base
- Création, lecture (affichage), mise à jour et suppression de tâches
- Tri des tâches par ID lors de l'affichage
- IDs auto-incrémentés
- Sauvegarde des tâches dans un fichier texte
- Gestion intuitive via arguments de ligne de commande
- Gestion des erreurs (tâches non trouvées, fichiers inexistants)

### Niveau 1 : Notion d'étiquette
- Possibilité d'ajouter des tags (labels) aux tâches pour les catégoriser
- Commandes dédiées pour ajouter (`add_options`), supprimer une étiquette spécifique (`rmLabel`) ou toutes les étiquettes (`clearLabel`)

### Niveau 2 : Gestion de l'historique
- Chaque action de modification (ajout, suppression, modification, ajout d'option) est enregistrée automatiquement
- Un fichier `historique.txt` trace les événements avec horodatage précis

### Niveau 3 : Notion de dépendance entre tâches
- Possibilité de lier une tâche à une autre (tâche parente)
- Une tâche ne peut dépendre que d'une tâche existante
- Le tableau des tâches affiche désormais les dépendances

## Avancée du Projet

Le développement a suivi les jalons imposés par le Codecamp :

- **Niveau 0** : Implémentation des commandes de base (`add`, `modify`, `rm`, `show`)
- **Niveau 1** : Implémentation du système d'étiquettes (Labels)
- **Niveau 2** : Implémentation du système d'historique (Log)
- **Niveau 3** : Implémentation des dépendances entre tâches

## Tests

Le projet a été testé manuellement avec les commandes ci-dessus.

## Utilisation de l'IA

L'IA (GitHub Copilot) a été utilisée pour :
- Restructurer et nettoyer le code existant
- Corriger les bugs et erreurs de syntaxe
- Améliorer la cohérence entre les modules
- Optimiser la gestion des fichiers et des erreurs
- Formatter l'affichage des tâches en tableau
- **Améliorer considérablement la documentation du code** :
  - Ajout de docstrings complètes avec format standard Python
  - Documentation des paramètres, valeurs de retour et effets de bord
  - Exemples concrets d'utilisation pour chaque fonction
  - En-têtes de modules avec descriptions détaillées
  - Commentaires inline explicatifs et sections logiques
  - Messages d'aide CLI en français et plus détaillés
  - Documentation de l'architecture et du flux d'exécution
