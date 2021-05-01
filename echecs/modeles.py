"""
Project 4 of OpenClassRooms Cursus:
Developpez un programme logiciel en Python
"""

import time as t
from operator import attrgetter

import config as cf


class Tournament:
    def __init__(self) -> None:
        self.name = ''
        self.location = ''
        self.date = ''
        self.round_number = ''
        self.rounds = []
        self.players = []
        self.time_control = ''  # ['bullet', 'blitz', 'coup rapide']
        self.description = ''

    @property
    def serialize(self):
        """ serialize the instance into a dictionary """
        # serialize self.players
        players = []
        if self.players is not []:
            for elem in self.players:
                players.append(elem.serialize_player())
        else:
            players = self.players

        # serialize self.rounds
        rounds = []
        if self.rounds is []:
            rounds = self.rounds
        else:
            for elem in self.rounds:
                rounds.append(elem.serialize_round())

        return {'name': self.name, 'location': self.location, 'date': self.date,
                'round_number': self.round_number, 'time_control': self.time_control,
                'description': self.description, 'rounds': rounds, 'players': players}

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
            # sort the players by total points and then by rank if needed
            print('dans generate_pairs_swiss, a finaliser triage des players')
            sorted_players = sorted(players, key=attrgetter("tournament_total_points", "rank"))
            # check that players did not play together before in this tournament
            print('verif players n ont pas deja joue ensemble A FAIRE')
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
        self.tournament_total_points = 0  # used to sort the players for the rounds of tournament
        self.opponents = []

    def serialize_player(self):
        """ serialize a player instance into a dictionary with the following structure:
         dico = {'name': player.name, }"""
        dico = {}
        for key, value in self.__dict__.items():
            dico.update({key: value})
        return dico
        # return {'id': self.id, 'last_name': self.last_name, 'first_name': self.first_name,
        #         'date_of_birth': self.date_of_birth, 'sex': self.sex, 'rank': self.rank, }

    def create_instance_from_serialized_data(self, numero_id, data):
        """ create an instance from a serialized data entered in parameter """
        print('dans create_instance_from_serialized_data A REPPRENDRE avec des setattr()')
        self.last_name = data['nom_de_famille']
        self.first_name = data['prenom']
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

    def serialize_match(self):
        """ serialize the instance into a dictionary """
        return {'player1': self.player1.serialize_player(),
                'player2': self.player2.serialize_player(),
                'score_player1': self.score_player1,
                'score_player2': self.score_player2}


class Round:
    """  model following the client requests """

    def __init__(self):
        """ initialize variables """
        self.matches = []
        self.name = ''  # to be filled to get 'Round1', 'Round2' ...
        self.time_start = self.generate_time()  # date and hour when a round instance is created (filled automatically)
        self.time_end = ''  # date and hour when a round instance is marked as ended by user (filled automatically)
        self.closed = False  # to know the state of the round when saved

    @staticmethod
    def generate_time():
        """ generate datetime when the round has been created
         return the time to setup: time_start or time_end with the timeformat given in
         the config file"""
        time = t.localtime()
        return t.strftime(cf.timeformat, time)

    def serialize_round(self):
        """ serialize the instance into a dictionary """
        matches = []
        if self.matches is []:
            matches = self.matches
        else:
            for elem in self.matches:
                matches.append(elem.serialize_match())

        return {'name': self.name, 'time_start': self.time_start,
                'time_end': self.time_end, 'matches': matches, 'closed': self.closed}
