"""
Core module for task management.

Ce module contient la logique métier principale pour la gestion des tâches.
Il fournit les fonctions de base pour créer, modifier, supprimer et afficher des tâches.

Format des tâches: Chaque tâche est stockée sous forme "ID;Description;étiquette1,étiquette2" 
ou "ID;Description;None" (pour les tâches sans étiquettes) dans le fichier.

Rétrocompatibilité: Supporte aussi l'ancien format "ID;Description" (sans étiquettes).

Auteurs: Groupe 4 - Codecamp
"""


def parse_tasks(tasks):
    """
    Parse les lignes brutes du fichier en une liste structurée de tâches.
    
    Args:
        tasks (list): Liste des lignes lues depuis le fichier de tâches
        
    Returns:
        list: Liste de tuples (id: int, description: str, labels: list[str]) représentant les tâches, s'il n'y a pas d'étiquettes labels=[]
        
    Note:
        - Ignore les lignes vides
        - Ignore les lignes mal formatées (sans ';' ou avec ID non numérique)
        - Le format attendu est "ID;Description"
        
    Exemple:
        >>> parse_tasks(["1;Faire les courses;None", "2;Réviser;Urgent"])
        [(1, 'Faire les courses', []), (2, 'Réviser', ['Urgent'])]
    """
    parsed_tasks = []
    for line in tasks:
        line = line.strip()
        if line:  # Ignore les lignes vides
            parts = line.split(";")
            if len(parts) >= 2:  # Au minimum ID et description
                try:
                    tid = int(parts[0])
                    description = parts[1]
                    # Gestion des étiquettes (rétrocompatibilité)
                    if len(parts) >= 3 and parts[2] != "None":
                        labels = [label.strip() for label in parts[2].split(",") if label.strip()]
                    else:
                        labels = []
                    parsed_tasks.append((tid, description, labels))
                except ValueError:
                    # Ignore les lignes avec un ID non numérique
                    continue
    return parsed_tasks


def add(tasks, details, labels = None):
    """
    Ajoute une nouvelle tâche avec un ID auto-incrémenté.
    
    Args:
        tasks (list): Liste des lignes existantes du fichier de tâches
        details (str): Description de la nouvelle tâche
        labels (list[str], optional): Liste d'étiquette(s) de la nouvelle tâche, None si aucune 
        
    Returns:
        tuple: (new_id: int, description: str, label: list, task_line: str)
            - new_id: L'ID assigné à la nouvelle tâche
            - description: La description de la tâche
            - label: Liste des étiquettes, vide si aucune
            - task_line: La ligne formatée à écrire dans le fichier
            
    Note:
        - L'ID est calculé comme max(IDs existants) + 1
        - Si aucune tâche n'existe, l'ID commence à 1
        - La ligne retournée inclut le saut de ligne final
        
    Example:
        >>> add(["1;Tâche existante;None"], "Nouvelle tâche", ["étiquette"])
        (2, 'Nouvelle tâche', ['étiquette'], '2;Nouvelle tâche;étiquette\n')
    """
    # Trouve le prochain ID disponible en analysant les tâches existantes
    parsed_tasks = parse_tasks(tasks)
    if parsed_tasks:
        # Calcule l'ID maximum et ajoute 1
        max_id = max(task[0] for task in parsed_tasks)
        new_id = max_id + 1
    else:
        # Premier ID si aucune tâche n'existe
        new_id = 1

    # Réécriture de labels
    if labels == None:
        labels_list = []
    else:
        labels_list = labels
    
    labels_str = ",".join(labels_list) if labels_list else "None"

    # Formate la ligne pour l'écriture dans le fichier
    new_task_line = f"{new_id};{details};{labels_str}\n"
    return (new_id, details, labels_list, new_task_line)


def modify(tasks, task_id, new_details):
    """
    Modifie la description d'une tâche existante par son ID.
    
    Args:
        tasks (list): Liste des lignes existantes du fichier de tâches
        task_id (str|int): ID de la tâche à modifier
        new_details (str): Nouvelle description pour la tâche
        
    Returns:
        tuple: (found: bool, updated_tasks: list, old_task: tuple)
            - found: True si la tâche a été trouvée et modifiée, False sinon
            - updated_tasks: Liste des tâches mis à jour
            - old_task: Tuple (id, desc, lab) correspondant à l'ancienne tâche
    Note:
        - L'ID peut être fourni comme string ou int, il sera converti
        - Si l'ID n'est pas numérique, retourne (False, [])
        - La liste retournée contient toutes les tâches, modifiée incluse
        
    Example:
        >>> modify(["1;Ancienne tâche;None"], "1", "Nouvelle description")
        (True, [(1, 'Nouvelle description', [])])
    """
    # Validation et conversion de l'ID
    try:
        task_id = int(task_id)
    except ValueError:
        # ID invalide (non numérique)
        return False, []
        
    # Parse les tâches existantes
    parsed_tasks = parse_tasks(tasks)
    found = False
    
    # Recherche et modification de la tâche correspondante
    for i, (tid, desc, lab) in enumerate(parsed_tasks):
        if tid == task_id:
            old_task = (tid, desc, lab)
            parsed_tasks[i] = (tid, new_details, lab)
            found = True
            break
    
    return found, parsed_tasks, old_task
    
def rm(tasks, task_id):
    """
    Supprime une tâche par son ID.
    
    Args:
        tasks (list): Liste des lignes existantes du fichier de tâches
        task_id (str|int): ID de la tâche à supprimer
        
    Returns:
        tuple: (found: bool, remaining_tasks: list, old_task: tuple)
            - found: True si la tâche a été trouvée et supprimée, False sinon
            - remaining_tasks: Liste des tâches restantes
            - old_task: Tuple (id, desc, lab) correspondant à l'ancienne tâche
            
    Note:
        - L'ID peut être fourni comme string ou int, il sera converti
        - Si l'ID n'est pas numérique, retourne (False, tâches_originales)
        - Les IDs des autres tâches ne sont pas réassignés
        
    Example:
        >>> rm(["1;Tâche 1;None", "2;Tâche 2;None"], "1")
        (True, [(2, 'Tâche 2', [])])
    """
    # Validation et conversion de l'ID
    try:
        task_id = int(task_id)
    except ValueError:
        # ID invalide, retourne les tâches non modifiées
        return False, parse_tasks(tasks)
        
    # Parse les tâches existantes
    parsed_tasks = parse_tasks(tasks)
    original_length = len(parsed_tasks)
    
    # Filtre les tâches pour enlever celle avec l'ID spécifié
    for (tid, desc, lab) in parsed_tasks:  
        filtered_tasks = []
        if tid != task_id:
            filtered_tasks.append((tid, desc, lab))
        else:
            old_task = (tid, desc, lab)
    
    # Détermine si une tâche a été supprimée
    found = len(filtered_tasks) < original_length
    if not found:
        old_task = None
    return found, filtered_tasks, old_task
            
def addLabel(tasks, task_id, labels):
    """
    Ajoute une ou plusieurs étiquette(s) à une tâche existante.

    Args:
        tasks (list): Liste des lignes existantes du fichier de tâches
        task_id (str|int): ID de la tâche à modifier
        labels (list[str]): Liste d'étiquette(s) à ajouter

    Returns:
        tuple: (found: bool, updated_tasks: list, old_task: tuple)
            - found: True si la tâche a été trouvée et modifiée, False sinon
            - updated_tasks: Liste des tuples (id: int, description: str, labels: list[str]) représentant toutes les tâches
            - old_task: Tuple (id, desc, lab) correspondant à l'ancienne tâche

    Note:
        - L'ID peut être fourni comme string ou int, il sera converti
        - Si l'ID n'est pas numérique, retourne (False, [])
        - La liste retournée contient toutes les tâches, ajout inclus
        
    Example:
        >>> addLabel(["1;Ancienne tâche;None"], "1", ["étiquette1", "étiquette2"])
        (True, [(1, 'Ancienne tâche', ['étiquette1', 'étiquette2'])])
    """

    # Validation et conversion de l'ID
    try:
        task_id = int(task_id)
    except ValueError:
        # ID invalide (non numérique)
        return False, []
        
    # Parse les tâches existantes
    parsed_tasks = parse_tasks(tasks)
    found = False
    
    # Recherche et modification de la tâche correspondante
    for i, (tid, desc, lab) in enumerate(parsed_tasks):
        if tid == task_id:
            old_task = (tid, desc, lab)
            # Initialisation de la liste des étiquettes
            new_lab = [] if lab is None else lab[:]
            for label in labels:
                if label not in new_lab:  # Éviter les doublons
                    new_lab.append(label)
            # Modification de la tâche avec les nouvelles étiquettes
            parsed_tasks[i] = (tid, desc, new_lab)
            found = True
            break
    
    return found, parsed_tasks, old_task



def rmLabel(tasks, task_id):
    """
    Supprime une étiquette d'une tâche existante en demandant à l'utilisateur quelle étiquette supprimer

    Args:
        tasks (list): Liste des lignes existantes du fichier de tâches
        task_id (str|int): ID de la tâche à modifier

    Returns:
        tuple: (found: bool, updated_tasks: list, old_task: tuple)
            - found: True si la tâche a été trouvée et modifiée, False sinon
            - updated_tasks: Liste des tuples (id: int, description: str, labels: list[str]) représentant toutes les tâches 
            - old_task: Tuple (id, desc, lab) correspondant à l'ancienne tâche
    Note:
        - L'ID peut être fourni comme string ou int, il sera converti
        - Si l'ID n'est pas numérique, retourne (False, tâches_originales)
        - Ne gère pas une mauvaise entrée de l'utilisateur (non entier)
        
    Example:
        >>> rmLabel(["1;Tâche 1;None", "2;Tâche 2;Etiquette1, Etiquette2"], "1")
        1: Etiquette1, 2: Etiquette2
        >>> 1
        (True, [(1, 'Tâche 1', []), (2, 'Tâche 2', ["Etiquette2"])])
    """
    
    # Validation et conversion de l'ID
    try:
        task_id = int(task_id)
    except ValueError:
        # ID invalide (non numérique)
        return False, []
        
    # Parse les tâches existantes
    parsed_tasks = parse_tasks(tasks)
    found = False
    
    # Recherche et modification de la tâche correspondante
    for i, (tid, desc, lab) in enumerate(parsed_tasks):
        if tid == task_id:
            old_task = (tid, desc, lab[:])
            if lab:
                print("Étiquettes de la tâche :")
                for j, label in enumerate(lab):
                    print(f"{j}: {label}")
                
                # Validation robuste de l'entrée utilisateur
                while True:
                    try:
                        n = int(input("Entrez le numéro de l'étiquette à supprimer : "))
                        if 0 <= n < len(lab):
                            break
                        else:
                            print(f"Le numéro doit être entre 0 et {len(lab)-1}")
                    except ValueError:
                        print("Erreur : veuillez entrer un nombre valide")
                    except KeyboardInterrupt:
                        print("\nOpération annulée")
                        return False, parsed_tasks
            
                # Suppression de l'étiquette
                lab.pop(n)
                parsed_tasks[i] = (tid, desc, lab)
            else:
                print("Cette tâche n'a pas d'étiquettes à supprimer")
            found = True
            break
    
    return found, parsed_tasks, old_task


def clearLabel(tasks, task_id):
    """
    Supprime l'ensemble des étiquettes d'une tâche en utilisant son ID

    Args:
        tasks (list): Liste des lignes existantes du fichier de tâches
        task_id (str|int): ID de la tâche à modifier

    Returns:
        tuple: (found: bool, updated_tasks: list, old_task: tuple)
            - found: True si la tâche a été trouvée et modifiée, False sinon
            - updated_tasks: Liste des tuples (id: int, description: str, labels: list[str]) représentant toutes les tâches
            - old_task: Tuple (id, desc, lab) correspondant à l'ancienne tâche

    Note:
        - L'ID peut être fourni comme string ou int, il sera converti
        - Si l'ID n'est pas numérique, retourne (False, tâches_originales)
        
    Example:
        >>> clearLabel(["1;Tâche 1;None", "2;Tâche 2;Etiquette1, Etiquette2"], "2")
        (True, [(1, 'Tâche 1', []), (2, 'Tâche 2', [])])
    """
    
    # Validation et conversion de l'ID
    try:
        task_id = int(task_id)
    except ValueError:
        # ID invalide (non numérique)
        return False, []
        
    # Parse les tâches existantes
    parsed_tasks = parse_tasks(tasks)
    found = False
    
    # Recherche et modification de la tâche correspondante
    for i, (tid, desc, lab) in enumerate(parsed_tasks):
        if tid == task_id:
            old_task = (tid, desc, lab)
            parsed_tasks[i] = (tid, desc, [])
            found = True
            break
    
    return found, parsed_tasks, old_task

def show(tasks):
    """
    Affiche la liste des tâches dans un tableau formaté, triées par ID.
    
    Args:
        tasks (list): Liste des lignes du fichier de tâches
        
    Returns:
        None: Affiche directement le résultat sur stdout
        
    Note:
        - Affiche "No tasks found." si aucune tâche n'existe
        - Le tableau s'adapte automatiquement à la longueur des descriptions
        - Les tâches sont automatiquement triées par ID croissant
        - Format du tableau: +-----+-------------+-----------------------------------------+
                             | id  | description | étiquette1, étiquette2, ..., étiquetten |
                             +-----+-------------+-----------------------------------------+
                           
    Example:
        >>> show(["2;Seconde tâche;None", "1;Première tâche;étiquette1,étiquette2"])
        +-----+---------------+------------------------+
        | id  | description   | étiquettes             |
        +-----+---------------+------------------------+
        | 1   | Première tâche| étiquette1, étiquette2 |
        | 2   | Seconde tâche | None                   |
        +-----+---------------+------------------------+
    """
    # Parse et vérifie s'il y a des tâches
    parsed_tasks = parse_tasks(tasks)
    if not parsed_tasks:
        print("No tasks found.")
        return
    
    # Trie les tâches par ID croissant
    sorted_tasks = sorted(parsed_tasks, key=lambda x: x[0])
    
    # Calcule la largeur optimale pour la colonne description
    max_desc_length = max(len(desc) for _, desc, _ in sorted_tasks) if sorted_tasks else 10
    max_desc_length = max(max_desc_length, 11)  # Largeur minimale pour "description"
    
    # Calcule la largeur optimale pour la colonne étiquette(s)
    max_lab_length = max(len(", ".join(lab)) for _, _, lab in sorted_tasks) if sorted_tasks else 11
    max_lab_length = max(max_lab_length, 12)  # Largeur minimale pour "étiquette(s)"

    # Construction et affichage du tableau
    border_line = f"+-----+{'-' * (max_desc_length + 2)}+{'-' * (max_lab_length + 2)}+"
    header_line = f"| {'id':<3} | {'description':<{max_desc_length}} | {'étiquette(s)':<{max_lab_length}} |"
    
    print(border_line)
    print(header_line)
    print(border_line)
    
    # Affichage de chaque tâche
    for task_id, description, labels in sorted_tasks:
        labels_str = ", ".join(labels) if labels else "None"
        print(f"| {task_id:<3} | {description:<{max_desc_length}} | {labels_str:{max_lab_length}} |")
    
    print(border_line)