"""
Project 4 of OpenClassRooms Cursus:
'Développez un programme logiciel en Python'
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
# first_order correspond to data coming from database to launch the program at the right step to continue the tournament
first_order = {}
# tables of database ('tournament' and 'players')
tables = {}
# tournament instance
tournament = mod.Tournament()


class Controls:
    """ control the tournament steps by sending orders to GUI to display the right step at the right time only """

    @classmethod
    def send_order_to_gui(cls) -> str:
        """ send order to GUI so that it can update the states of the menus
        regarding the order and display the right information to continue tournament"""
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
        # create tournament instance from models
        tournament = mod.Tournament()
        if tournament.tournament_started is True:  # tournament already created by user
            return {}
        else:
            # set all the attributs regarding the user entries in the GUI
            for key, value in cf.labels_tournament_creation.items():
                setattr(tournament, key, info[value])
            setattr(tournament, 'tournament_started', True)
            # save the data in the database
            SaveOpenTournament.save_current_tournament()
            # set the order to send to the GUI
            order = cls.send_order_to_gui()
            # return order and info to display in the left window
            return {'order': order, 'left_window_value': tournament.name}

    @classmethod
    def verify_players_creation(cls, info: dict) -> dict:
        """ verify players creation when tournament (instance of Tournament model) is already created,
         - create Player model for each new player created by user and set
         its attributs regarding the user entries in the GUI.
         - set the menus_states for next step of tournament
         """
        # while number of players created by user is < than number of players defined in config file
        if len(tournament.players) < cf.number_of_players:
            player = mod.Player()
            tournament.players.append(player)
            for key, value in cf.labels_add_players.items():
                setattr(player, key, info[value])
            setattr(player, 'id', len(tournament.players))
            # update tournament field in the database
            SaveOpenTournament.update_current_tournament()
            # create a player field in the 'players' table of the database
            SaveOpenTournament.save_player(tournament.players[-1])
            # set the order to the GUI
            order = cls.send_order_to_gui()
            # send order and data to display to the GUI
            return {'order': order, 'left_window_value': '{}/{}'.format(len(tournament.players), cf.number_of_players)}
        else:  # all the players have been created
            # set the order to the GUI
            order = cls.send_order_to_gui()
            # send order and data to display to the GUI
            return {'order': order, 'left_window_value': '{}/{}'.format(len(tournament.players), cf.number_of_players)}

    @classmethod
    def verify_round_creation(cls, info: dict) -> dict:
        """ verify round creation, if round created, set the menus_states for next step of tournament and the data to
        display in the left window """
        global tournament
        # if not all rounds have been created
        if len(tournament.rounds) < tournament.round_number:
            # create round instance from model and save it into the tournament variable
            round_instance = mod.Round()
            tournament.rounds.append(round_instance)
            # set all the attributs regarding the user entries in the GUI
            for key, value in cf.labels_round_creation.items():
                setattr(round_instance, key, info[value])
            # save the updated tournament instance in the database
            SaveOpenTournament.update_current_tournament()
            # set the order to the GUI
            order = cls.send_order_to_gui()
            # send order and data to display to the GUI
            return {'order': order, 'left_window_value': round_instance.name}

    @classmethod
    def generate_matches(cls) -> list:
        """ when a round is created, matches are automatically created between players regarding the swiss-pair
        algorithm and then added to tournament instance and saved into the database"""
        matches = tournament.generate_pairs_swiss()
        for match in matches:
            tournament.rounds[-1].matches.append(mod.Match(match[0], match[1]))
        SaveOpenTournament.update_current_tournament()
        return matches

    @classmethod
    def get_current_matches(cls) -> list:
        """ used in the GUI to display the current matches if the round is not finished """
        return tournament.rounds[-1].matches

    @classmethod
    def save_scores(cls, data: list) -> dict:
        """ close a round when finished and set the time and date of end and the scores for each match """
        # generate scores for each player regarding match results
        for elem in data:
            cls.set_match_scores(elem)
        # generate time_end attribut for Round instance and set self.closed attribut to True
        cls.create_time_end_for_round()
        if len(tournament.rounds) == tournament.round_number:
            tournament.tournament_ended = True
        # update the database with the new data of the tournament instance
        SaveOpenTournament.update_current_tournament()
        return {'order': '', 'left_window_value': tournament.rounds[-1].name, 'matches': tournament.rounds[-1].matches}

    @classmethod
    def end_round(cls) -> dict:
        """ When a round is closed, set up and send order and data to display to the GUI """
        order = cls.send_order_to_gui()
        return {'order': order, 'left_window_value': tournament.rounds[-1].name,
                'matches': tournament.rounds[-1].matches}

    @staticmethod
    def display_round_result() -> dict:
        """ at the end of a round, when it is closed, send data to display to GUI """
        return {'name': tournament.rounds[-1].name, 'matches': tournament.rounds[-1].matches}

    @classmethod
    def set_match_scores(cls, match_dictionary: dict) -> None:
        """ use match_dictionary to get the winner of the match and give scores
        to players match_dictionary = {'match_instance': <Match instance>,
        'label': '', 'choice': ['match nul', <player1>, <player2>],
        'result': str(<user choice>)}"""
        # setup the players names
        p1 = match_dictionary['match_instance'].player1.first_name + ' ' + match_dictionary['match_instance']. \
            player1.last_name
        p2 = match_dictionary['match_instance'].player2.first_name + ' ' + match_dictionary['match_instance']. \
            player2.last_name
        # comparaison to the winner of the match
        if p1 == match_dictionary['result'].get():
            match_dictionary['match_instance'].score_player1 = cf.score_winner_match
            match_dictionary['match_instance'].score_player2 = cf.score_loser_match
        elif p2 == match_dictionary['result'].get():
            match_dictionary['match_instance'].score_player2 = cf.score_winner_match
            match_dictionary['match_instance'].score_player1 = cf.score_loser_match
        else:
            match_dictionary['match_instance'].score_player1 = cf.score_even_match
            match_dictionary['match_instance'].score_player2 = cf.score_even_match
        # write these info in the players attributes for next rounds and final score of tournament
        match_dictionary['match_instance'].player1.tournament_total_points += match_dictionary['match_instance']. \
            score_player1
        match_dictionary['match_instance'].player1.opponents.append(match_dictionary['match_instance'].player2.id)
        match_dictionary['match_instance'].player2.tournament_total_points += match_dictionary['match_instance']. \
            score_player2
        match_dictionary['match_instance'].player2.opponents.append(match_dictionary['match_instance'].player1.id)

    @classmethod
    def create_time_end_for_round(cls) -> None:
        """ method used when a round is closed"""
        tournament.rounds[-1].time_end = tournament.rounds[-1].generate_time()
        tournament.rounds[-1].closed = True


class DataBase:
    """ use tinyDB bdd regarding client request to save and open data """

    @staticmethod
    def create_data_base() -> None:
        """ create the database and its tables if not created. It uses config file """
        global tables
        db = TinyDB(cf.data_base_file_name)
        tables = {'tournament': db.table(cf.table_tournament), 'players': db.table(cf.table_players)}

    @classmethod
    def insert_player(cls, player: object) -> None:
        """ method used when a player is added to the tournament instance to add it also into the database """
        tables['players'].insert(player.serialize_player())

    @staticmethod
    def insert_tournament() -> None:
        """ insert tournament instance serialized in the table 'tournament' of te database"""
        tables['tournament'].insert(tournament.serialize)

    @classmethod
    def get_last_data_from_database_table(cls, table_name: object) -> dict:
        """ used to open the last tournament in the database and check if it is needed to finish it"""
        try:
            return table_name.all()[-1]
        except IndexError:
            return {}

    @classmethod
    def update_last_data_in_database_table(cls, table_name: object, data_updated: dict) -> None:
        """ update the last data in the database table_name with updated data in parameter """
        data = Query()
        last_entry = cls.get_last_data_from_database_table(table_name)
        table_name.update(data_updated, data.name == last_entry['name'])


class SaveOpenTournament:
    """ Automatically save and open tournament instance to and from database """

    @classmethod
    def open_saved_tournament(cls) -> dict:
        """ used only at first start of the program to check at what step the last tournament instance saved into
         the database is. This method is used the method which_tournament_step
         """
        global tournament
        data = DataBase.get_last_data_from_database_table(tables['tournament'])
        tournament = mod.Tournament()
        if data != {}:  # if the database is empty
            tournament.from_serialized_to_instance(data)
        else:
            pass
        return cls.which_tournament_step()

    @staticmethod
    def which_tournament_step() -> dict:
        """ method used only for the first launch of the program to know if it must continue a tournament already
        existing and save in the database but not finished or if it must start a new one, send dict to the GUI"""
        if tournament.tournament_ended is False:
            menus_states = {'tournament_start': 'disabled', 'add_players': 'disabled', 'launch_round': 'disabled'}
            left_window_values = {'Tournoi': tournament.name,
                                  'Joueurs': '{}/{}'.format(len(tournament.players), cf.number_of_players),
                                  'Tour en cours': 'aucun'}
            if tournament.tournament_started is False:  # if the tournament instance has not been activated by user,
                # start the GUI for a new tournament
                menus_states['tournament_start'] = 'normal'
                return {'states': menus_states, 'left_window_values': left_window_values}

            elif len(tournament.players) < cf.number_of_players:  # if all the players have not been created
                menus_states['add_players'] = 'normal'
                return {'states': menus_states, 'left_window_values': left_window_values}
            elif not tournament.rounds:  # if all players have been created but no round exists
                left_window_values['Tour en cours'] = 'aucun'
                menus_states['launch_round'] = 'normal'
                return {'states': menus_states, 'left_window_values': left_window_values}
            elif len(tournament.rounds) < tournament.round_number:  # if not all the rounds have been created
                if tournament.rounds[-1].closed is False:  # if the last round is not finished
                    left_window_values['Tour en cours'] = tournament.rounds[-1].name
                    menus_states['launch_round'] = 'disabled'
                    matches = [(match.player1, match.player2) for match in tournament.rounds[-1].matches]
                    return {'states': menus_states, 'left_window_values': left_window_values, 'data': matches}
                else:  # if the last round is finished
                    left_window_values['Tour en cours'] = 'aucun'
                    menus_states['launch_round'] = 'disabled'
                    return {'states': menus_states, 'left_window_values': left_window_values, 'display': {}}
            elif len(tournament.rounds) == tournament.round_number and tournament.rounds[-1].closed is False:
                # if all the rounds have been created but the last one is not yet finished
                left_window_values['Tour en cours'] = tournament.rounds[-1].name
                menus_states['launch_round'] = 'normal'
                matches = [(match.player1, match.player2) for match in tournament.rounds[-1].matches]
                return {'states': menus_states, 'left_window_values': left_window_values, 'data': matches}
        else:  # if the tournament is finished
            menus_states = {'tournament_start': 'normal', 'add_players': 'disabled', 'launch_round': 'disabled'}
            left_window_values = {'Tournoi': 'aucun', 'Joueurs': '0/8', 'Tour en cours': 'aucun'}
            return {'states': menus_states, 'order': 'repeat_step', 'left_window_values': left_window_values}

    @staticmethod
    def save_current_tournament() -> None:
        """ save the current tournament for the first time in the database """
        DataBase.insert_tournament()

    @staticmethod
    def save_player(player) -> None:
        """ used each time a new player is created by user """
        DataBase.insert_player(player)

    @staticmethod
    def update_current_tournament():
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
    # 2 - read the database to search for the last tournament and check if it's finished or not, return an order for
    # the GUI
    first_order = SaveOpenTournament.open_saved_tournament()
    # 3 - launch the GUI
    gui.MainWindow().mainloop()


if __name__ == "__main__":
    run()
