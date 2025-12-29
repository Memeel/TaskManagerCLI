#!/usr/bin/env python3
"""
TaskManager - Gestionnaire de tâches en ligne de commande.

Programme principal du gestionnaire de tâches développé dans le cadre du codecamp.
Ce script coordonne l'analyse des arguments, la lecture des fichiers et l'exécution
des commandes de gestion de tâches.

Usage:
    python3 task.py <fichier> add <description> -l <etiquette1> <etiquette2> ...
    python3 task.py <fichier> modify <id> <nouvelle_description>
    python3 task.py <fichier> rm <id>
    python3 task.py <fichier> addLabel <id> <etiquette1> <etiquette2> ...
    python3 task.py <fichier> rmLabel <id>
    python3 task.py <fichier> clearLabel <id>
    python3 task.py <fichier> show

Exemples:
    python3 task.py lestaches.txt add "Faire les courses" -l "demain"
    python3 task.py lestaches.txt modify 1 "Faire les courses au supermarché"
    python3 task.py lestaches.txt rm 1
    python3 task.py lestaches.txt addLabel 1 urgent 
    python3 task.py lestaches.txt rmLabel 1
    python3 task.py lestaches.txt clearLabel 1
    python3 task.py lestaches.txt show
"""

import commands
from options import create_parser

# === ANALYSE DES ARGUMENTS ===
# Création et utilisation du parseur de ligne de commande
options = create_parser().parse_args()

try:
    # === LECTURE DU FICHIER DE TÂCHES ===
    # Tente de lire le fichier existant
    with open(options.file, 'r') as f:
        tasks = f.readlines()
    
    # === EXÉCUTION DE LA COMMANDE ===
    # Dispatch vers la fonction appropriée selon la commande

    ## Commandes de base
    if options.command == 'add':
        # Disjonction de cas selon les options
        if options.labels and options.status:
            # Ajoute une nouvelle tâche
            commands.add(' '.join(options.details), options.file, tasks, options.labels, options.status)
        elif options.labels:
            # Ajoute une nouvelle tâche
            commands.add(' '.join(options.details), options.file, tasks, options.labels)
        elif options.status:
            # Ajoute une nouvelle tâche
            commands.add(' '.join(options.details), options.file, tasks, status = options.status)
        else:
            commands.add(' '.join(options.details), options.file, tasks)

        
    elif options.command == 'modify':
        # Disjonction de cas selon les options
        if options.details and options.status:
            # Modifie la description d'une tâche existante
            commands.modify(options.id, options.file, tasks, ' '.join(options.details), options.status)
        elif options.details:
            # Modifie la description d'une tâche existante
            commands.modify(options.id, options.file, tasks, ' '.join(options.details))
        elif options.status:
            # Modifie la description d'une tâche existante
            commands.modify(options.id, options.file, tasks, new_status = options.status)
        else:
            print("Erreur: Absence de description ou de statut à modifier")
        
    elif options.command == 'rm':
        # Supprime une tâche
        commands.rm(options.id, options.file, tasks)

    elif options.command == 'add_options':
        # Prépare les labels et la dépendance
        labels = options.labels if options.labels else None
        dep = options.dependence if options.dependence else None

        # Appelle la fonction une seule fois
        commands.add_options(options.id, options.file, tasks, new_labels=labels, id_dep=dep)
      
    elif options.command == 'rmLabel':
        # Supprime une étiquette en demandant à l'utilisateur le label à supprimer
        commands.rmLabel(options.id, options.file, tasks)
    
    elif options.command == 'clearLabel':
        # Supprime l'ensemble des étiquettes d'une tâche
        commands.clearLabel(options.id, options.file, tasks)
    
    elif options.command == 'rmDep':
        # Supprime la dépendance d'une tâche
        commands.rmDep(options.id, options.file, tasks)
        
    ## Affichage
    elif options.command == 'show':
        # Affiche toutes les tâches
        commands.show(tasks)
        
except FileNotFoundError:
    # === GESTION DES FICHIERS INEXISTANTS ===
    # Gère le cas où le fichier de tâches n'existe pas encore
    if options.command == 'add':
        # Permet d'ajouter la première tâche dans un nouveau fichier
        labels = options.labels if hasattr(options, 'labels') and options.labels else None
        commands.add(' '.join(options.details), options.file, [], labels)
    elif options.command == 'add_options':
        # Impossible d'ajouter une étiquette dans un fichier inexistant
        print(f"Error: The file {options.file} was not found")
    elif options.command == 'modify':
        # Impossible de modifier dans un fichier inexistant
        print(f"Error: The file {options.file} was not found")
    elif options.command in ['rm', 'rmLabel', 'clearLabel', 'rmDep']:
        # Impossible de supprimer dans un fichier inexistant
        print(f"Error: The file {options.file} was not found")
    elif options.command == 'show':
        # Affiche un message approprié pour un fichier vide
        print("No tasks found.")
