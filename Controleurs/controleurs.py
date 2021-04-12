"""
Project 4 of OpenClassRooms Cursus:
Développez un programme logiciel en Python
From the specs file the Tournament is going through the following steps:
1 - the user creates a new tournament (enter data ...)
2 - the user add 8 players (enter data fore each one)
3 - program generates pairs of players to create matches
4 - At the end of the round ( = end of all matches) user enter the scores
5 - Repeat 3 & 4 until tournament is over

Needed features:
1- save and/or load at any time in between user interaction with program the state of the tournament
2 - generate the following reports:
    a - list of all actors (by alphabetical order or rank)
    b - list of all players of a tournament (by alphabetical order or rank)
    c - List of all tournaments
    d - list of all the rounds of one tournament
    e - list of all matches of one tournament

Generate pairs of players using swiss system:
1 - at the beginning of a tournament class all players with their rank
2 - Divide all the players in the half (half up and half down).
The best of half up is paired with the best of half down and so forth and so on (1 with 5, 2 with 6...)
3 - next round sort the players with their total number of points.
If necessary sort them again with their rank.
"""


class NewTournament:

    def create_tournament_1(self):
        """ the user create a new tournament """

    def add_players_2(self):
        """ the user add 8 players and their associated data """

    def create_new_round(self):
        """ the user starts a new round  the program get the date and hour of its start"""

    def __generate_pairs_3(self):
        """ private method : when all the players are entered by the user,
        the program creates the pairs following the swiss system rules given by the client """

    def enter_round_scores_4(self):
        """ at the end of the round, the user enter the scores for each match,
        the program get the date and hour of its end """

    def __calculate_total_score(self):
        """ private method to automatically calculate total score
        for each player of the tournament """


class OpenSaveTournament:

    def open_saved_tournament(self):
        """ open an already saved tournament """

    def save_current_tournament(self):
        """ save the current tournament """


class GenerateReports:

    def generate_report(self):
        """ generate report with the parameters """
