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

# for display_dictionary --> first key = tournament status,
# second key = players registered, third key = round in progress
display_dictionary = {'Statut tournoi': 'non créé', 'Joueurs': '0/8', 'Tour en cours': 'aucun'}
# values to enter in the dictionary when user has completed steps
# tournament created
update_tournament = 'en cours'
# all the players registered
update_players = '8/8'

# variable used also in the controller file to control gui behavior
authorization = [{'name': 'tournament_start', 'label': "Créer le tournoi", 'class': 'CreateNewTournament',
                  'size': size_tournament, 'state': 'normal',
                  'left_window': {'label': 'Tournoi', 'value': 'non créé'}},
                 {'name': 'add_players', 'label': "Ajouter les joueurs", 'class': 'AddPlayers',
                  'size': size_add_player, 'state': 'disabled',
                  'left_window': {'label': 'Joueurs', 'value': '0/8'}},
                 {'name': 'launch_round', 'label': "Lancer le tour", 'class': 'LaunchRound',
                  'size': size_round_in_progress, 'state': 'disabled',
                  'left_window': {'label': 'Tour en cours', 'value': 'aucun'}},
                 {'name': 'close_round', 'label': 'Cloturer le tour', 'class': 'CloseRound',
                  'size': size_closing_round, 'state': 'disabled',
                  'left_window': {'label': 'Tour terminé', 'value': 'aucun'}}]

# name and path to text file containing json data from gui to be used by controller
update_menus_file = 'menus_states.txt'
path_state_file = os.path.join(os.path.abspath(os.path.curdir), update_menus_file)

########################################################################################
#               GUI CONFIG
########################################################################################

# ################################config the main menus  #######################################@

# 'name' is the name of the menu then 'unfold' provides all the submenu with a dictionary containing
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

# fields name for tournament creation window. The keys correspond to the attribut of the
# Tournament class in the modeles file
labels_tournament_creation = {'name': 'Nom du tournoi', 'location': 'Lieu', 'date': 'date',
                              'round_number': 'Nombre de tours', 'time_control': 'Contrôle du temps',
                              'description': 'Description'}

labels_add_players = {'last_name': 'Nom de famille', 'first_name': 'Prénom', 'date_of_birth': 'Date de naissance',
                      'sexe': 'Sexe', 'rank': 'Classement'}
