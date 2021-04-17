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
# config of errors messages linked with the several steps of the tournament
title_error = "ATTENTION"
tournament_error = 'UN TOURNOI EST DÉJA CRÉÉ'
players_error = "Créez un tournoi avant de créer des joueurs"
round_start_error = "Créez les joueurs avant de lancer un round"
round_end_error = "Créez un tour avant de le finir"

# ################################config the main menus  #######################################@

# 'name' is the name of the menu then 'unfold' provides all the submenu with a dictionnary containing
# first the label and second the function to be executed when selected
menus_main = [{'name': "tournoi actuel",
               'unfold': [{'label': "Créer le tournoi",
                           'function': "lambda i= 'tournament_start': self.request_controler_tournament(i)"},
                          {'label': "Ajouter les joueurs",
                           'function': "lambda i= 'add_players': self.request_controler_tournament(i)"},
                          {'label': "Lancer le tour",
                           'function': "lambda i= 'launch_round': self.request_controler_tournament(i)"},
                          {'label': 'Cloturer le tour',
                           'function': "lambda i= 'close_round': self.request_controler_tournament(i)"}]},
              {'name': "ouvrir / sauvegarder le tournoi",
               'unfold': [{'label': "Ouvrir un tournoi sauvegardé", 'function': 'self.test'},
                          {'label': "Sauvegarder le tournoi en cours", 'function': 'self.test'}]},
              {'name': "générer les rapports",
               'unfold': [{'label': "liste de tous les acteurs", 'function': 'self.test'},
                          {'label': "liste des joueurs du tournoi actuel", 'function': 'self.test'},
                          {'label': "liste de tous les tournois", 'function': 'self.test'},
                          {'label': "liste de tous les tours d'un tournoi", 'function': 'self.test'},
                          {'label': "liste de tous les matchs d'un tournoi", 'function': 'self.test'}]}]

# ############################# config of the left window  ###################################

# for display_dictionnary --> first key = tournament status,
# second key = players registered, third key = round in progress
display_dictionary = {'Statut tournoi': 'non créé', 'Joueurs': '0/8', 'Tour en cours': 'aucun'}
# values to enter in the dictionnary when user has completed steps
# tournament created
update_tournament = 'en cours'
# all the players registered
update_players = '8/8'

########################################################################################
#               CONTROLER CONFIG
########################################################################################
# config of the requests parameters to use to communicate with the GUI (method request_controler_tournament
# in the MainWindow class

tournament_start = False
add_players = True
launch_round = True
close_round = True

# ############################  WARNING  #########################
# the names used in this dictionnary MUST BE THE SAME as the i in the lambda functions of menus_main
# ################################################################

authorization = [{'name': 'tournament_start', 'class': 'CreateNewTournament', 'size': size_tournament,
                  'variable_name': tournament_start, 'error_message': tournament_error},
                 {'name': 'add_players', 'class': 'AddPlayers', 'size': size_add_player,
                  'variable_name': add_players, 'error_message': players_error},
                 {'name': 'launch_round', 'class': 'LaunchRound', 'size': size_round_in_progress,
                  'variable_name': launch_round, 'error_message': round_start_error},
                 {'name': 'close_round', 'class': 'CloseRound', 'size': size_closing_round,
                  'variable_name': close_round, 'error_message': round_end_error}
                 ]
