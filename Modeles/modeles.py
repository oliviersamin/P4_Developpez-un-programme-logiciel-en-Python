"""
Project 4 of OpenClassRooms Cursus:
'Développez un programme logiciel en Python'
"""

import time as t
from operator import attrgetter

import config as cf


class Tournament:
    """ model following the client requests """
    def __init__(self):
        # attributes asked by client
        self.name = ''
        self.location = ''
        self.date = ''
        self.round_number = ''
        self.rounds = []
        self.players = []
        self.time_control = ''  # ['bullet', 'blitz', 'coup rapide']
        self.description = ''
        # attributes for program use
        self.tournament_started = False  # used to know if the user started a new tournament
        self.tournament_ended = False  # used to know if the tournament is finished (for database purposes)

    @property
    def serialize(self) -> dict:
        """ serialize the instance into a dictionary """
        dico = {}
        # serialize all the attributs
        for key, value in self.__dict__.items():
            dico.update({key: value})
        players = []
        rounds = []
        # serialize and update self.players in dico
        if self.players:
            for elem in self.players:
                players.append(elem.serialize_player())
        else:
            players = self.players
        dico.update({'players': players})
        # serialize and update self.rounds in dico
        if not self.rounds:
            rounds = self.rounds
        else:
            for elem in self.rounds:
                rounds.append(elem.serialize_round())
        dico.update({'rounds': rounds})
        return dico

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
        matches = []
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

        elif (len(self.rounds) > 1) & (len(self.rounds) <= int(self.round_number)):
            # sort the players by total points and then by rank if needed
            sorted_players = sorted(self.players, key=attrgetter("tournament_total_points", "rank"), reverse=True)
            first_half = sorted_players[:4]
            second_half = sorted_players[4:]
            # select an opponent that has not been played so far
            for index, p_fh in enumerate(first_half):
                num = len(p_fh.opponents)
                for ind, p_sh in enumerate(second_half):
                    if p_sh.id not in p_fh.opponents:
                        p_fh.opponents.append(p_sh.id)
                        second_half.pop(ind)
                        matches.append((p_fh, p_sh))
                        break
                if num == len(p_fh.opponents):
                    print('prendre un joueur dans la liste first_half')
            return matches

        else:
            print('dans generate_pairs_swiss, PROBLÈME!!!!')

    def from_serialized_to_instance(self, serialized_tournament: dict) -> None:
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
    """ model following the client requests """
    def __init__(self):
        # attributes asked by client
        self.id = 0
        self.last_name = ''
        self.first_name = ''
        self.date_of_birth = ''
        self.sex = ''
        self.rank = 0  # positive number only
        # attributes for program used
        self.tournament_total_points = 0  # used to sort the players for the rounds of tournament and display the
        # tournament results
        self.opponents = []  # used for generating swiss pairs for matches

    def serialize_player(self) -> dict:
        """ serialize a player instance into a dictionary with the following structure:
         dico = {'name': player.name, }"""
        dico = {}
        for key, value in self.__dict__.items():
            dico.update({key: value})
        return dico

    def from_serialized_data_to_instance(self, serialized_data: dict) -> None:
        """ create an instance from a serialized data entered in parameter and coming from database"""
        for key, value in serialized_data.items():
            setattr(self, key, value)


class Match:
    """ model following the client requests """
    def __init__(self, player1: object, player2: object):
        """ initialize variables """
        self.player1 = player1  # instance of Player
        self.player2 = player2  # instance of Player
        self.score_player1 = None
        self.score_player2 = None
        self.results = ([self.player1, self.score_player1],
                        [self.player2, self.score_player2])  # client requests

    def set_results(self, score1: float, score2: float):
        """ once scores entered by user, update data """
        self.score_player1 = score1
        self.score_player2 = score2
        # self.results = ([self.player1, self.score_player1],
        #                 [self.player2, self.score_player2])

    def serialize_match(self) -> dict:
        """ serialize the instance into a dictionary """
        return {'player1': self.player1.serialize_player(),
                'player2': self.player2.serialize_player(),
                'score_player1': self.score_player1,
                'score_player2': self.score_player2}

    def from_serialized_to_instance(self, serialized_data: dict):
        """ transform serialized data from database into Match instance """
        for key, value in serialized_data.items():
            # if (key == 'player1') or (key == 'player2'):
            if key in ['player1', 'player2']:
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
        # attributes requested by client
        self.matches = []
        self.name = ''  # to be filled to get 'Round1', 'Round2' ...
        self.time_start = self.generate_time()  # date and hour when a round instance is created (filled automatically)
        self.time_end = ''  # date and hour when a round instance is marked as ended by user (filled automatically)
        # attribute for program use
        self.closed = False  # to be used by database to know at which step is the tournament

    @staticmethod
    def generate_time() -> str:
        """ generate datetime when the round is created, return the time to setup: time_start or time_end
        with the time format given in the config file"""
        time = t.localtime()
        return t.strftime(cf.TIME_FORMAT, time)

    def serialize_round(self) -> dict:
        """ serialize the instance into a dictionary for the database"""
        matches = []
        if not self.matches:
            matches = self.matches
        else:
            for elem in self.matches:
                matches.append(elem.serialize_match())

        return {'name': self.name, 'time_start': self.time_start,
                'time_end': self.time_end, 'matches': matches, 'closed': self.closed}

    def from_serialized_to_instance(self, serialized_data: dict):
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
