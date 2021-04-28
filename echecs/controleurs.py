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

import json
import os

from tinydb import TinyDB

import gui
import config as cf
import modeles as mod

# initialize variables
# tournament that will become an instance of Tournament modeles
tournament = None
# states that will be the core of GUI - controller communication
# for tournament steps control
states = None


class Controls:
    """ control the tournament steps regarding the user inputs """
    @classmethod
    def verify_tournament_creation(cls, info):
        """ verify tournament creation,
         if tournament created, set the menus_states for next step of tournament
         """
        global tournament, states
        # read the menus states sent by GUI
        states = cls.read_menus_states()
        # instructions regarding states
        if tournament is not None:
            print('tournoi déjà créé')
            return {}
        else:
            # create tournament instance from modeles
            tournament = mod.Tournament()
            # set all the attributs regarding the user entries in the GUI
            for key, value in cf.labels_tournament_creation.items():
                setattr(tournament, key, info[value])
            # set the menus states to be able to perform next step of tournament
            for elem in states:
                if elem['name'] == 'tournament_start':
                    elem['state'] = 'disabled'
                    elem['left_window_value'] = tournament.name
                elif elem['name'] == 'add_players':
                    elem['state'] = 'normal'
            # write the new menus states in the file to communicate with GUI
            cls.write_menus_states(states)

    @classmethod
    def verify_players_creation(cls, info):
        """ verify players creation when tournament (instance of Tournament modele) is already created,
         - create Player model for each new player created by user and set its attributs regarding
           the user entries in the GUI.
         - set the menus_states for next step of tournament
         """
        all_players_created = False
        for elem in states:
            # while number fo players created by user is < than number of players defined in config file
            if (elem['name'] == 'add_players') & (len(tournament.players) < cf.number_of_players):
                player = mod.Player()
                tournament.players.append(player)
                for key, value in cf.labels_add_players.items():
                    setattr(player, key, info[value])
                setattr(player, 'id', len(tournament.players))
                elem['left_window_value'] = '{}/{}'.format(len(tournament.players), cf.number_of_players)
                if len(tournament.players) == cf.number_of_players:
                    elem['state'] = 'disabled'
                    for st in states:
                        if st['name'] == 'launch_round':
                            st['state'] = 'normal'
                            break
                    all_players_created = True
                    # for player in tournament.players:
                    #     print(player.__dict__)
        cls.write_menus_states(states)
        return all_players_created

    @classmethod
    def verify_round_creation(cls, info):
        """ verify round creation,
         if round created, set the menus_states for next step of tournament
         """
        global tournament, states
        # read the menus states sent by GUI
        states = cls.read_menus_states()
        # instructions regarding states
        if len(tournament.rounds) < cf.number_of_rounds:
            # create round instance from modeles and save it into the tournament variable
            round_instance = mod.Round()
            tournament.rounds.append(round_instance)
            # set all the attributs regarding the user entries in the GUI
            for key, value in cf.labels_round_creation.items():
                setattr(round_instance, key, info[value])
            # set the menus states to be able to perform next step of tournament
            for elem in states:
                if elem['name'] == 'launch_round':
                    elem['state'] = 'disabled'
                    elem['left_window_value'] = round_instance.name
                elif elem['name'] == 'close_round':
                    elem['state'] = 'normal'
            # write the new menus states in the file to communicate with GUI
            cls.write_menus_states(states)

        # elif len(tournament.rounds) == cf.number_of_rounds:
        #     # create tournament instance from modeles
        #     tournament = mod.Tournament()
        #     # set all the attributs regarding the user entries in the GUI
        #     for key, value in cf.labels_tournament_creation.items():
        #         setattr(tournament, key, info[value])

    @classmethod
    def generate_matches(cls):
        matches = tournament.generate_pairs_swiss()
        for match in matches:
            tournament.rounds[-1].matches.append(mod.Match(match[0], match[1]))
        return matches

    @classmethod
    def get_current_matches(cls):
        return(tournament.rounds[-1].matches)

    @classmethod
    def delete_menus_states(cls):
        """ delete the communication file between GUI and controller.
        First function used in the program to start the GUI with no pre-existing data"""
        try:
            os.remove(cf.path_state_file)
        except FileNotFoundError:
            pass

    @classmethod
    def read_menus_states(cls):
        """ reads the states from the communication file between GUI and controller """
        with open(cf.path_state_file, 'r') as f:
            states_menus = json.load(f)
        return states_menus

    @classmethod
    def write_menus_states(cls, menus_states):
        """ write the menus states into the communication file """
        with open(cf.path_state_file, 'w') as f:
            json.dump(menus_states, f)


class DataBase:
    """ use tinyDB bdd regarding client request to save and open data """

    @classmethod
    def create_data_base_and_tables(cls):
        """ create a database file and the two corresponding tables as requeted
        by the client """
        db = TinyDB(cf.data_base_file_name)
        for table in cf.list_tables:
            db.table(table)

    @classmethod
    def clear_table(cls, table_name):
        """ clear the table from data """
        table_name.truncate()

    @classmethod
    def insert_multiple_data(cls, table_name, data):
        """ insert data in the table_name """
        table_name.insert_multiple(data)

    @classmethod
    def get_all_data_from_database_table(cls, table_name):
        """ get all the data contained in table_name as a list of dictionaries"""
        print('dans get_all_data_from_database_table:\nIdentifier la structure du dico retourné '
              'et entrer cette structure dans le docstring de la fonction')
        return table_name.all()


class SaveOpenTournament:

    @classmethod
    def open_saved_tournament(cls):
        """ open an already saved tournament """

    @classmethod
    def save_current_tournament(cls):
        """ save the current tournament """


class GenerateReports:

    def generate_report(self):
        """ generate report with the parameters """


if __name__ == "__main__":
    # delete menus_state file if it exists to start the program with no pre-existing data
    Controls.delete_menus_states()
    # launch of GUI
    gui.MainWindow().mainloop()
