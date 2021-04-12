"""
Project 4 of OpenClassRooms Cursus:
Développez un programme logiciel en Python
"""


class Tournament:
    def __init__(self):
        self.name = ''
        self.location = ''
        self.date = []  # list because they think about playing during several days
        self.round_number = 4
        self.rounds = []
        self.players = []
        self.time_control = ''  # ['bullet', 'blitz', 'coup rapide']
        self.description = ''


class Player:
    def __init__(self):
        self.last_name = ''
        self.first_name = ''
        self.date_of_birth = ''
        self.sexe = ''
        self.rank = 0  # positive number only


class Match:
    def __init__(self):
        self.results = ([playerInstance1, score1], [playerInstance2, score2])  # client requests


class Round:
    def __init__(self):
        self.matchs = []
        self.name = 'Round'  # to be filled to get 'Round1', 'Round2' ...
        self.start = ''  # date and hour when a round instance is created (filled automatically)
        self.end = ''  # date and hour when a round instance is marked as ended by user (filled automatically)
        self.round_ended = False  # Boolean to check if round is ended by user

