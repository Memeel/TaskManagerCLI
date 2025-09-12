"""
Ce module configure l'analyseur de ligne de commande en utilisant argparse.
Il définit la structure des commandes disponibles et leurs arguments.

Structure CLI:
    python task.py <fichier> <commande> [arguments]

Commandes disponibles:
    - add <description> -l <labels>       : Ajoute une nouvelle tâche
    - modify <id> <description>           : Modifie une tâche existante
    - rm <id>                             : Supprime une tâche
    - addLabel <id> <labels>              : Ajoute une étiquette
    - rmLabel <id>                        : Supprime une étiquette d'une tâche
    - clearLabel <id>                     : Supprime toutes les étiquettes d'une tâche
    - show                                : Affiche toutes les tâches
"""

import argparse


def create_parser():
    """
    Crée et configure l'analyseur de ligne de commande.
    
    Returns:
        argparse.ArgumentParser: Parseur configuré avec toutes les commandes
        
    Note:
        Utilise des sous-parseurs pour gérer les différentes commandes.
        Chaque commande a ses propres arguments spécifiques.
    """
    # Création du parseur principal
    parser = argparse.ArgumentParser(
        description='Simple task manager - Gestionnaire de tâches en ligne de commande',
        epilog='Exemple: python task.py lestaches.txt add "Faire les courses"'
    )
    
    # Argument positionnel obligatoire : le fichier de tâches
    parser.add_argument(
        'file', 
        help='Chemin vers le fichier contenant les tâches'
    )
    
    # Sous-parseurs pour les différentes commandes
    subparsers = parser.add_subparsers(
        help='Commandes disponibles pour gérer les tâches', 
        dest='command', 
        required=True,
        metavar='COMMANDE'
    )
    
    # === Commande ADD ===
    parser_add = subparsers.add_parser(
        'add', 
        help='Ajouter une nouvelle tâche',
        description='Ajoute une nouvelle tâche avec la description fournie et son/ses étiquettes si fournie(s)'
    )
    parser_add.add_argument(
        'details', 
        nargs='*', 
        default=["no details"], 
        help="Description de la tâche (plusieurs mots acceptés)"
    )
    parser_add.add_argument(
        '-l', '--labels',
        nargs='*',
        help='Etiquettes optionnelles pour la tâche'
    )
    parser_add.add_argument(
        '--statut',
        help='Statut de la tâche : started, suspended, completed ,cancelled(par défaut suspended) '
    )
    
    # === Commande MODIFY ===
    parser_modify = subparsers.add_parser(
        'modify', 
        help='Modifier une tâche existante',
        description='Modifie la description d\'une tâche en utilisant son ID'
    )
    parser_modify.add_argument(
        'id', 
        help="ID numérique de la tâche à modifier"
    )
    parser_modify.add_argument(
        'details', 
        nargs='*', 
        default=["no details"], 
        help="Nouvelle description de la tâche"
    )
    
    # === Commande RM (Remove) ===
    parser_rm = subparsers.add_parser(
        'rm', 
        help='Supprimer une tâche',
        description='Supprime définitivement une tâche en utilisant son ID'
    )
    parser_rm.add_argument(
        'id', 
        help="ID numérique de la tâche à supprimer"
    )
    # === Commande modifyStatus ===
    parser_updateStatus = subparsers.add_parser(
        'updateStatus',
        help='Ajouter des étiquettes',
        description='modifier le statut pour une tâche existante '
    )
    parser_updateStatus.add_argument(
        'id',
        help="ID numérique de la tâche dont on souhaite modifier le statut"
    )
    # === Commande ADDLABEL ===
    parser_addLabel = subparsers.add_parser(
        'addLabel',
        help='Ajouter des étiquettes',
        description='Ajoute une ou plusieurs étiquettes à une tâche existante (évite automatiquement les doublons)'
    )
    parser_addLabel.add_argument(
        'id',
        help="ID numérique de la tâche dont on souhaite ajouter des étiquettes"
    )
    parser_addLabel.add_argument(
        'labels',
        nargs='+',
        help="Étiquette(s) à ajouter à la tâche (séparées par des espaces)"
    )

    # === Commande RMLABEL ===
    parser_rmLabel = subparsers.add_parser(
        'rmLabel',
        help="Supprimer une étiquette d'une tâche",
        description="Supprime une étiquette d'une tâche existante en demandant à l'utilisateur quelle étiquette supprimer"
    )
    parser_rmLabel.add_argument(
        'id',
        help="ID numérique de la tâche"
    )

    # === Commande CLEARLABEL ===
    parser_clearLabel = subparsers.add_parser(
        'clearLabel',
        help="Supprimer l'ensemble des étiquettes d'une tâche",
        description="Supprime l'ensemble des étiquettes d'une tâche en utilisant son ID"
    )
    parser_clearLabel.add_argument(
        'id',
        help="ID numérique de la tâche dont on veut supprimer les étiquettes"
    )
    
    # === Commande SHOW ===
    parser_show = subparsers.add_parser(
        'show', 
        help='Afficher toutes les tâches',
        description='Affiche la liste de toutes les tâches dans un tableau formaté'
    )
    
    return parser
