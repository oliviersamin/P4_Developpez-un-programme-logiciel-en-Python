import os

########################################################################################
#               GUI CONFIG
########################################################################################


# ############### config of windows and main title  ##################################

title_main_window = "Centre d'échecs"
size_main = "550x300"
size_tournament = "550x380"
size_add_player = "550x350"
size_left_window = "550x400"
size_round_in_progress = "550x300"
size_closing_round = "550x450"

# ############################# config of the left window  ###################################

# for display_dictionnary --> first key = tournament status,
# second key = players registered, third key = round in progress
display_dictionary = {'Statut tournoi': 'non créé', 'Joueurs': '0/8', 'Tour en cours': 'aucun'}
# values to enter in the dictionnary when user has completed steps
# tournament created
update_tournament = 'en cours'
# all the players registered
update_players = '8/8'

# variable used also in the controller file to control gui behavior
authorization = [{'name': 'tournament_start', 'label': "Créer le tournoi", 'class': 'CreateNewTournament',
                  'size': size_tournament, 'state': 'normal'},
                 {'name': 'add_players', 'label': "Ajouter les joueurs", 'class': 'AddPlayers',
                  'size': size_add_player, 'state': 'disabled'},
                 {'name': 'launch_round', 'label': "Lancer le tour", 'class': 'LaunchRound',
                  'size': size_round_in_progress, 'state': 'disabled'},
                 {'name': 'close_round', 'label': 'Cloturer le tour', 'class': 'CloseRound',
                  'size': size_closing_round, 'state': 'disabled'}]

# name and path to text file containing json data from gui to be used by controller
update_menus_file = 'menus_states.txt'
path_state_file = os.path.join(os.path.abspath(os.path.curdir),update_menus_file)

########################################################################################
#               GUI CONFIG
########################################################################################

# ################################config the main menus  #######################################@

# 'name' is the name of the menu then 'unfold' provides all the submenu with a dictionnary containing
# first the label and second the function to be executed when selected
menus_main = [{'name': "tournoi actuel",
               'unfold': [{'label': elem['label'], 'state': elem['state'],
                           'function': "lambda i= '"+elem['name']+"': self.display_right_window(i)"}
                          for elem in authorization]},
              {'name': "ouvrir / sauvegarder le tournoi",
               'unfold': [{'label': "Ouvrir un tournoi sauvegardé",  'state': 'normal',
                           'function': 'self.test'},
                          {'label': "Sauvegarder le tournoi en cours",  'state': 'disabled',
                           'function': 'self.test'}]},
              {'name': "générer les rapports",
               'unfold': [{'label': "liste de tous les acteurs", 'state': 'disabled',
                           'function': 'self.test'},
                          {'label': "liste des joueurs du tournoi actuel", 'state': 'disabled',
                           'function': 'self.test'},
                          {'label': "liste de tous les tournois", 'state': 'disabled',
                           'function': 'self.test'},
                          {'label': "liste de tous les tours d'un tournoi", 'state': 'disabled',
                           'function': 'self.test'},
                          {'label': "liste de tous les matchs d'un tournoi", 'state': 'disabled',
                           'function': 'self.test'}]}]

# field name for tournament creation window.
labels_tournament_creation = ['Nom du tournoi', 'Lieu', 'date', 'Nombre de tours', 'Contrôle du temps', 'Description']
