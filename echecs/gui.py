import tkinter as tk
# import tkinter.messagebox as mb  # use it as follow: mb.showinfo(title=<TITRE>, message=<MESSAGE>)


import config as cf
import controleurs as ct


class MainWindow(tk.Tk):
    """ main window of the GUI """
    def __init__(self):
        tk.Tk.__init__(self)
        # size of the several windows displayed during the program
        self.size_main = cf.size_main
        self.size_tournament = cf.size_tournament
        self.size_add_player = cf.size_add_player
        self.size_left_window = cf.size_left_window
        self.size_round_in_progress = cf.size_round_in_progress
        self.size_closing_round = cf.size_closing_round
        # title of the main window
        self.title(cf.title_main_window)
        # apply the size of the main window at start
        self.geometry(self.size_main)
        # initialize variable for parameters to send to controller
        self.menus_states_for_controller_file = []
        # name of the text file used to send the parameters to controller
        self.update_menus_file = cf.update_menus_file
        # build the two containers to displays windows
        self.create_right_left_containers()
        # create the instances for the main menus
        self.list_instances_menus_tournament = Menu.initialize_menus_instances_tournament()
        self.list_instances_menus_reports = Menu.initialize_menus_instances_reports()
        # initialize self.menus_states_for_controller_file = []
        self.initialize_menus_states_for_controller_file()
        # write file for communication
        ct.Controls.write_menus_states(self.menus_states_for_controller_file)
        # display the GUI
        self.launch()

    def initialize_menus_states_for_controller_file(self):
        """ initialize the self.menus_states_for_controller_file variable,
         it will be used to create a file to communicate with controller """
        for elem in self.list_instances_menus_tournament:
            self.menus_states_for_controller_file.append(elem.create_menu_states())

    def create_right_left_containers(self):
        """ create the containers where the windows are displayed """
        self.frame_left = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_left.grid(row=0, column=0)
        # self.window_left_info = None
        self.frame_right = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_right.grid(row=0, column=1)

    def launch(self):
        """ displays the GUI """
        # read the state file created by controller to adapt the GUI
        self.menus_states_for_controller_file = ct.Controls.read_menus_states()
        # create the containers that contain the windows
        self.create_right_left_containers()
        # displays the left window
        LeftWindow.display_left_window(self)
        # display the menubar
        self.menubar = tk.Menu(self)
        Menu.update_menus(self.list_instances_menus_tournament, self.menus_states_for_controller_file)
        menus_to_display = Menu.setup_main_menus_architecture(self.list_instances_menus_tournament,
                                                              self.list_instances_menus_reports)
        for elem in menus_to_display:
            menu = tk.Menu(self.menubar, tearoff=0)
            for el in elem['unfold']:
                menu.add_command(label=el['label'], state=el['state'],
                                 command=eval(el['function'], {'RightWindow': RightWindow, 'self': self}))
            self.menubar.add_cascade(label=elem['name'], menu=menu)
        self.config(menu=self.menubar)

    def test(self):
        """ while construction is in progress. MUST BE ERASED AT THE END"""
        print('methode test')


class Menu:
    """ Generate each menu to be displayed in the GUI and manage all the operations to
     perform on them"""

    def __init__(self, name, label, class_to_use, size, state, left_window_label, left_window_value):
        """ initilaize a Menu instance with parameters """
        self.name = name
        self.label = label
        self.class_to_use = class_to_use
        self.size = size
        self.state = state
        self.left_window_label = left_window_label
        self.left_window_value = left_window_value

    def create_menu_states(self):
        """ return a dictionary with info regarding the Menu instance
        used for communication file with controller """
        return {'name': self.name, 'state': self.state, 'left_window_label': self.left_window_label,
                'left_window_value': self.left_window_value}

    @classmethod
    def initialize_menus_instances_tournament(cls):
        """ initialize the menus for the GUI, it is used by MainWindow to create menus"""
        tournament_start = Menu(name='tournament_start', label="Créer le tournoi", class_to_use=CreateNewTournament,
                                size=cf.size_tournament,
                                state='normal', left_window_label='Tournoi', left_window_value='non créé')
        add_players = Menu(name='add_players', label="Ajouter les joueurs", class_to_use=AddPlayers,
                           size=cf.size_add_player,
                           state='disabled', left_window_label='Joueurs',
                           left_window_value='0/{}'.format(cf.number_of_players))
        launch_round = Menu(name='launch_round', label="Lancer le tour", class_to_use=LaunchRound,
                            size=cf.size_round_in_progress,
                            state='disabled', left_window_label='Tour en cours', left_window_value='aucun')
        close_round = Menu(name='close_round', label='Cloturer le tour', class_to_use=CloseRound,
                           size=cf.size_closing_round, state='disabled',
                           left_window_label='Tour terminé', left_window_value='aucun')
        return [tournament_start, add_players, launch_round, close_round]

    @classmethod
    def initialize_menus_instances_reports(cls):
        """ initialize the menus for the GUI, it is used by MainWindow to create menus"""
        list_all_actors = Menu(name='list_all_actors', label="liste de tous les acteurs",
                               class_to_use=ct.GenerateReports,
                                size=cf.size_tournament,
                                state='disabled', left_window_label='report', left_window_value='report')
        list_all_players_current_tournament = Menu(name='list_all_players_current_tournament',
                                                   label="liste des joueurs du tournoi actuel",
                                                   class_to_use=ct.GenerateReports,
                                                   size=cf.size_add_player, state='disabled',
                                                   left_window_label='report', left_window_value='report')
        list_all_tournaments = Menu(name='list_all_tournaments', label="liste de tous les tournois",
                                    class_to_use=ct.GenerateReports, size=cf.size_round_in_progress,
                                    state='disabled', left_window_label='report', left_window_value='report')
        list_all_rounds_of_tournament = Menu(name='list_all_rounds_of_tournament',
                                             label="liste de tous les tours d'un tournoi",
                                             class_to_use=ct.GenerateReports, size=cf.size_closing_round,
                                             state='disabled', left_window_label='report',
                                             left_window_value='report')
        list_all_matches_of_tournament = Menu(name='list_all_matches_of_tournament',
                                             label="liste de tous les matchs d'un tournoi",
                                             class_to_use=ct.GenerateReports, size=cf.size_closing_round,
                                             state='disabled', left_window_label='report',
                                             left_window_value='report')
        return [list_all_actors, list_all_players_current_tournament, list_all_tournaments,
                list_all_rounds_of_tournament, list_all_matches_of_tournament]


    @classmethod
    def setup_main_menus_architecture(cls, instances_tournament, instances_report):
        """ setup the main menus architecture to display"""
        return [{'name': "tournoi actuel",
                 'unfold': [{'label': elem.label, 'state': elem.state,
                             'function': "lambda i= ['" + elem.name + "', self.frame_right, "
                                                                      "self.list_instances_menus_tournament]: "
                                                                      "RightWindow.display_right_window(i)"}
                            for elem in instances_tournament]},
                {'name': "ouvrir / sauvegarder le tournoi",
                 'unfold': [{'label': "Ouvrir un tournoi sauvegardé", 'state': 'normal',
                             'function': 'self.test'},
                            {'label': "Sauvegarder le tournoi en cours", 'state': 'disabled',
                             'function': 'self.test'}]},
                {'name': "générer les rapports",
                 'unfold': [{'label': elem.label, 'state': elem.state,
                             'function': 'self.test'} for elem in instances_report]}]

    @classmethod
    def update_menus(cls, list_instances_menus_tournament, menus_states_for_controller_file):
        """ update the main menu of the gui with the new states """
        for elem, el in zip(list_instances_menus_tournament, menus_states_for_controller_file):
            elem.state = el['state']
            elem.left_window_value = el['left_window_value']


class RightWindow:
    """ displays a window inside a pre created right container.
     You must define the master, the class to use and the row and column to setup your
     window"""
    def __init__(self, size, class_to_use, master, row, column):
        """ initialize all the needed variables with parameters """
        master.master.geometry(size)
        self.window = class_to_use(master=master, borderwidth=0, relief=tk.GROOVE)
        self.window.grid(row=row, column=column, padx=10, pady=20)
        # master.master.last_created_window = self.window
        # master.master.windows['right_window'] = self.window

    @classmethod
    def display_right_window(cls, list):
        """ display the window in the right container
        entry : list with following data [name, master, list_instances_menus_tournament]"""
        for elem in list[2]:
            if elem.name == list[0]:
                cls(size=elem.size, class_to_use=elem.class_to_use, master=list[1], row=1, column=0)


class GenericWindow(tk.Frame):
    """ This class define generic commands for windows to be displayed inside the GUI"""
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.data = []  # data with following structure {'name': <NAME>, 'tk_object': <tkObject>}
        self.attributs = {}
        self.menus_states = ct.states

    def my_line(self, master, name, r, c, rsp, csp, px, py):
        """ this method generates a line with a label in a column and an Entry in the column next to it
         It also saves the Entry in the self.data variable
         """
        line = tk.Label(master=master, text=name, anchor='w')
        line.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        l2 = tk.Entry(master=master)
        l2.grid(row=r, column=c + 1, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        self.data.append({'name': name, 'tk_object': l2})

    def my_data(self, master, name1, name2, r, c, rsp, csp, px, py):
        """ this method generates two lines with one label each """
        line1 = tk.Label(master=master, text=name1, anchor='w', font="Helvetica 12 bold")
        line1.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        line2 = tk.Label(master=master, text=name2, anchor='w')
        line2.grid(row=r+1, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)

    def my_button(self, master, name, c, r, action):
        """ this method generates a button with a text and an action to perform when clicked"""
        b = tk.Button(master=master, text=name, command=action)
        b.grid(row=r, column=c, rowspan=1, columnspan=1, padx=10, pady=10)

    def destroy_window(self):
        """ destroy the actual window and reset the containers """
        self.master.destroy()
        self.master.master.create_right_left_containers()

    def reset_window(self):
        """ reset the actual window and update left window information"""
        for elem in self.master.winfo_children():
            elem.destroy()
        self.master.master.menus_states_for_controller_file = ct.Controls.read_menus_states()
        self.master.master.create_right_left_containers()
        LeftWindow.display_left_window(self.master.master)


    def test(self):
        """ to be deleted when program finished """
        print('test')


class LeftWindow(GenericWindow):
    """ display the information of the tournament to allow the user to see its evolution """
    def __init__(self, master, **kwargs):
        """ initialize the variables needed and display the left window """
        GenericWindow.__init__(self, master, **kwargs)
        self.values = {}
        self.get_data()
        self.display(master)

    def get_data(self):
        """ get data from the communication file with controller and save it into self.values """
        try:
            data = ct.Controls.read_menus_states()
        except FileNotFoundError:
            data = []
        for elem in data:
            self.values.update({elem['left_window_label']: elem['left_window_value']})

    def display(self, master):
        """ display the window and the information of tournament steps"""
        ligne = 0
        for key, value in self.values.items():
            self.my_data(master, key, value, ligne, 0, 1, 1, 2, 2)
            ligne += 2
        # master.master.windows['left_window'] = self

    @classmethod
    def display_left_window(cls, master):
        """ Display the tournament information available """
        master.geometry(master.size_left_window)
        window_left_info = cls(
            master=master.frame_left,
            borderwidth=0, relief=tk.GROOVE)
        window_left_info.grid(row=1, column=0, padx=10, pady=20)


class CreateNewTournament(GenericWindow):
    """ create a new tournament """

    def __init__(self, master, **kwargs):
        """ initialize variable and display the window to create tournament """
        GenericWindow.__init__(self, master, **kwargs)
        self.states = None
        self.display(master)

    def display(self, master):
        """ displays  the window """
        labels = [value for value in cf.labels_tournament_creation.values()]
        for index, elem in enumerate(labels):
            self.my_line(master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(master, 'créer le tournoi', 0, len(labels)+1, self.create_new_tournament)

    def create_new_tournament(self):  # TO BE MODIFIED
        """ 1 - gather all the user inputs and update the corresponding variable
            2 - send info and request to controller
            3 - relaunch main window and destroy actual right window
            """
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
        ct.Controls.verify_tournament_creation(self.attributs)
        self.master.master.launch()
        # 3
        self.destroy_window()


class AddPlayers(GenericWindow):
    """ create a window to add a new player to the tournament """
    def __init__(self, master, **kwargs):
        """ initialize variables """
        GenericWindow.__init__(self, master, **kwargs)
        self.master = master
        self.all_players_created = False
        self.display()

    def reset_variables(self):
        """ reset variables """
        self.attributs = {}
        self.data = []

    def display(self):
        """ displays  the window """
        self.reset_variables()
        labels = [value for value in cf.labels_add_players.values()]
        for index, elem in enumerate(labels):
            self.my_line(self.master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(self.master, 'ajouter le joueur', 1, len(labels) + 1, self.add_new_player)

    def add_new_player(self):  # TO BE DONE
        """ 1 - gather the user inputs into self.attributs
            2 - send info to controller  and update left window
            3 - reset the window to enter a new player or close this window"""

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
        self.all_players_created = ct.Controls.verify_players_creation(self.attributs)

        # 3
        if not self.all_players_created:
            self.reset_window()
            self.display()
        else:
            self.destroy_window()
            self.master.master.launch()


class LaunchRound(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.round_number = None
        self.master = master
        self.display_round_creation()

    def display_round_creation(self):
        """ displays  the window """
        labels = [value for value in cf.labels_round_creation.values()]
        for index, elem in enumerate(labels):
            self.my_line(self.master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(self.master, 'créer le tour', 0, len(labels)+1, self.create_new_round)

    def create_new_round(self):
        """ create and launch the round
        1 - gather all the information entered by user and save them into variable
        2 - send info to controller and receive order in return
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
        ct.Controls.verify_round_creation(self.attributs)

        # 3
        self.reset_window()
        self.display_round_information()

    def display_round_information(self):
        """ display the matches to be played during this round """
        print('dans display_round_information:\n')
        print('1 - generation des pairs\n2 - enregistrer les matches\n3 - afficher les matches')
        ct.Controls.generate_matches()


class CloseRound(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.display(master, ['john', 'papa', 'maman', 'luli', 'moi', 'papou', 'madou', 'jess'])

    def display(self, master, list_players):
        """ displays  the window that allows the user to enter scores for the round that just stopped"""
        for index, elem in enumerate(list_players):
            self.my_line(master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(master, 'Valider les scores', 0, len(list_players)+1, self.validate_scores)

    def validate_scores(self):
        """ method to save scores of one round """
        print('VALIDATION DES SCORES à créer')
