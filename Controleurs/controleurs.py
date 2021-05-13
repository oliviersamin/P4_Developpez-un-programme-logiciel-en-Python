"""
Project 4 of OpenClassRooms Cursus:
'Developpez un programme logiciel en Python'
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

from tinydb import TinyDB, Query

import Vues.gui as gui
import Modeles.modeles as mod
import config as cf

# initialize variables
# states that will be the core of GUI - controller communication for tournament steps control
states = None
# first_order coreespond to data coming from database to launch the program at the right step to continue the tournament
first_order = {}
# tables of database ('tournament' and 'players')
tables = {}
# tournament instance
tournament = mod.Tournament()


class Controls:
    """ control the tournament steps regarding the user inputs """

    @classmethod
    def send_order_to_gui2(cls) -> str:
        """ send order to GUI so that it can update the states of the menus
        regarding the order """
        # print('dans send_order_to_gui: ', data, len(data['rounds']))
        if tournament.tournament_started is False:
            return 'next_step'
        else:
            if len(tournament.players) == 0:
                return 'next_step'

            elif 0 < len(tournament.players) < cf.number_of_players:
                return 'repeat_step'
            elif (len(tournament.players) == cf.number_of_players) & (tournament.rounds == []):
                return 'next_step'
            elif 0 < len(tournament.rounds) < int(tournament.round_number):
                if tournament.rounds[-1].closed is True:
                    return 'repeat_step'
                else:
                    return 'next_step'
            elif len(tournament.rounds) == tournament.round_number:
                return 'end_tournament'

    @classmethod
    def verify_tournament_creation(cls, info: dict) -> dict:
        """ verify tournament creation,
         if tournament created, set the menus_states for next step of tournament
         """
        global tournament, states
        tournament = mod.Tournament()
        if tournament.tournament_started is True:
            print('tournoi deja cree')
            return {}
        else:
            # create tournament instance from modeles
            # tournament = mod.Tournament()
            # set all the attributs regarding the user entries in the GUI
            for key, value in cf.labels_tournament_creation.items():
                setattr(tournament, key, info[value])
            setattr(tournament, 'tournament_started', True)
            # update the json file with all data of the actual tournament
            # cls.update_json_file()
            SaveOpenTournament.save_current_tournament()
            # create order to the GUI
            order = cls.send_order_to_gui2()
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
        # while number fo players created by user is < than number of players defined in config file
        if len(tournament.players) < cf.number_of_players:
            player = mod.Player()
            tournament.players.append(player)
            for key, value in cf.labels_add_players.items():
                setattr(player, key, info[value])
            setattr(player, 'id', len(tournament.players))
            # cls.update_json_file()
            SaveOpenTournament.update_current_tournament()
            SaveOpenTournament.save_player(tournament.players[-1])
            order = cls.send_order_to_gui2()
            return {'order': order, 'left_window_value': '{}/{}'.format(len(tournament.players), cf.number_of_players)}
        else:
            order = cls.send_order_to_gui2()
            return {'order': order, 'left_window_value': '{}/{}'.format(len(tournament.players), cf.number_of_players)}

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
            # cls.update_json_file()
            SaveOpenTournament.update_current_tournament()
            order = cls.send_order_to_gui2()
            return {'order': order, 'left_window_value': round_instance.name}

    @classmethod
    def save_round_matches(cls):
        """ save the matches of the current round """
        SaveOpenTournament.update_current_tournament()

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
    def save_scores(cls, data: list) -> dict:
        """ execute all the needed tasks when a round is closed """
        for elem in data:
            cls.set_match_scores(elem)
        # generate time_end attribut for Round instance and set self.closed attribut to True
        cls.create_time_end_for_round()
        # update the menus to be able to create new round
        # cls.update_json_file()
        if len(tournament.rounds) == tournament.round_number:
            tournament.tournament_ended = True
        SaveOpenTournament.update_current_tournament()
        # order = cls.send_order_to_gui()
        return {'order': '', 'left_window_value': tournament.rounds[-1].name, 'matches': tournament.rounds[-1].matches}

    @classmethod
    def end_round(cls) -> dict:
        """ execute all the needed tasks when a round is closed """
        order = cls.send_order_to_gui2()
        return {'order': order, 'left_window_value': tournament.rounds[-1].name,
                'matches': tournament.rounds[-1].matches}

    @staticmethod
    def display_round_result() -> dict:
        return {'name': tournament.rounds[-1].name, 'matches': tournament.rounds[-1].matches}

    @classmethod
    def set_match_scores(cls, match_dictionary: dict) -> None:
        """ use match_dictionary to get the winner of the match and give scores
        to players match_dictionary = {'match_instance': <Match instance>,
        'label': '', 'choice': ['match nul', <player1>, <player2>],
        'result': str(<user choice>)}"""
        p1 = match_dictionary['match_instance'].player1.first_name + ' ' + match_dictionary['match_instance']. \
            player1.last_name
        p2 = match_dictionary['match_instance'].player2.first_name + ' ' + match_dictionary['match_instance']. \
            player2.last_name
        if p1 == match_dictionary['result'].get():
            match_dictionary['match_instance'].score_player1 = cf.score_winner_match
            match_dictionary['match_instance'].score_player2 = cf.score_loser_match
        elif p2 == match_dictionary['result'].get():
            match_dictionary['match_instance'].score_player2 = cf.score_winner_match
            match_dictionary['match_instance'].score_player1 = cf.score_loser_match
        else:
            match_dictionary['match_instance'].score_player1 = cf.score_even_match
            match_dictionary['match_instance'].score_player2 = cf.score_even_match
        # write these info in the players attributs for next rounds and final score of tournament
        match_dictionary['match_instance'].player1.tournament_total_points += match_dictionary['match_instance']. \
            score_player1
        match_dictionary['match_instance'].player1.opponents.append(match_dictionary['match_instance'].player2.id)
        match_dictionary['match_instance'].player2.tournament_total_points += match_dictionary['match_instance']. \
            score_player2
        match_dictionary['match_instance'].player2.opponents.append(match_dictionary['match_instance'].player1.id)

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

    # @classmethod
    # def create_data_base_and_tables(cls):
    #     """ create a database file and the two corresponding tables as requested
    #     by the client """
    #     global tables
    #     db = TinyDB(cf.data_base_file_name)
    #     tables = {'tournament': db.table(cf.table_tournament),
    #               'players': db.table(cf.table_players)}
    #     return tables

    @staticmethod
    def create_data_base():
        global tables
        db = TinyDB(cf.data_base_file_name)
        tables = {'tournament': db.table(cf.table_tournament), 'players': db.table(cf.table_players)}

    @classmethod
    def clear_table(cls, table_name):
        """ clear the table from data """
        table_name.truncate()

    @classmethod
    def insert_player(cls, player):
        """ insert data in the table_name """
        tables['players'].insert(player.serialize_player())

    @classmethod
    def insert_tournament(cls, table_name):
        """ insert data in the table_name """
        table_name.insert(tournament.serialize)

    @classmethod
    def get_last_data_from_database_table(cls, table_name) -> dict:
        """ get all the data contained in table_name as a list of dictionaries"""
        try:
            return table_name.all()[-1]
        except IndexError:
            return {}

    @classmethod
    def update_last_data_in_database_table(cls, table_name, data_updated):
        """ update the last data in the database table_name with updated data in parameter """
        data = Query()
        last_entry = cls.get_last_data_from_database_table(table_name)
        table_name.update(data_updated, data.name == last_entry['name'])


class SaveOpenTournament:
    """ used to do actions on database with tournament instance """

    # tables = DataBase.create_data_base_and_tables()

    @classmethod
    def open_saved_tournament(cls) -> dict:
        """ open an already saved tournament """
        global tournament
        data = DataBase.get_last_data_from_database_table(tables['tournament'])
        tournament = mod.Tournament()
        if data != {}:
            tournament.from_serialized_to_instance(data)
        else:
            pass
        return cls.which_tournament_step()

    @classmethod
    def which_tournament_step(cls) -> dict:
        """ always get all states menus of the GUI to 'disabled' before launching this method,
         and get left window value and menu = 'normal'"""
        if tournament.tournament_ended is False:
            menus_states = {'tournament_start': 'disabled', 'add_players': 'disabled', 'launch_round': 'disabled'}
            left_window_values = {'Tournoi': tournament.name,
                                  'Joueurs': '{}/{}'.format(len(tournament.players), cf.number_of_players),
                                  'Tour en cours': 'aucun'}
            if tournament.tournament_started is False:
                menus_states['tournament_start'] = 'normal'
                return {'states': menus_states, 'left_window_values': left_window_values}

            elif len(tournament.players) < cf.number_of_players:
                # print(tournament.__dict__)
                # print('players à entrer: ', left_window_values)
                menus_states['add_players'] = 'normal'
                return {'states': menus_states, 'left_window_values': left_window_values}
            elif not tournament.rounds:
                left_window_values['Tour en cours'] = 'aucun'
                menus_states['launch_round'] = 'normal'
                return {'states': menus_states, 'left_window_values': left_window_values}
            elif len(tournament.rounds) < tournament.round_number:
                print('dans len(tournament.rounds) < tournament.round_number:')
                if tournament.rounds[-1].closed is False:
                    left_window_values['Tour en cours'] = tournament.rounds[-1].name
                    menus_states['launch_round'] = 'disabled'
                    matches = [(match.player1, match.player2) for match in tournament.rounds[-1].matches]
                    return {'states': menus_states, 'left_window_values': left_window_values, 'data': matches}
                else:
                    left_window_values['Tour en cours'] = 'aucun'
                    menus_states['launch_round'] = 'disabled'
                    return {'states': menus_states, 'left_window_values': left_window_values, 'display': {}}
            elif len(tournament.rounds) == tournament.round_number and tournament.rounds[-1].closed is False:
                left_window_values['Tour en cours'] = tournament.rounds[-1].name
                menus_states['launch_round'] = 'normal'
                matches = [(match.player1, match.player2) for match in tournament.rounds[-1].matches]
                return {'states': menus_states, 'left_window_values': left_window_values, 'data': matches}
        else:
            menus_states = {'tournament_start': 'normal', 'add_players': 'disabled', 'launch_round': 'disabled'}
            left_window_values = {'Tournoi': 'aucun', 'Joueurs': '0/8', 'Tour en cours': 'aucun'}
            return {'states': menus_states, 'order': 'repeat_step', 'left_window_values': left_window_values}

    @staticmethod
    def save_current_tournament():
        """ save the current tournament and the players for the first time in the database """
        # global tables
        DataBase.insert_tournament(tables['tournament'])
        # DataBase.insert_players(tables['players'])

    @staticmethod
    def save_player(player):
        DataBase.insert_player(player)

    @classmethod
    def update_current_tournament(cls):
        """ update the last tournament inside the database """
        DataBase.update_last_data_in_database_table(tables['tournament'], tournament.serialize)


class GenerateReports:
    """" class to generate reports requested by client """

    def generate_report(self):
        """ generate report with the parameters """


def run():
    """ main function to be launch to run the program """
    global first_order
    # 1- create the database and tables if does not exists
    DataBase.create_data_base()
    # 2 - read teh database to search for the last tournament and check if it's finished or not
    first_order = SaveOpenTournament.open_saved_tournament()
    # Controls.update_json_file()
    # # 3 - send the first order to gui to display or the unfinished tournament in the database or a new one
    # (if finished)
    # Controls.send_order_to_gui()
    # 4 - launch the GUI
    gui.MainWindow().mainloop()


if __name__ == "__main__":
    run()
