"""
Project 4 of OpenClassRooms Cursus:
Developpez un programme logiciel en Python
"""

import time as t
from operator import attrgetter

import config as cf


class Tournament:
    def __init__(self):
        self.name = ''
        self.location = ''
        self.date = ''
        self.round_number = ''
        self.rounds = []
        self.players = []
        self.time_control = ''  # ['bullet', 'blitz', 'coup rapide']
        self.description = ''
        self.tournament_started = False
        self.tournament_ended = False

    @property
    def serialize(self):
        """ serialize the instance into a dictionary """
        # serialize self.players
        dico = {}
        for key, value in self.__dict__.items():
            dico.update({key: value})
        players = []
        rounds = []
        if self.players is not []:
            for elem in self.players:
                players.append(elem.serialize_player())
        else:
            players = self.players
        dico.update({'players': players})
        # serialize self.rounds

        if self.rounds is []:
            rounds = self.rounds
        else:
            for elem in self.rounds:
                rounds.append(elem.serialize_round())
        dico.update({'rounds': rounds})
        return dico
        # return {'name': self.name, 'location': self.location, 'date': self.date,
        #         'round_number': self.round_number, 'time_control': self.time_control,
        #         'description': self.description, 'rounds': rounds, 'players': players}

    def generate_pairs_swiss(self) -> list:
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

        elif (len(self.rounds) > 1) & (len(self.rounds) <= cf.number_of_rounds):
            print('dans generate_pairs_swiss, round >1 et <{}:\n'.format(cf.number_of_rounds))
            # sort the players by total points and then by rank if needed
            sorted_players = sorted(self.players, key=attrgetter("tournament_total_points", "rank"), reverse=True)
            print('dans generate_pairs_swiss: ', sorted_players)
            for elem in sorted_players:
                print(elem.id, elem.tournament_total_points, elem.rank, elem.opponents)
            first_half = sorted_players[:4]
            second_half = sorted_players[4:]
            # select an opponent that has not been played so far
            print('verif players n ont pas deja joue ensemble A FAIRE')

            # create matches
            matches = [(player_fh, player_sh) for player_fh, player_sh in zip(first_half, second_half)]
            return matches

        else:
            print('dans generate_pairs_swiss, PROBLEME!!!!')

    def from_serialized_to_instance(self, serialized_tournament):
        """ use a serialized data from database to convert it into a tournament instance """
        for key, value in serialized_tournament.items():
            if key == 'rounds':
                result = []
                for tour in value:
                    # print('round = ', round)
                    r = Round()
                    r.from_serialized_to_instance(tour)
                    # print(type(r), r.__dict__)
                    result.append(r)
                setattr(self, key, result)
            elif key == 'players':
                result = []
                for player in value:
                    p = Player()
                    p.from_serialized_data_to_instance(player)
                    result.append(p)
                setattr(self, key, result)
            else:
                setattr(self, key, value)


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

    def from_serialized_data_to_instance(self, serialized_data):
        """ create an instance from a serialized data entered in parameter """
        for key, value in serialized_data.items():
            setattr(self, key, value)


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

    def from_serialized_to_instance(self, serialized_data):
        """ transform serialized data from database into Match instance """
        for key, value in serialized_data.items():
            if (key == 'player1') or (key == 'player2'):
                p = Player()
                p.from_serialized_data_to_instance(value)
                # print(p)
                setattr(self, key, p)
            elif key == 'results':
                pass
            else:
                setattr(self, key, value)
            self.results = ([self.player1, self.score_player1], [self.player2, self.score_player2])


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

    def from_serialized_to_instance(self, serialized_data):
        """ transform serialized data from database into Round instance """
        for key, value in serialized_data.items():
            if key == 'matches':
                result = []
                for match in value:
                    m = Match(Player(), Player())
                    m.from_serialized_to_instance(match)
                    result.append(m)
                    setattr(self, key, result)
            else:
                setattr(self, key, value)
