"""
Project 4 of OpenClassRooms Cursus:
Developpez un programme logiciel en Python
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
The best of half up is paired with the best of half down and so forth and so on
(1 with 5, 2 with 6...)
3 - next round sort the players with their total number of points.
If necessary sort them again with their rank.
"""

import json

from tinydb import TinyDB, table

import Vues.gui as gui
import Modeles.modeles as mod
import config as cf


# initialize variables
# tournament that will become an instance of Tournament modeles
# tournament = None
# states that will be the core of GUI - controller communication
# for tournament steps control
states = None
tournament = None
tables = None


class Controls:
    """ control the tournament steps regarding the user inputs """
    @classmethod
    def send_order_to_gui(cls):
        """ send order to GUI so that it can update the states of the menus
        regarding the order """
        data = cls.read_json_file()
        if data == {}:
            return 'next_step'
        else:
            if len(data['players']) == 0:
                return 'next_step'

            elif 0 < len(data['players']) < cf.number_of_players:
                return 'repeat_step'
            elif (len(data['players']) == cf.number_of_players) & (data
            ['rounds'] == []):
                return 'next_step'
            elif 0 < len(data['rounds']) < int(data['round_number']):
                if data['rounds'][-1]['closed'] is True:
                    return 'repeat_step'
                else:
                    return 'next_step'
            elif len(data['rounds']) == data['round_number']:
                return 'end_tournament'

    @classmethod
    def read_json_file(cls):
        """ read json file to get info on state of menus """
        with open(cf.json_file_path, 'r') as f:
            data = json.load(f)
        return data

    @classmethod
    def update_json_file(cls):
        """ create or update the JSON file which is the link between controller
        and GUI """
        global tournament
        with open(cf.json_file_path, 'w') as f:
            if tournament is not None:
                json.dump(tournament.serialize, f)
            else:
                json.dump({}, f)

    @classmethod
    def verify_tournament_creation(cls, info):
        """ verify tournament creation,
         if tournament created, set the menus_states for next step of tournament
         """
        global tournament, states
        if tournament is not None:
            print('tournoi deja cree')
            return {}
        else:
            # create tournament instance from modeles
            tournament = mod.Tournament()
            # set all the attributs regarding the user entries in the GUI
            for key, value in cf.labels_tournament_creation.items():
                setattr(tournament, key, info[value])
            # update the json file with all data of the actual tournament
            cls.update_json_file()
            # create order to the GUI
            order = cls.send_order_to_gui()
            return {'order': order, 'left_window_value': tournament.name}

    @classmethod
    def verify_players_creation(cls, info):
        """ verify players creation when tournament (instance of Tournament
        modele) is already created,
         - create Player model for each new player created by user and set
         its attributs regarding
           the user entries in the GUI.
         - set the menus_states for next step of tournament
         """
        # while number fo players created by user is < than number of players
        # defined in config file
        if len(tournament.players) < cf.number_of_players:
            player = mod.Player()
            tournament.players.append(player)
            for key, value in cf.labels_add_players.items():
                setattr(player, key, info[value])
            setattr(player, 'id', len(tournament.players))
            cls.update_json_file()
            order = cls.send_order_to_gui()
            return {'order': order, 'left_window_value': '{}/{}'.format(len
            (tournament.players), cf.number_of_players)}
        else:
            order = cls.send_order_to_gui()
            return {'order': order, 'left_window_value': '{}/{}'.format(len
            (tournament.players), cf.number_of_players)}

    @classmethod
    def verify_round_creation(cls, info):
        """ verify round creation,
         if round created, set the menus_states for next step of tournament
         """
        global tournament
        if len(tournament.rounds) < cf.number_of_rounds:
            # create round instance from modeles and save it into the tournament variable
            round_instance = mod.Round()
            tournament.rounds.append(round_instance)
            # set all the attributs regarding the user entries in the GUI
            for key, value in cf.labels_round_creation.items():
                setattr(round_instance, key, info[value])
            cls.update_json_file()
            order = cls.send_order_to_gui()
            return {'order': order, 'left_window_value': round_instance.name}

    @classmethod
    def generate_matches(cls):
        matches = tournament.generate_pairs_swiss()
        for match in matches:
            tournament.rounds[-1].matches.append(mod.Match(match[0], match[1]))
        return matches

    @classmethod
    def get_current_matches(cls):
        return tournament.rounds[-1].matches

    @classmethod
    def end_round(cls, data):
        """ execute all the needed tasks when a round is closed """
        for elem in data:
            cls.set_match_scores(elem)
        # generate time_end attribut for Round instance and set self.closed attribut to True
        cls.create_time_end_for_round()
        # update the menus to be able to create new round
        cls.update_json_file()
        order = cls.send_order_to_gui()
        return {'order': order, 'left_window_value': tournament.rounds[-1].name}

    @classmethod
    def set_match_scores(cls, match_dictionary):
        """ use match_dictionary to get the winner of the match and give scores
        to players match_dictionary = {'match_instance': <Match instance>,
        'label': '', 'choice': ['match nul', <player1>, <player2>],
        'result': str(<user choice>)}"""
        p1 = match_dictionary['match_instance'].player1.first_name + ' '
        + match_dictionary['match_instance'].player1.last_name
        p2 = match_dictionary['match_instance'].player2.first_name + ' '
        + match_dictionary['match_instance'].player2.last_name
        if p1 == match_dictionary['result'].get():
            match_dictionary['match_instance'].score_player1 = cf.score_
            winner_match
            match_dictionary['match_instance'].score_player2 = cf.score_loser_
            match
        elif p2 == match_dictionary['result'].get():
            match_dictionary['match_instance'].score_player2 = cf.score_winner_
            match
            match_dictionary['match_instance'].score_player1 = cf.score_loser_
            match
        else:
            match_dictionary['match_instance'].score_player1 = cf.score_even_
            match
            match_dictionary['match_instance'].score_player2 = cf.score_even_
            match
        # write these info in the players attributs for next rounds and final score of tournament
        match_dictionary['match_instance'].player1.tournament_total_
        points += match_dictionary['match_instance'].score_player1
        match_dictionary['match_instance'].player1.opponents.append(
        match_dictionary['match_instance'].player2.id)
        match_dictionary['match_instance'].player2.tournament_total_
        points += match_dictionary['match_instance'].score_player2
        match_dictionary['match_instance'].player2.opponents.append(
        match_dictionary['match_instance'].player1.id)

    @classmethod
    def create_time_end_for_round(cls):
        """ set the time_end attribut of current Round instance to actual time """
        tournament.rounds[-1].time_end = tournament.rounds[-1].generate_time()
        tournament.rounds[-1].closed = True


class DataBase:
    """ use tinyDB bdd regarding client request to save and open data """

    # @classmethod
    # def get_tournament_id(cls, name):
    #     """ get and return the current tournament id in the database table """
    #     t_id = tables['tournament'].get(tournament.name = name)

    @classmethod
    def create_data_base_and_tables(cls):
        """ create a database file and the two corresponding tables as requested
        by the client """
        global tables
        db = TinyDB(cf.data_base_file_name)
        tables = {'tournament': db.table(cf.table_tournament),
                  'players': db.table(cf.table_players)}
        return tables

    @classmethod
    def clear_table(cls, table_name):
        """ clear the table from data """
        table_name.truncate()

    @classmethod
    def insert_players(cls, table_name):
        """ insert data in the table_name """
        for player in tournament.players:
            table_name.insert(player.serialize_player())
        print('fin de insert_players')

    @classmethod
    def insert_tournament(cls, table_name):
        """ insert data in the table_name """
        print('dans insert_tournament:', tournament.serialize)
        table_name.insert(table.Document(tournament.serialize, doc_id=tournament.id))
        print('fin de insert_tournament')

    @classmethod
    def get_all_data_from_database_table(cls, table_name):
        """ get all the data contained in table_name as a list of dictionaries"""
        print('dans get_all_data_from_database_table:\nIdentifier la structure du dico retourne '
              'et entrer cette structure dans le docstring de la fonction')
        return table_name.all()


class SaveOpenTournament:
    """ used to do actions on database with tournament instance """
    tables = DataBase.create_data_base_and_tables()

    @classmethod
    def open_saved_tournament(cls):
        """ open an already saved tournament """
        data = DataBase.get_all_data_from_database_table(cls.tables['tournament'])
        print('open_saved_tournament, data = ', data)

    @classmethod
    def save_current_tournament(cls):
        """ save the current tournament and the players """
        # print('dans save_current_tournament')
        # tables = {'tournament': <table>, 'players': <table>}
        global tables
        # tables = DataBase.create_data_base_and_tables()
        DataBase.insert_tournament(cls.tables['tournament'])
        DataBase.insert_players(cls.tables['players'])


class GenerateReports:
    """" class to generate reports requested by client """
    def generate_report(self):
        """ generate report with the parameters """


def run():
    global tables
    tables = DataBase.create_data_base_and_tables()
    Controls.update_json_file()
    Controls.send_order_to_gui()
    gui.MainWindow().mainloop()


if __name__ == "__main__":
    run()