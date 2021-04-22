import tkinter as tk
import tkinter.messagebox as mb  # use it as follow: mb.showinfo(title=<TITRE>, message=<MESSAGE>)


import config_v2 as cf
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
        # authorization parameters for controller
        self.authorization = cf.authorization
        # display the main menus of the gui
        self.menus_main = cf.menus_main
        # name of the json file used to update self.authorization
        self.update_menus_file = cf.update_menus_file
        # build the two secondary windows to displays information
        self.create_secondary_windows()
        # stock the last created window to be able to reset it if needed
        self.windows = {'left_window': None, 'right_window': None}
        self.last_created_window = None
        self.launch()

    def create_secondary_windows(self):
        self.frame_left = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_left.grid(row=0, column=0)
        self.window_left_info = None
        self.frame_right = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_right.grid(row=0, column=1)

    def show_error_message(self, title, message):
        mb.showinfo(title=title, message=message)

    def display_left_window_informations(self):
        """ Displays the tournament information available """
        self.geometry(self.size_left_window)
        self.window_left_info = LeftWindow(
            master=self.frame_left,
            display_dictionary=cf.display_dictionary,
            borderwidth=0, relief=tk.GROOVE)
        self.window_left_info.grid(row=1, column=0, padx=10, pady=20)

    def update_menus(self):
        """ update the main menus of the gui"""
        return [{'name': "tournoi actuel",
                 'unfold': [{'label': elem['label'], 'state': elem['state'],
                             'function': "lambda i= '" + elem['name'] + "': self.display_right_window(i)"}
                            for elem in self.authorization]},
                {'name': "ouvrir / sauvegarder le tournoi",
                 'unfold': [{'label': "Ouvrir un tournoi sauvegardé", 'state': 'normal',
                             'function': 'self.test'},
                            {'label': "Sauvegarder le tournoi en cours", 'state': 'disabled',
                             'function': 'self.test'}]},
                {'name': "générer les rapports",
                 'unfold': [{'label': "liste de tous les acteurs", 'state': 'disabled',
                             'function': 'self.test'},
                            {'label': "liste des joueurs du tournoi actuel", 'state': 'disabled',
                             'function': 'self.test'},
                            {'label': "liste de tous les tournois", 'state': 'disabled',
                             'function': 'self.test'},
                            {'label': "liste de tous les tours d'un tournoi", 'state': 'disabled',
                             'function': 'self.test'},
                            {'label': "liste de tous les matchs d'un tournoi", 'state': 'disabled',
                             'function': 'self.test'}]}]

    def launch(self):
        """ displays the main window of the GUI """
        # displays the left window
        self.display_left_window_informations()
        # displays the menubar using the config file in the package
        self.menubar = tk.Menu(self)
        self.menus_main = self.update_menus()
        for elem in self.menus_main:
            menu = tk.Menu(self.menubar, tearoff=0)
            for el in elem['unfold']:
                menu.add_command(label=el['label'], state=el['state'], command=eval(el['function'], {'self': self}))
            self.menubar.add_cascade(label=elem['name'], menu=menu)
        self.config(menu=self.menubar)
        ct.write_menus_states(self.authorization)

    def test(self):
        """ while construction is in progress. MUST BE ERASED AT THE END"""
        print('methode test')

    def display_right_window(self, name):
        """ send a request to the controller to authorize actions """
        for elem in self.authorization:
            for key, value in elem.items():
                if (key == 'name') & (value == name):
                    DisplayWindow(size=elem['size'],
                                  class_to_use=eval(elem['class']),
                                  master=self.frame_right, row=1, column=0)


class DisplayWindow:
    """ displays a window inside a pre created container. This window is created
     with a class. You must define the master, the class to use and the row and column to put your
     window"""
    def __init__(self, size, class_to_use, master, row, column):
        master.master.geometry(size)
        self.window = class_to_use(master=master, borderwidth=0, relief=tk.GROOVE)
        self.window.grid(row=row, column=column, padx=10, pady=20)
        master.master.last_created_window = self.window
        master.master.windows['right_window'] = self.window


class DisplayMenus:
    def __init__(self, master, menus_to_display):
        self.menubar = tk.Menu(master)
        for elem in menus_to_display:
            menu = tk.Menu(self.menubar, tearoff=0)
            for el in elem['unfold']:
                menu.add_command(label=el['label'], command=eval(el['function']))
            self.menubar.add_cascade(label=elem['name'], menu=menu)
        # self.config(menu=self.menubar)


class GenericWindow(tk.Frame):
    """ This class define generic commands for all windows to be displayed inside the GUI"""
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.data = []  # data with following structure {'name': <NAME>, 'tk_object': <tkObject>}
        self.attributs = {}
        self.menus_states = ct.states

    def my_line(self, master, name, r, c, rsp, csp, px, py):
        """ this method generates a line with a label in a column and an Entry in the column next to it
         It also saves the Entry in the self.data variable to be used later by the controller part
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

    def reset(self, master):
        """ reset the whole window """
        for index, elem in enumerate(master.winfo_children()):
            elem.destroy()

    def destroy_previous_window(self):  # TO BE MODIFIED
        """ destroy a previous window that might still be displayed """
        if self.master.master.last_created_window is not None:
            self.master.master.last_created_window.destroy()
            self.master.master.last_created_window = None

    def destroy_window(self):
        """ destroy the actual window and reset the main window """
        self.master.destroy()
        self.master.master.create_secondary_windows()

    def update_main_window_menus(self):
        """ update the main menu of the gui with the new states """
        self.master.master.authorization = ct.read_menus_states()
        self.master.master.launch()

    def actions_to_perform_when_button_clicked(self):
        """ generic actions to perform when a button is clicked (1 to 4)
         this method must be combined with steps to be written in the specific function (0)
         0 - specific function = gather all the user inputs and update the corresponding variable
         1 - create a text file with menus states of the main window (to be used by controller)
         2 - send the updated variable to controller
         3 - when controller has finished its work,
         update the menus of the main window and left window
         using the new text file created by controller
            """
        # 1
        ct.write_menus_states(self.menus_states)
        # 2
        ct.receive_gui_tournament_info(self.attributs)
        # 3
        self.update_main_window_menus()
        left_window = self.master.master.windows['left_window']
        left_window.update_window(self.master.master.frame_left)

    def test(self):
        """ to be deleted when program finished """
        print('test')


class LeftWindow(GenericWindow):
    """ display the information of the tournament to allow the user to see its evolution """
    def __init__(self, master, display_dictionary, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.values = {}
        self.get_data()
        self.display(master)

    def get_data(self):
        try:
            data = ct.read_menus_states()
        except FileNotFoundError:
            data = cf.authorization
        for elem in data:
            self.values.update({elem['left_window']['label']: elem['left_window']['value']})

    def display(self, master):
        """ displays  the window """
        ligne = 0
        for key, value in self.values.items():
            self.my_data(master, key, value, ligne, 0, 1, 1, 2, 2)
            ligne += 2
        self.master.master.windows['left_window'] = self

    def update_window(self, master):
        """ update the display when changes occur """
        self.get_data()
        self.reset(master)
        self.display(master)


class CreateNewTournament(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.destroy_previous_window()
        self.display(master)

    def display(self, master):
        """ displays  the window """
        labels = [value for value in cf.labels_tournament_creation.values()]
        for index, elem in enumerate(labels):
            self.my_line(master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(master, 'créer le tournoi', 0, len(labels)+1, self.create_new_tournament)

    def create_new_tournament(self):  # TO BE MODIFIED
        """ 1 - gather all the user inputs and update the corresponding variable
            2 - use the generic method to perform automatic tasks
            3 - destroy window
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
        self.actions_to_perform_when_button_clicked()
        # 3
        self.destroy_window()


class AddPlayers(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.master = master
        self.players = []
        self.destroy_previous_window()
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
        self.my_button(self.master, 'ajouter le joueur', 0, len(labels) + 1, self.add_new_player)
        self.my_button(self.master, 'valider la liste de joueurs', 1, len(labels) + 1, self.validate_players)

    def add_new_player(self):  # TO BE DONE
        """ 1 - gather the user inputs into self.attributs
            2 - send info to controller  and update left window
            3 - reset the window to enter a new player"""
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
        print('dans add_new_player\n', self.attributs)
        # 2
        self.actions_to_perform_when_button_clicked()
        #3
        self.reset(self.master)
        self.display()


    def validate_players(self):
        """ 1 - send info to controller that all players have been added
            2 - get
            3 - reset the window to enter a new player"""


class LaunchRound(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.destroy_previous_window()
        self.display(master)

    def display(self, master):
        """ displays  the window """
        self.my_data(master, 'TOUR N° ?', 'En cours....', 0, 0, 1, 1, 10, 10)
        self.my_button(master, 'Finir le tour', 0, 2, self.end_tour)

    def end_tour(self, master):
        """ end the tour in progress """
        print('Fonction à créer... Doit lancer la classe CloseRound')
        self.reset(master)


class CloseRound(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.destroy_previous_window()
        self.display(master, ['john', 'papa', 'maman', 'luli', 'moi', 'papou', 'madou', 'jess'])

    def display(self, master, list_players):
        """ displays  the window that allows the user to enter scores for the round that just stopped"""
        for index, elem in enumerate(list_players):
            self.my_line(master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(master, 'Valider les scores', 0, len(list_players)+1, self.validate_scores)

    def validate_scores(self):
        """ method to save scores of one round """
        print('VALIDATION DES SCORES à créer')


if __name__ == "__main__":
    print('ok')
