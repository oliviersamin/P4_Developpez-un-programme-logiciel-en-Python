""" Config file to setup some parameters for the program """

########################################################################################
#               GUI CONFIG
########################################################################################

# ############### config of windows and main title  ##################################

TITLE_MAIN_WINDOW = "Centre d'échecs"
SIZE_MAIN = "550x300"
SIZE_TOURNAMENT = "550x380"
SIZE_ADD_PLAYER = "550x350"
SIZE_LEFT_WINDOW = "550x400"
SIZE_ROUND_IN_PROGRESS = "550x350"
SIZE_CLOSING_ROUND = "550x450"

# ################################other GUI config ##############################

TITLE_WINDOW_DISPLAY_MATCHES_OF_ROUND = 'Matchs a jouer pour ce round'

LABELS_TOURNAMENT_CREATION = {'name': 'Nom du tournoi', 'location': 'Lieu', 'date': 'date',
                              'round_number': 'Nombre de tours', 'time_control': 'Contrôle du temps',
                              'description': 'Description'}

LABELS_ADD_PLAYERS = {'last_name': 'Nom de famille', 'first_name': 'Prénom', 'date_of_birth': 'Date de naissance',
                      'sex': 'Sexe', 'rank': 'Classement'}

LABELS_ROUND_CREATION = {'name': 'nom du tour'}

NUMBER_OF_ROUNDS = 4

# ######################################## controller config ###################################################
NUMBER_OF_PLAYERS = 8

# fields for rounds and matches
TIME_FORMAT = '%d/%m/%Y - %H:%M'  # save the date and time with the following format 'day/month/year - hour:minutes'
SCORE_WINNER_MATCH = 1
SCORE_LOSER_MATCH = 0
SCORE_EVEN_MATCH = 0.5


# ##################################### Database config (TinyDB) ################################################
DATA_BASE_FILE_NAME = 'db.json'
TABLE_PLAYERS = 'players'
TABLE_TOURNAMENT = 'tournament'
