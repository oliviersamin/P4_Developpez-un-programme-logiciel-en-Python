########################################################################################
#               GUI CONFIG
########################################################################################

# ############### config of windows and main title  ##################################

title_main_window = "Centre d'échecs"
size_main = "550x300"
size_tournament = "550x380"
size_add_player = "550x350"
size_left_window = "550x400"
size_round_in_progress = "550x350"
size_closing_round = "550x450"

# ################################other GUI config ##############################

title_window_display_matches_of_round = 'Matchs a jouer pour ce round'

labels_tournament_creation = {'name': 'Nom du tournoi', 'location': 'Lieu', 'date': 'date',
                              'round_number': 'Nombre de tours', 'time_control': 'Contrôle du temps',
                              'description': 'Description'}

labels_add_players = {'last_name': 'Nom de famille', 'first_name': 'Prénom', 'date_of_birth': 'Date de naissance',
                      'sexe': 'Sexe', 'rank': 'Classement'}

labels_round_creation = {'name': 'nom du tour'}

number_of_rounds = 4

# ######################################## controller config ###################################################
number_of_players = 8

# fields for rounds and matches
time_format = '%d/%m/%Y - %H:%M'  # save the date and time with the following format 'day/month/year - hour:minutes'
score_winner_match = 1
score_loser_match = 0
score_even_match = 0.5


# ##################################### Database config (TinyDB) ################################################
data_base_file_name = 'db.json'
table_players = 'players'
table_tournament = 'tournament'
