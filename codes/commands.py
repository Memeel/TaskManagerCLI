"""
Ce module implémente l'interface entre la ligne de commande et la logique métier.
Il gère les opérations sur les fichiers et l'affichage des messages utilisateur.

Chaque fonction correspond à une commande CLI et gère:
- La lecture/écriture des fichiers de tâches
- L'affichage des messages de succès/erreur
- La coordination avec le module core pour la logique métier
"""

import core
from datetime import datetime

def get_current_datetime():
    """Retourne la date et l'heure actuelle sous forme de chaîne."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def add(details, filename, tasks, labels = None):
    """
    Commande CLI pour ajouter une nouvelle tâche.
    
    Args:
        details (str): Description de la nouvelle tâche
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        labels (str, optional) : Etiquette(s) de la nouvelle tâche, None si aucune
        
    Side Effects:
        - Ajoute une ligne au fichier spécifié
        - Affiche un message de confirmation avec l'ID assigné
        
    Example:
        >>> add("Faire les courses", "tasks.txt", [], "important")
        Successfully added task 1 (Faire les courses: important)
    """
    # Utilise la logique métier pour créer la nouvelle tâche
    task_id, description, labels_list, task_line = core.add(tasks, details, labels)
    with open("history.txt", "a") as h:
        h.write(f"[this task was add as {get_current_datetime()}] id: {task_id} | desc: {description} | labels: {labels_list}\n")
    
    # Ajoute la tâche au fichier (mode append)
    with open(filename, 'a') as f:
        f.write(task_line)
    
    # Gestion des étiquettes
    labels_str = ",".join(labels_list) if labels_list else "None"

    # Confirmation à l'utilisateur
    print(f"Successfully added task {task_id} ({description}: {labels_str})")

def modify(task_id, new_details, filename, tasks):
    """
    Commande CLI pour modifier une tâche existante.
    
    Args:
        task_id (str): ID de la tâche à modifier
        new_details (str): Nouvelle description pour la tâche
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        
    Side Effects:
        - Réécrit entièrement le fichier avec les modifications
        - Affiche un message de succès ou d'erreur
        
    Note:
        Le fichier est entièrement réécrit pour maintenir la cohérence.
        
    Example:
        >>> modify("1", "Nouvelle description", "tasks.txt", ["1;Ancienne;None"])
        Task 1 modified.
    """
    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.modify(tasks, task_id, new_details)
    
    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab in updated_tasks:
                # Gestion des étiquettes
                labels_str = ",".join(lab) if lab else "None"
                f.write(f"{tid};{desc};{labels_str}\n")
        print(f"Task {task_id} modified.")

        # Enregistre les modifications dans l'historique
        with open("historique.txt", 'a') as h:
            tid, desc, lab = old_task
            labels_str = ",".join(lab) if lab else "None" 
            h.write(f"[The description of this task was modified on {get_current_datetime()}] {tid};{desc};{labels_str}\n")

    else:
        # Message d'erreur si la tâche n'existe pas
        print(f"Error: task id {task_id} not found.")

def rm(task_id, filename, tasks):
    """
    Commande CLI pour supprimer une tâche.
    
    Args:
        task_id (str): ID de la tâche à supprimer
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        
    Side Effects:
        - Réécrit le fichier sans la tâche supprimée
        - Affiche un message de succès ou d'erreur
        
    Note:
        Les IDs des autres tâches ne sont pas modifiés après suppression.
        
    Example:
        >>> rm("1", "tasks.txt", ["1;Tâche à supprimer;None", "2;Autre tâche;None"])
        Task 1 removed.
    """
    # Utilise la logique métier pour supprimer la tâche
    found, remaining_tasks, old_task = core.rm(tasks, task_id)
    
    if found:
        # Réécrit le fichier avec les tâches restantes
        with open(filename, 'w') as f:
            for tid, desc, lab in remaining_tasks:
                # Gestion des étiquettes
                labels_str = ",".join(lab) if lab else "None"
                f.write(f"{tid};{desc};{labels_str}\n")
        print(f"Task {task_id} removed.")

        with open("historique.txt", 'a') as h:
            tid, desc, lab = old_task
            labels_str = ",".join(lab) if lab else "None" 
            h.write(f"[This task was removed on {get_current_datetime()}] {tid};{desc};{labels_str}\n")

    else:
        # Message d'erreur si la tâche n'existe pas
        print(f"Error: task id {task_id} not found.")

def addLabel(task_id, new_labels, filename, tasks):
    """
    Commande CLI pour ajouter une ou plusieurs étiquettes à une tâche existante.
    
    Args:
        task_id (str): ID de la tâche à modifier
        new_labels (str): Étiquette(s) à ajouter à la tâche (séparées par des espaces)
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        
    Side Effects:
        - Réécrit entièrement le fichier avec les modifications
        - Affiche un message de succès ou d'erreur
        
    Note:
        Le fichier est entièrement réécrit pour maintenir la cohérence.
        Les doublons d'étiquettes sont automatiquement évités.
        
    Example:
        >>> addLabel("1", "urgent important", "tasks.txt", ["1;Ancienne;None"])
        Labels added successfully.
    """
    # Convertit la chaîne d'étiquettes en liste si c'est une chaîne
    if isinstance(new_labels, str):
        labels_list = new_labels.split()
    else:
        labels_list = new_labels if new_labels else []

    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.addLabel(tasks, task_id, labels_list)
    
    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab in updated_tasks:
                # Gestion des étiquettes
                labels_str = ",".join(lab) if lab else "None"
                f.write(f"{tid};{desc};{labels_str}\n")
        print(f"Labels added successfully.")

        with open("historique.txt", 'a') as h:
            tid, desc, lab = old_task
            labels_str = ",".join(lab) if lab else "None" 
            h.write(f"[A label was added to this task on {get_current_datetime()}] {tid};{desc};{labels_str}\n")

    else:
        # Message d'erreur si la tâche n'existe pas
        print(f"Error: task id {task_id} not found.")

def rmLabel(task_id, filename, tasks):
    """
    Commande CLI pour supprimer une étiquette d'une tâche existante.
    
    Args:
        task_id (str): ID de la tâche à modifier
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        
    Side Effects:
        - Réécrit entièrement le fichier avec les modifications
        - Affiche un message de succès ou d'erreur
        
    Note:
        Le fichier est entièrement réécrit pour maintenir la cohérence.
        
    Example:
        >>> rmLabel("1", "tasks.txt", ["1;Ancienne;etiquette"])
        Label deleted.
    """

    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.rmLabel(tasks, task_id)
    
    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab in updated_tasks:
                # Gestion des étiquettes
                labels_str = ",".join(lab) if lab else "None"
                f.write(f"{tid};{desc};{labels_str}\n")
        print(f"Label removed successfully.")

        with open("historique.txt", 'a') as h:
            tid, desc, lab = old_task
            labels_str = ",".join(lab) if lab else "None" 
            h.write(f"[A label was removed from this task on {get_current_datetime()}] {tid};{desc};{labels_str}\n")

    else:
        # Message d'erreur si la tâche n'existe pas
        print(f"Error: task id {task_id} not found.")

def clearLabel(task_id, filename, tasks):
    """
    Commande CLI pour supprimer toutes les étiquettes d'une tâche existante.
    
    Args:
        task_id (str): ID de la tâche à modifier
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        
    Side Effects:
        - Réécrit entièrement le fichier avec les modifications
        - Affiche un message de succès ou d'erreur
        
    Note:
        Le fichier est entièrement réécrit pour maintenir la cohérence.
        
    Example:
        >>> clearLabel("1", "tasks.txt", ["1;Ancienne;etiquette"])
        Labels deleted.
    """
    
    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.clearLabel(tasks, task_id)
    
    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab in updated_tasks:
                # Gestion des étiquettes
                labels_str = ",".join(lab) if lab else "None"
                f.write(f"{tid};{desc};{labels_str}\n")
        print(f"All labels removed successfully.")

        with open("historique.txt", 'a') as h:
            tid, desc, lab = old_task
            labels_str = ",".join(lab) if lab else "None" 
            h.write(f"[All labels of this task were removed on {get_current_datetime()}] {tid};{desc};{labels_str}\n")

    else:
        # Message d'erreur si la tâche n'existe pas
        print(f"Error: task id {task_id} not found.")


def show(tasks):
    """
    Commande CLI pour afficher toutes les tâches.
    
    Args:
        tasks (list): Liste des lignes du fichier de tâches
        
    Side Effects:
        - Affiche un tableau formaté des tâches sur stdout
        - Affiche "No tasks found." si aucune tâche n'existe
        
    Note:
        Délègue l'affichage au module core qui gère le formatage du tableau.
        
    Example:
        >>> show(["1;Première tâche;étiquette1,étiquette2", "2;Seconde tâche;None"])
        +-----+---------------+------------------------+
        | id  | description   | étiquettes             |
        +-----+---------------+------------------------+
        | 1   | Première tâche| étiquette1, étiquette2 |
        | 2   | Seconde tâche | None                   |
        +-----+---------------+------------------------+
    """
    # Délègue l'affichage au module core
    core.show(tasks)