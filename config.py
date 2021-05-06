import os


########################################################################################
#               GUI CONFIG
########################################################################################


# ############### config of windows and main title  ##################################

title_main_window = "Centre d'echecs"
size_main = "550x300"
size_tournament = "550x380"
size_add_player = "550x350"
size_left_window = "550x400"
size_round_in_progress = "550x350"
size_closing_round = "550x450"

# ############################# config of the left window  ###################################

# for display_dictionary --> first key = tournament status,
# second key = players registered, third key = round in progress
# display_dictionary = {'Statut tournoi': 'non cree', 'Joueurs': '0/8', 'Tour en cours': 'aucun',
# 'Tour cloture': 'aucun'}
left_window_default_display = {'Tournoi': 'non cree', 'Joueurs': '0/8', 'Tour en cours': 'aucun'}

# values to enter in the dictionary when user has completed steps
# tournament created
update_tournament = 'en cours'
# all the players registered
update_players = '8/8'

# variable used also in the controller file to control gui behavior
# name and path to text file containing json data from gui to be used by controller
update_menus_file = 'menus_states.txt'
path_state_file = os.path.join(os.path.abspath(os.path.curdir), update_menus_file)

########################################################################################
#               GUI CONFIG
########################################################################################

# ################################config the main menus  #######################################@

# 'name' is the name of the menu then 'unfold' provides all the submenu with a dictionary containing
# first the label and second the function to be executed when selected

# fields name for tournament creation window. The keys correspond to the attribut of the
# Tournament class in the modeles file
number_of_players = 8
number_of_rounds = 4
title_window_display_matches_of_round = 'Matchs a jouer pour ce round'
score_winner_match = 1
score_loser_match = 0
score_even_match = 0.5

# fields for rounds and matches
timeformat = '%d/%m/%Y - %H:%M'  # save the date and time with the following format 'day/month/year - hour:minutes'

labels_tournament_creation = {'name': 'Nom du tournoi', 'location': 'Lieu', 'date': 'date',
                              'round_number': 'Nombre de tours', 'time_control': 'Contrôle du temps',
                              'description': 'Description'}

labels_add_players = {'last_name': 'Nom de famille', 'first_name': 'Prenom', 'date_of_birth': 'Date de naissance',
                      'sexe': 'Sexe', 'rank': 'Classement'}

labels_round_creation = {'name': 'nom du tour'}

# configuration for database with TinyDB
data_base_file_name = 'db.json'
table_players = 'players'
table_tournament = 'tournament'
list_tables = [table_tournament, table_players]

# json file configuration
json_file_name = 'program_state.json'
json_file_path = os.path.join(os.path.abspath(os.path.curdir), json_file_name)
