"""
Project 4 of OpenClassRooms Cursus:
Développez un programme logiciel en Python
"""

import time as t

import config as cf


class Tournament:
    def __init__(self):
        self.name = ''
        self.location = ''
        self.date = ''
        self.round_number = 4
        self.rounds = []
        self.players = []
        self.time_control = ''  # ['bullet', 'blitz', 'coup rapide']
        self.description = ''


    def generate_pairs_swiss(self):
        """ generate pairs to create matches following the client requests
         1 - if round 1:
            a - sort players by rank
            b - split the players sorted  in 2 halves
            c - best of first half plays best of second half on so forth and so on
        2 - if round > 1:
            a - sort players by total number of points (from tournament) and if needed then by rank
            b - player 1 vs player 2 ..... (never played together)"""

        # transform rank attribut from string to int to be able to make operations with it
        for elem in self.players:
            elem.rank = int(elem.rank)
        # 1-a
        if len(self.rounds) == 1:
            self.players.sort(key=lambda item: item.rank)
            # 1-b
            first_half = self.players[:4]
            second_half = self.players[4:]
            # 1-c
            matches = [(player_fh, player_sh) for player_fh, player_sh in zip(first_half, second_half)]
            return matches

        elif (len(self.rounds) > 1) & (len(self.rounds) < cf.number_of_rounds):
            print('dans generate_pairs_swiss, round >1 et <{}:\n'.format(cf.number_of_rounds))
            # sort the players by rank

        else:
            print('dans generate_pairs_swiss, PROBLEME!!!!')


class Player:
    def __init__(self):
        self.id = 0
        self.last_name = ''
        self.first_name = ''
        self.date_of_birth = ''
        self.sex = ''
        self.rank = 0  # positive number only

    def serialize_player(self):
        """ serialize a player instance into a dictionary with the following structure:
         dico = {'name': player.name, }"""
        return {'nom_de_famille': self.last_name, 'prénom': self.first_name,
                'date_de_naissance': self.date_of_birth, 'sexe': self.sex, 'classement': self.rank}

    def create_instance_from_serialized_data(self, numero_id, data):
        """ create an instance from a serialized data entered in parameter """
        self.last_name = data['nom_de_famille']
        self.first_name = data['prénom']
        self.date_of_birth = data['date_de_naissance']
        self.sex = data['sexe']
        self.rank = data['classement']
        self.id = numero_id


class Match:
    """ model following the client requests """
    def __init__(self, player1, player2):
        """ initialize variables """
        self.player1 = player1  # instance of Player
        self.player2 = player2  # instance of Player
        self.score_player1 = None
        self.score_player2 = None
        self.results = ([self.player1, self.score_player1],
                        [self.player2, self.score_player2])  # client requests

    def set_results(self, score1, score2):
        """ once scores entered by user, update data """
        self.score_player1 = score1
        self.score_player2 = score2
        # self.results = ([self.player1, self.score_player1],
        #                 [self.player2, self.score_player2])


class Round:
    """  model following the client requests """

    def __init__(self):
        """ initialize variables """
        self.matches = []
        self.name = ''  # to be filled to get 'Round1', 'Round2' ...
        self.time_start = self.generate_time()  # date and hour when a round instance is created (filled automatically)
        self.time_end = ''  # date and hour when a round instance is marked as ended by user (filled automatically)

    def generate_time(self):
        """ generate datetime when the round has been created
         return the time to setup: time_start or time_end with the timeformat given in
         the config file"""
        time = t.localtime()
        return t.strftime(cf.timeformat, time)
