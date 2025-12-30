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


def add(details, filename, tasks, labels = None, status = "suspended"):
    """
    Commande CLI pour ajouter une nouvelle tâche.
    
    Args:
        details (str): Description de la nouvelle tâche
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        labels (list[str], optional): Etiquette(s) de la nouvelle tâche, None si aucune
        status (str, optional): Statut initial de la tâche (défaut: "suspended")
        
    Side Effects:
        - Ajoute une ligne au fichier spécifié et à l'historique
        - Affiche un message de confirmation avec l'ID assigné
        - Peut demander interactivement à l'utilisateur de définir une dépendance
    """

    # Utilise la logique métier pour créer la nouvelle tâche
    result = core.add(tasks, details, labels, status)
    
    # Si l'utilisateur a annulé (Ctrl+C), on arrête tout pour éviter le crash
    if result[0] is None:
        return

    task_id, description, labels_list, task_line = result

    with open("historique.txt", "a") as h:
        h.write(f"[This task was added at {get_current_datetime()}] {task_line}")
    
    # Ajoute la tâche au fichier (mode append)
    with open(filename, 'a') as f:
        f.write(task_line)
    
    # Gestion des étiquettes
    labels_str = ",".join(labels_list) if labels_list else "None"

    # Confirmation à l'utilisateur
    print(f"Successfully added task {task_id} ({description}: {labels_str})")

def modify(task_id, filename, tasks, new_details = None, new_status = None):
    """
    Commande CLI pour modifier une tâche existante.
    
    Args:
        task_id (str): ID de la tâche à modifier
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        new_details (str, optional): Nouvelle description pour la tâche
        new_status (str, optional): Nouveau statut pour la tâche
        
    Side Effects:
        - Réécrit entièrement le fichier avec les modifications
        - Enregistre les modifications dans l'historique
        - Affiche un message de succès ou d'erreur
        
    Note:
        Le fichier est entièrement réécrit pour maintenir la cohérence.
    """

    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.modify(tasks, task_id, new_details, new_status)
    
    if found:
        # Vérifie la tâche modifiée pour l'affichage
        new_task = None
        for t in updated_tasks:
            if t[0] == old_task[0]:
                new_task = t
                break

        if new_task == old_task:
            print("Aucune modification apportée à la tâche.")
            return
        
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab, status, dep in updated_tasks:
                # Gestion des étiquettes et des dépendances
                labels_str = ",".join(lab) if lab else "None"
                dep = dep if dep else "None"
                f.write(f"{tid};{desc};{labels_str};{status};{dep}\n")
        print(f"Task {task_id} modified.")

        # Enregistre les modifications dans l'historique
        with open("historique.txt", 'a') as h:
            tid, desc, lab, status, dep = old_task
            labels_str = ",".join(lab) if lab else "None" 
            dep = dep if dep else "None"
            h.write(f"[The description of this task was modified at {get_current_datetime()}] {tid};{desc};{labels_str};{status};{dep}\n")

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
    """

    # Utilise la logique métier pour supprimer la tâche
    found, remaining_tasks, old_task = core.rm(tasks, task_id)
    
    if found:
        # Réécrit le fichier avec les tâches restantes
        with open(filename, 'w') as f:
            for tid, desc, lab, status, dep in remaining_tasks:
                # Gestion des étiquettes et des dépendances
                labels_str = ",".join(lab) if lab else "None"
                dep = dep if dep else "None"
                f.write(f"{tid};{desc};{labels_str};{status};{dep}\n")
        print(f"Task {task_id} removed.")

        with open("historique.txt", 'a') as h:
            tid, desc, lab, status, dep = old_task
            labels_str = ",".join(lab) if lab else "None" 
            dep = dep if dep else "None"
            h.write(f"[This task was removed at {get_current_datetime()}] {tid};{desc};{labels_str};{status};{dep}\n")

    else:
        # Message d'erreur si la tâche n'existe pas
        print(f"Error: task id {task_id} not found.")

def add_options(task_id, filename, tasks, new_labels = None, id_dep = None):
    """
    Commande CLI pour ajouter des options à une tâche existante (étiquettes ou dépendance).
    
    Args:
        task_id (str): ID de la tâche à modifier
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        new_labels (list[str], optional): Étiquette(s) à ajouter à la tâche
        id_dep (int, optional): ID de la tâche dont dépend la tâche cible
        
    Side Effects:
        - Réécrit entièrement le fichier avec les modifications
        - Enregistre les modifications dans l'historique
        - Affiche un message de succès ou d'erreur
        
    Note:
        Le fichier est entièrement réécrit pour maintenir la cohérence.
        Les doublons d'étiquettes sont automatiquement évités.
    """

    # Convertit la chaîne d'étiquettes en liste si c'est une chaîne
    if isinstance(new_labels, str):
        labels_list = new_labels.split()
    else:
        labels_list = new_labels if new_labels else []

    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.add_options(tasks, task_id, labels_list, id_dep)
    
    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab, state, dep in updated_tasks:
                # Gestion des étiquettes et des dépendances
                labels_str = ",".join(lab) if lab else "None"
                dep = dep if dep else "None"
                f.write(f"{tid};{desc};{labels_str};{state};{dep}\n")
        print(f"Options added successfully.")

        with open("historique.txt", 'a') as h:
            tid, desc, lab, state, dep = old_task
            labels_str = ",".join(lab) if lab else "None" 
            dep = dep if dep else "None"
            h.write(f"[A label was added to this task at {get_current_datetime()}] {tid};{desc};{labels_str};{state};{dep}\n")

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
    """

    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.rmLabel(tasks, task_id)
    
    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab, status, dep in updated_tasks:
                # Gestion des étiquettes
                labels_str = ",".join(lab) if lab else "None"
                f.write(f"{tid};{desc};{labels_str};{status};{dep}\n")
        print(f"Label removed successfully.")

        old_id, old_desc, old_lab, old_status, old_dep = old_task
        if old_lab: 
            labels_str = ",".join(old_lab)
        else:
            labels_str = "None"

        old_dep = old_dep if old_dep else "None"

        with open("historique.txt", 'a') as h:
            h.write(f"[A label was removed from this task at {get_current_datetime()}] {old_id};{old_desc};{labels_str};{old_status};{old_dep}\n")

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
    """
    
    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.clearLabel(tasks, task_id)
    
    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab, status, dep in updated_tasks:
                # Gestion des étiquettes et des dépendances
                labels_str = ",".join(lab) if lab else "None"
                dep = dep if dep else "None"
                f.write(f"{tid};{desc};{labels_str};{status};{dep}\n")
        print(f"All labels removed successfully.")

        with open("historique.txt", 'a') as h:
            tid, desc, lab, status, dep = old_task
            labels_str = ",".join(lab) if lab else "None" 
            dep = dep if dep else "None"
            h.write(f"[All labels of this task were removed at {get_current_datetime()}] {tid};{desc};{labels_str};{status};{dep}\n")

    else:
        # Message d'erreur si la tâche n'existe pas
        print(f"Error: task id {task_id} not found.")

def rmDep(task_id, filename, tasks):
    """
    Commande CLI pour supprimer une dépendance à une tâche existante.
    
    Args:
        task_id (str): ID de la tâche à modifier
        filename (str): Chemin vers le fichier de tâches
        tasks (list): Liste des lignes existantes du fichier
        
    Side Effects:
        - Réécrit entièrement le fichier avec les modifications
        - Affiche un message de succès ou d'erreur
        
    Note:
        Le fichier est entièrement réécrit pour maintenir la cohérence.
    """

    # Utilise la logique métier pour modifier la tâche
    found, updated_tasks, old_task = core.rmDep(tasks, task_id)

    if found:
        # Réécrit tout le fichier avec les tâches mises à jour
        with open(filename, 'w') as f:
            for tid, desc, lab, state, dep in updated_tasks:
                # Gestion des étiquettes
                labels_str = ",".join(lab) if lab else "None"
                # Gestion de la dépendance
                dep = dep if dep else "None"
                f.write(f"{tid};{desc};{labels_str};{state};{dep}\n")

        print("Dependence removed successfully.")

        old_id, old_desc, old_lab, old_state, old_dep = old_task
        labels_str = ",".join(old_lab) if old_lab else "None"
        old_dep = old_dep if old_dep else "None"

        with open("historique.txt", 'a') as h:
            h.write(
                f"[A dependence was removed from this task at {get_current_datetime()}] "
                f"{old_id};{old_desc};{labels_str};{old_state};{old_dep}\n"
            )

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
    """
    # Délègue l'affichage au module core
    core.show(tasks)