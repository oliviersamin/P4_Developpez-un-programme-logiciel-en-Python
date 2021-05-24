""" module that generates the GUI """

import os
import tkinter as tk
import tkinter.messagebox as msg

import config as cf
import Controleurs.controleurs as ct


class MainWindow(tk.Tk):
    """ main window of the GUI """
    def __init__(self):
        tk.Tk.__init__(self)
        # size of the several windows displayed during the program
        self.size_main = cf.SIZE_MAIN
        self.size_tournament = cf.SIZE_TOURNAMENT
        self.size_add_player = cf.SIZE_ADD_PLAYER
        self.size_left_window = cf.SIZE_LEFT_WINDOW
        self.size_round_in_progress = cf.SIZE_ROUND_IN_PROGRESS
        self.size_closing_round = cf.SIZE_CLOSING_ROUND
        # title of the main window
        self.title(cf.TITLE_MAIN_WINDOW)
        # apply the size of the main window at start
        self.geometry(self.size_main)
        # initializing needed variables
        self.left_window = None
        self.last_window_created = None
        self.frame_left = None
        self.frame_right = None
        self.menubar = None
        self.window = None
        self.list_instances_menus_tournament = Menu.initialize_menus_instances_tournament()
        self.list_instances_menus_reports = Menu.initialize_menus_instances_reports()
        self.first_update_menus_tournament(ct.FIRST_ORDER)
        # displays the main window and its widgets
        self.launch()

    def first_update_menus_tournament(self, order: dict) -> None:
        """ used at first start only to display the right data regarding the tournament steps to display"""
        # setup the menus available to user and left window data to display
        for menu, state, value in zip(self.list_instances_menus_tournament, order['states'].values(),
                                      order['left_window_values'].values()):
            menu.state = state
            menu.left_window_value = value
        try:  # if the tournament step correspond to launch a new round
            self.create_right_left_containers()
            self.window = LaunchRound(master=self.frame_right, relaunch=order['data'], borderwidth=0, relief=tk.GROOVE)
            self.window.grid(row=1, column=0, padx=10, pady=20)

        except KeyError:
            try:  # if the tournament step correspond to close an existing round
                self.create_right_left_containers()
                self.window = CloseRound(master=self.frame_right, relaunch=order['display'], borderwidth=0,
                                         relief=tk.GROOVE)
                self.window.grid(row=1, column=0, padx=10, pady=20)

            except KeyError:
                pass

    def create_right_left_containers(self) -> None:
        """ create the containers where the left and right windows are displayed """
        self.frame_left = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_left.grid(row=0, column=0)
        # self.window_left_info = None
        self.frame_right = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_right.grid(row=0, column=1)

    def launch(self) -> None:
        """ displays the GUI main window and its widgets"""
        # create the containers that contain the windows
        self.create_right_left_containers()
        # 1 - displays the left window
        self.left_window = LeftWindow(self.frame_left)
        # 2 - displays the menu bar
        self.menubar = tk.Menu(self)
        menus_to_display = Menu.setup_main_menus_architecture(self.list_instances_menus_tournament,
                                                              self.list_instances_menus_reports)
        for elem in menus_to_display:
            menu = tk.Menu(self.menubar, tearoff=0)
            for el in elem['unfold']:
                menu.add_command(label=el['label'], state=el['state'],
                                 command=eval(el['function'], {'RightWindow': RightWindow, 'self': self, 'ct': ct,
                                                               'ChooseTournamentForReport':
                                                                   ChooseTournamentForReport}))
            self.menubar.add_cascade(label=elem['name'], menu=menu)
        self.config(menu=self.menubar)

    @staticmethod
    def test():  # TO BE DELETED WHEN PROGRAM COMPLETED
        """ while construction is in progress. MUST BE ERASED AT THE END"""
        print('methode test')


class Menu:
    """ Generate each menu to be displayed in the GUI and manage all the operations to
     perform on them"""
    def __init__(self, name, label, class_to_use, size, state, left_window_label=None, left_window_value=None):
        """ initialize a Menu instance with parameters """
        self.name = name
        self.label = label
        self.class_to_use = class_to_use
        self.size = size
        self.state = state
        self.left_window_label = left_window_label
        self.left_window_value = left_window_value

    @staticmethod
    def initialize_menus_instances_tournament() -> list:
        """ initialize the menus link with tournament steps for the GUI, it is used by MainWindow to create menus"""
        tournament_start = Menu(name='tournament_start', label="Créer le tournoi", class_to_use=CreateNewTournament,
                                size=cf.SIZE_TOURNAMENT,
                                state='disabled', left_window_label='Tournoi', left_window_value='non cree')
        add_players = Menu(name='add_players', label="Ajouter les joueurs", class_to_use=AddPlayers,
                           size=cf.SIZE_ADD_PLAYER,
                           state='disabled', left_window_label='Joueurs',
                           left_window_value='0/{}'.format(cf.NUMBER_OF_ROUNDS))
        launch_round = Menu(name='launch_round', label="Lancer le tour", class_to_use=LaunchRound,
                            size=cf.SIZE_ROUND_IN_PROGRESS,
                            state='disabled', left_window_label='Tour en cours', left_window_value='aucun')
        return [tournament_start, add_players, launch_round]

    @staticmethod
    def initialize_menus_instances_reports() -> list:
        """ initialize the menus linked with reports generation for the GUI, it is used by MainWindow
        to create menus"""
        list_all_actors = Menu(name='list_all_actors', label="liste de tous les acteurs",
                               class_to_use=ChooseTournamentForReport,
                               size=cf.SIZE_TOURNAMENT,
                               state='normal')
        list_all_players_of_tournament = Menu(name='list_all_players_of_tournament',
                                              label="liste des joueurs d'un tournoi",
                                              class_to_use=ChooseTournamentForReport,
                                              size=cf.SIZE_ADD_PLAYER, state='normal')
        list_all_tournaments = Menu(name='list_all_tournaments', label="liste de tous les tournois",
                                    class_to_use=ChooseTournamentForReport, size=cf.SIZE_ROUND_IN_PROGRESS,
                                    state='normal')
        list_all_rounds_of_tournament = Menu(name='list_all_rounds_of_tournament',
                                             label="liste de tous les tours d'un tournoi",
                                             class_to_use=ChooseTournamentForReport, size=cf.SIZE_CLOSING_ROUND,
                                             state='normal')
        list_all_matches_of_tournament = Menu(name='list_all_matches_of_tournament',
                                              label="liste de tous les matchs d'un tournoi",
                                              class_to_use=ChooseTournamentForReport, size=cf.SIZE_CLOSING_ROUND,
                                              state='normal')
        return [list_all_actors, list_all_tournaments, list_all_players_of_tournament,
                list_all_rounds_of_tournament, list_all_matches_of_tournament]

    @staticmethod
    def setup_main_menus_architecture(instances_tournament, instances_report) -> list:
        """ setup the main menus architecture to display by the main window"""
        return [{'name': "tournoi actuel",
                 'unfold': [{'label': elem.label, 'state': elem.state,
                             'function': "lambda i= ['" + elem.name + "', self.frame_right, "
                                                                      "self.list_instances_menus_tournament]: "
                                                                      "RightWindow.display_right_window(i)"}
                            for elem in instances_tournament]},
                {'name': "générer les rapports",
                 'unfold': [{'label': elem.label, 'state': elem.state,
                             'function': "lambda i= '" +
                                         elem.name + "': ChooseTournamentForReport(self.frame_right, i)"}
                            for elem in instances_report]}]

    @staticmethod
    def update_menus_tournament(order: dict, master: object) -> list:
        """used each time the GUI receive an order from controller. Is allows the user to see go through all steps of
        the tournament
        """
        list_menus = master.master.list_instances_menus_tournament
        for index, elem in enumerate(list_menus):
            if (elem.name == 'tournament_start') & (elem.state == 'normal'):  # step of tournament creation
                if order['order'] == 'next_step':
                    elem.state = 'disabled'
                    elem.left_window_value = order['left_window_value']
                    list_menus[index + 1].state = 'normal'
                    return list_menus
            elif (elem.name == 'add_players') & (elem.state == 'normal'):  # step of adding players to the tournament
                if order['order'] == 'repeat_step':
                    elem.left_window_value = order['left_window_value']
                    return list_menus
                elif order['order'] == 'next_step':
                    elem.left_window_value = order['left_window_value']
                    elem.state = 'disabled'
                    list_menus[index + 1].state = 'normal'
                    return list_menus
            elif (elem.name == 'launch_round') & (elem.state == 'normal'):  # step of launching new round of tournament
                elem.left_window_value = order['left_window_value']
                elem.state = 'disabled'
                return list_menus
            elif (elem.name == 'launch_round') & (elem.state == 'disabled'):
                if order['order'] == 'repeat_step':
                    elem.state = 'normal'
                    return list_menus
                elif order['order'] == 'end_tournament':
                    # print("order['order'] == 'end_tournament'")
                    # list_menus[0].state = 'normal'
                    return list_menus
                else:
                    return list_menus


class GenericWindow(tk.Frame):
    """ This class define generic commands for windows to be displayed inside the GUI"""

    def __init__(self, master, **kwargs):
        """ initialize attributes """
        tk.Frame.__init__(self, master, **kwargs)
        self.data = []  # data with following structure {'name': <NAME>, 'tk_object': <tkObject>}
        self.attributs = {}
        self.widgets = []
        self.menus_states = ct.STATES

    def destroy_widgets(self) -> None:
        """ destroy all the widgets of the window """
        for elem in self.widgets:
            try:
                for el in elem:
                    el.destroy()
            except TypeError:
                elem.destroy()

    def my_line(self, master, name, prefilled_entry, r, c, rsp, csp, px, py) -> None:
        """ this method generates a line with a label in a column and an Entry in the column next to it
         It also saves the Entry in the self.data variable
         """
        line = tk.Label(master=master, text=name, anchor='w')
        line.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        text = tk.StringVar()
        text.set(prefilled_entry)
        l2 = tk.Entry(master=master, textvariable=text)
        l2.grid(row=r, column=c + 1, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        self.data.append({'name': name, 'tk_object': l2})

    def my_line2(self, master, name, r, c, rsp, csp, px, py) -> object:
        """ this method generates a line with a label in a column and an Entry in the column next to it
         It also saves the Entry in the self.data variable
         """
        line = tk.Label(master=master, text=name, anchor='w')
        line.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        l2 = tk.Entry(master=master)
        l2.grid(row=r, column=c + 1, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        self.data.append({'name': name, 'tk_object': l2})
        return line, l2

    @staticmethod
    def my_simple_line(master, name, r, c, rsp, csp, px, py) -> object:
        """ this method generates a line with a label   """
        line = tk.Label(master=master, text=name, anchor='w')
        line.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        return line

    @staticmethod
    def my_data(master, name1, name2, r, c, rsp, csp, px, py) -> None:
        """ this method generates two lines with one label each """
        line1 = tk.Label(master=master, text=name1, anchor='w', font="Helvetica 12 bold")
        line1.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        line2 = tk.Label(master=master, text=name2, anchor='w')
        line2.grid(row=r + 1, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)

    @staticmethod
    def my_button(master, name, c, r, action) -> object:
        """ this method generates a button with a text and an action to perform when clicked"""
        b = tk.Button(master=master, text=name, command=action)
        b.grid(row=r, column=c, rowspan=1, columnspan=1, padx=10, pady=10)
        return b

    @staticmethod
    def my_option_menu(master, choice_list, r, c, rsp, csp, px, py) -> object:
        """ used to display the choice of winner at the end of a round """
        variable = tk.StringVar(master)
        menu = tk.OptionMenu(master, variable, *choice_list)
        menu.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        return variable, menu

    def destroy_window(self) -> None:
        """ destroy the master of the actual window and reset the containers. Used to pass from one right window
         to another one when a button is clicked"""
        self.master.destroy()
        self.master.master.create_right_left_containers()


class RightWindow:
    """ displays a window inside a pre created right container.
     You must define the master, the class to use and the row and column to setup your
     window"""

    def __init__(self, size, class_to_use, master, row, column, report=None):
        """ initialize all the needed variables with parameters """
        try:
            master.master.geometry(size)
        except AttributeError:
            pass
        self.window = class_to_use(master=master, borderwidth=0, relief=tk.GROOVE)
        self.window.grid(row=row, column=column, padx=10, pady=20)

    @classmethod
    def display_right_window(cls, list_instances: list) -> None:
        """ display the window in the right container
        entry : list with following data [name, master, list_instances_menus_tournament]"""
        for elem in list_instances[2]:
            if elem.name == list_instances[0]:
                # try:
                cls(size=elem.size, class_to_use=elem.class_to_use, master=list_instances[1], row=1, column=0,
                    report=elem.name)
                #     print('dans try')
                # except IndexError:
                #     cls(size=elem.size, class_to_use=elem.class_to_use, master=list_instances[1], row=1, column=0)


class LeftWindow(GenericWindow):
    """ display the information of the tournament to allow the user to see its evolution """

    def __init__(self, master, **kwargs):
        """ initialize the variables needed and display the left window """
        GenericWindow.__init__(self, master, **kwargs)
        # self.get_data()
        self.master = master
        self.values = {}
        for elem in self.master.master.list_instances_menus_tournament:
            self.values.update({elem.left_window_label: elem.left_window_value})
        self.__display()

    def update_and_display(self, updated_data: list) -> None:
        """ used  to update the data to display and then display it"""
        for elem in updated_data:
            self.values.update({elem.left_window_label: elem.left_window_value})
        self.__display()

    def __display(self) -> None:
        """ display the window and the information of tournament steps"""
        ligne = 0
        for key, value in self.values.items():
            self.my_data(self.master, key, value, ligne, 0, 1, 1, 2, 2)
            ligne += 2


class CreateNewTournament(GenericWindow):
    """ create a new tournament right window to allow the user to entre the data"""
    def __init__(self, master, **kwargs):
        """ initialize variable and display the window to create tournament """
        GenericWindow.__init__(self, master, **kwargs)
        self.states = None
        self.master = master
        self.display()

    def display(self) -> None:
        """ displays  the window """
        labels = [value for value in cf.LABELS_TOURNAMENT_CREATION.values()]
        entries = [value for value in cf.ENTRIES_TOURNAMENT_CREATION.values()]
        for index, elem in enumerate(labels):
            self.my_line(self.master, elem, entries[index], index, 0, 1, 1, 10, 10)
        self.my_button(self.master, 'créer le tournoi', 0, len(labels) + 1, self.create_new_tournament)

    def create_new_tournament(self) -> None:
        """ 1 - gather all the user inputs and update the corresponding variable
            2 - send info and request to controller and execute the order received
            3 - relaunch main window to apply the update and destroy actual right window
            """
        # 1
        for elem in self.data:
            key = ''
            value = ''
            for k, v in elem.items():
                if k == 'name':
                    key = v
                else:
                    if key == 'Nombre de tours':
                        if v.get() != '':
                            value = v.get()
                        else:
                            value = cf.NUMBER_OF_ROUNDS
                    else:
                        value = v.get()
            self.attributs.update({key: value})
        # 2
        # order id a dictionary {'order': order, 'left_window_value': <value to display>}
        order = ct.Controls.verify_tournament_creation(self.attributs)
        # update the menus and the left window
        self.master.master.list_instances_menus_tournament = Menu.update_menus_tournament(order, self.master)
        self.master.master.left_window.update_and_display(self.master.master.list_instances_menus_tournament)
        # 3
        self.master.master.launch()
        self.destroy_window()


class AddPlayers(GenericWindow):
    """ create a right window to add a new player to the tournament """

    def __init__(self, master, **kwargs):
        """ initialize variables and display the window"""
        GenericWindow.__init__(self, master, **kwargs)
        self.master = master
        self.all_players_created = False
        self.display()

    def reset_variables(self) -> None:
        """ reset variables between players to add"""
        self.attributs = {}
        self.data = []

    def display(self) -> None:
        """ displays  the window """
        self.reset_variables()
        labels = [value for value in cf.LABELS_ADD_PLAYERS.values()]
        for index, elem in enumerate(labels):
            self.my_line(self.master, elem, '', index, 0, 1, 1, 10, 10)
        self.my_button(self.master, 'ajouter le joueur', 1, len(labels) + 1, self.add_new_player)

    def add_new_player(self) -> None:
        """ 1 - gather the user inputs into self.attributs
            2 - send info to controller, get the order from controller, update left window
            3 - reset / close the window  regarding the order received"""

        # 1
        for elem in self.data:
            key = ''
            value = ''
            for k, v in elem.items():
                if k == 'name':
                    key = v
                else:
                    value = v.get()
            self.attributs.update({key: value})

        # 2
        order = ct.Controls.verify_players_creation(self.attributs)
        self.master.master.list_instances_menus_tournament = Menu.update_menus_tournament(order, self.master)
        self.master.master.left_window.update_and_display(self.master.master.list_instances_menus_tournament)
        # 3
        if order['order'] == 'repeat_step':
            self.display()
        else:
            self.destroy_window()
            self.master.master.launch()


class LaunchRound(GenericWindow):
    """ create a right window to  launch a new round"""
    def __init__(self, master, relaunch=None, **kwargs):
        """ initialize variables """
        GenericWindow.__init__(self, master, **kwargs)
        self.round_number = None
        self.master = master  # not None if launched at first time from database
        self.relaunch = relaunch
        if self.relaunch is not None:
            self.display_round_information(self.relaunch)
        else:
            self.display_round_creation()

    def display_round_creation(self) -> None:
        """ displays  the window to create the round"""
        labels = [value for value in cf.LABELS_ROUND_CREATION.values()]
        for index, elem in enumerate(labels):
            self.widgets.append(self.my_line2(self.master, elem, index, 0, 1, 1, 10, 10))
        self.widgets.append(self.my_button(self.master, 'créer le tour', 1, len(labels), self.create_new_round))

    def create_new_round(self) -> None:
        """ create and launch the round
        1 - gather all the information entered by user and save them into variable
        2 - send info to controller and receive order in return, update the menus and left window data to display
        3 - display all the matches to be played in the round"""

        # 1
        for elem in self.data:
            key = ''
            value = ''
            for k, v in elem.items():
                if k == 'name':
                    key = v
                else:
                    value = v.get()
            self.attributs.update({key: value})

        # 2
        order = ct.Controls.verify_round_creation(self.attributs)
        self.master.master.list_instances_menus_tournament = Menu.update_menus_tournament(order, self.master)
        self.master.master.left_window.update_and_display(
            self.master.master.list_instances_menus_tournament)
        self.master.master.launch()
        self.destroy_widgets()

        # # 3
        matches = ct.Controls.generate_matches()
        self.display_round_information(matches)

    def display_round_information(self, matches) -> None:
        """ display the matches to be played during this round """
        line = 1
        # displaying title
        title = cf.TITLE_WINDOW_DISPLAY_MATCHES_OF_ROUND
        self.my_simple_line(self.master, title, line, 1, 1, 1, 10, 10)
        line += 1
        # displaying one match by line
        for match in matches:
            label = 'match {} : '.format(matches.index(match) + 1) + match[0].first_name + ' ' + match[0].last_name + \
                    ' vs ' + match[1].first_name + ' ' + match[1].last_name
            self.my_simple_line(self.master, label, line, 0, 1, 3, 10, 10)
            line += 1
        # displaying a button to go through next step
        self.my_button(self.master, 'Entrer les scores', 1, line, self.close_round)

    def close_round(self) -> None:
        """ close the current round launching the CloseRound instance """
        self.destroy_window()
        self.master.master.launch()
        menu = Menu(name='close_round', label='Clôturer le tour', class_to_use=CloseRound,
                    size=cf.SIZE_CLOSING_ROUND, state='disabled',
                    left_window_label='Tour termine', left_window_value='aucun')
        RightWindow.display_right_window(['close_round', self.master.master.frame_right, [menu]])


class CloseRound(GenericWindow):
    """ display a right window that allows user to enter the scores for each match and therefore close the round
    and go through next step of tournament """
    def __init__(self, master, relaunch=None, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        # self.lignes = [{'match_instance': <Match instance>, 'label': '', 'choice': ['match nul', ],
        # 'result': None}, ....]
        self.relaunch = relaunch  # not None if launched at first time from database
        self.lignes = []
        self.list_matches = []
        if self.relaunch is None:
            self.display()
        else:
            self.display_rounds_result()

    def display(self) -> None:
        """ displays  the window that allows the user to enter the winners for the current round
        GUI uses OptionMenu"""
        # ask info to display to controller
        self.list_matches = ct.Controls.get_current_matches()
        for elem in self.list_matches:  # setup the data to be displayed
            p1 = str(elem.player1)
            p2 = str(elem.player2)
            match = p1 + ' vs ' + p2
            self.lignes.append({'match_instance': elem, 'label': match, 'choice': ['match nul', p1, p2],
                                'result': None})
        for index, elem in enumerate(self.lignes):  # display the data
            self.widgets.append(self.my_simple_line(self.master, elem['label'], index + 1, 0, 1, 1, 10, 10))
            elem['result'], menu_option = self.my_option_menu(self.master, elem['choice'], index + 1, 1, 1, 1, 10, 10)
            self.widgets.append(menu_option)
        # display the button to go through next step of tournament
        self.widgets.append(self.my_button(self.master, 'Clôturer ce tour', 0, len(self.lignes) + 1, self.save_scores))

    def save_scores(self) -> None:
        """ method to save scores of one round """
        # generate scores for this round for all players and save it in the Match instances and create end_time
        # of round order = {'order': <order>, 'left_window_value': <value to display>}
        order = ct.Controls.save_scores(self.lignes)
        # order = ct.Controls.end_round(self.lignes)
        self.master.master.list_instances_menus_tournament = Menu.update_menus_tournament(order, self.master)
        self.master.master.left_window.update_and_display(
            self.master.master.list_instances_menus_tournament)
        self.master.master.launch()
        # self.destroy_window()
        self.destroy_widgets()
        self.display_rounds_result()

    def display_rounds_result(self) -> None:
        """ display the results of all the rounds played and the rank of each player """
        self.master.master.geometry("700x500")
        # ask the data to controller
        order = ct.Controls.display_round_result()
        # round title displayed
        self.my_simple_line(master=self.master, name=order['name'], r=0, c=1, rsp=1, csp=1, px=10, py=10)
        # construct headers
        headers = ['nom du joueur', 'total de points du tournoi', 'rang avant le tournoi']
        for index, name in enumerate(headers):
            self.my_simple_line(master=self.master, name=name, r=1, c=index, rsp=1, csp=1, px=10, py=10)
        # construct one line for each player of tournament
        lignes = []
        for match in order['matches']:
            lignes.append([])
            lignes[-1].append(str(match.player1))
            lignes[-1].append(match.player1.tournament_total_points)
            lignes[-1].append(match.player1.rank)
            lignes.append([])
            lignes[-1].append(str(match.player2))
            lignes[-1].append(match.player2.tournament_total_points)
            lignes[-1].append(match.player2.rank)

        for index, ligne in enumerate(lignes):  # display each player information by line
            for ind, elem in enumerate(ligne):
                self.my_simple_line(master=self.master, name=elem, r=1 + index + 1, c=ind, rsp=1, csp=1, px=10, py=10)
        # display hte button to go through next step of tournament
        self.my_button(master=self.master, name='Fermer le tableau', c=1, r=100, action=self.action_to_do)

    def action_to_do(self) -> None:
        """ 1 - get from controller the next action to do, update the menus and the left window and apply the changes
         2 - close the actual window"""
        # 1
        order = ct.Controls.end_round()
        self.master.master.list_instances_menus_tournament = Menu.update_menus_tournament(order, self.master)
        self.master.master.left_window.update_and_display(self.master.master.list_instances_menus_tournament)
        self.master.master.launch()
        # 2
        self.master.destroy()


class ChooseTournamentForReport(GenericWindow):
    """ used to display the choice of the tournament to use for the report """
    def __init__(self, master, option, **kwargs):
        """ initialize variables """
        GenericWindow.__init__(self, master, **kwargs)
        self.choice = None
        self.top = tk.Toplevel(self.master)
        self.title = 'Sélectionner le tournoi :'
        self.label_line = 'Choisir le tournoi'
        self.path_to_folder = os.path.join(os.path.abspath(os.path.curdir), 'Reports')
        self.message_path_to_folder = "Le rapport est créé et disponible\n\nChemin d'accès au rapport:" \
                                      "\n\n{}".format(self.path_to_folder)
        self.tournament = None
        self.name = option
        self.filtres = ['list_all_actors', 'list_all_tournaments']
        self.report = ct.GenerateReports
        if self.name in self.filtres:
            self.report(self.name)
            msg.showinfo(title=None, message=self.message_path_to_folder)
            self.master.destroy()
            self.master.master.launch()
        else:
            self.get_tournament_names_from_controller()
            self.__display()

    def get_tournament_names_from_controller(self) -> None:
        """ get data from controller to display the tournaments """
        # self.choice = ct.GenerateReports(self.name).get_tournament_names_for_gui()
        self.choice = self.report(self.name).get_tournament_names_for_gui()

    def __display(self) -> None:
        """ display the window """
        # self.top = tk.Toplevel(self.master)
        self.top.grid()
        # title
        self.my_simple_line(self.top, self.label_line, 1, 0, 1, 1, 10, 10)
        # # path to folder where reports are stored
        # self.my_simple_line(self.top, self.message_path_to_folder, 2, 0, 1, 1, 10, 10)
        # choice of tournament
        self.my_simple_line(self.top, self.title, 3, 0, 1, 1, 10, 10)
        self.tournament, menu_option = self.my_option_menu(self.top, self.choice, 3, 1, 1, 1, 10, 10)
        # display the button to go through next step of tournament
        self.my_button(self.top, 'Valider', 0, 4, self.__validate)

    def __validate(self):
        """ create the report with info selected by user """
        self.report(self.name).receive_info_from_gui(self.tournament.get())
        msg.showinfo(title=None, message=self.message_path_to_folder)
        self.master.master.launch()
        self.master.destroy()
