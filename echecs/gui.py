import tkinter as tk
import tkinter.messagebox as mb  # use it as follow: mb.showinfo(title=<TITRE>, message=<MESSAGE>)


import config_v2 as cf
import controleurs as ct


def send_info_to_controller(info):
    """ send the info entered by user to the controller and modify state parameters of label in
    the main menus to be able to activate next step of tournament
    info is a dictionnary"""
    return(ct.receive_gui_tournament_info(info))

# def read_menus_states():
#     """ reads from a .json file the states of the several submenus of the gui """
#     with (open(cf.update_menus_file,'r') as f):
#         states = f.read()
#     print(states)
#     return(states)
#
# def write_menus_states(menus_states):
#     """ write from self.authorization thes states of the menus in a json file """
#     states = json.dumps(menus_states)
#     with (open(cf.update_menus_file,'w') as f):
#         f.write(states)


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
        # name of the json file used to update self.authorization
        self.update_menus_file = cf.update_menus_file
        # build the two secondary windows to displays information
        self.frame_left = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_left.grid(row=0, column=0)
        self.window_left_info = None
        self.frame_right = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_right.grid(row=0, column=1)
        # stock the last created window to be able to reset it if needed
        self.last_created_window = None
        self.controls = {'tournament_start_request': False, 'add_players_request': False}
        self.launch()

    def show_error_message(self, title, message):
        mb.showinfo(title=title, message=message)

    def display_left_window_informations(self):
        """ Displays the tournement information available """
        self.geometry(self.size_left_window)
        self.window_left_info = LeftWindow(
            master=self.frame_left,
            display_dictionary=cf.display_dictionary,
            borderwidth=0, relief=tk.GROOVE)
        self.window_left_info.grid(row=1, column=0, padx=10, pady=20)

    def launch(self):
        """ displays the main window of the GUI """
        # displays the left window
        self.display_left_window_informations()
        # displays the menubar using the config file in the package
        self.menubar = tk.Menu(self)
        for elem in cf.menus_main:
            menu = tk.Menu(self.menubar, tearoff=0)
            for el in elem['unfold']:
                menu.add_command(label=el['label'], state= el['state'], command=eval(el['function'],{'self': self}))
            self.menubar.add_cascade(label=elem['name'], menu=menu)
        self.config(menu=self.menubar)
        cf.write_menus_states(self.authorization)

    def test(self):
        """ while contruction is in progress. MUST BE ERASED AT THE END"""
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
        self.data = []  # data with following struture {'name': <NAME>, 'tk_object': <tkObject>}
        self.menus_states = None

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
        """ reset the all window """
        for index, elem in enumerate(master.winfo_children()):
            elem.destroy()

    def destroy_previous_window(self):  # TO BE MODIFIED
        """ destroy a previous window that might still be displayed """
        if self.master.master.last_created_window is not None:
            self.master.master.last_created_window.destroy()
            self.master.master.last_created_window = None

    def display_variables(self):  # TO BE MODIFIED
        """ test methos while the program is being built.
         TO BE ERASE AT THE END"""
        for elem in self.data:
            print(elem['tk_object'].get())
        self.destroy()
        self.master.master.geometry(self.master.master.size_main)


class LeftWindow(GenericWindow):
    """ display the information of the tournament to allow the user to see its evolution """
    def __init__(self, master, display_dictionary, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.values = display_dictionary
        self.display(master)

    def display(self, master):
        """ displays  the window """
        ligne = 0
        for key, value in self.values.items():
            self.my_data(master, key, value, ligne, 0, 1, 1, 2, 2)
            ligne += 2

    # def update(self): # TO BE MODIFIED
    #     """ update the display when changes occur """
    #     for index, key in enumerate(self.values):
    #         if (index == 0) & self.master.master.new_tournament.tournament_start:
    #             self.values[key] = cf.update_tournament
    #         if (index == 1) & self.master.master.new_tournament.players_check:
    #             self.values[key] = cf.update_players
    #         if index == 2:
    #             for index, tour in enumerate(self.master.master.new_tournament.rounds_checks[::-1]):
    #                 if tour:
    #                     self.values[key] = '{}/{}'.format(index+1,
    #                     len(self.master.master.new_tournament.rounds_checks))
    #                     break
    #     self.reset()
    #     self.display()


class CreateNewTournament(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.tournament_created = False
        self.attributs = {}
        self.destroy_previous_window()
        self.display(master)

    def display(self, master):
        """ displays  the window """
        labels = ['Nom du tournoi', 'Lieu', 'date', 'Nombre de tours', 'Contrôle du temps', 'Description']
        for index, elem in enumerate(labels):
            self.my_line(master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(master, 'créer le tournoi', 0, len(labels)+1, self.create_new_tournament)

    def create_new_tournament(self):  # TO BE MODIFIED
        """ create a new tournament with all variables and send a signal to controller for en d of
        tournament step by user"""
        for elem in self.data:
            key = ''
            value = ''
            for k, v in elem.items():
                if k == 'name':
                    key = v
                else:
                    value = v.get()
            self.attributs.update({key: value})
        cf.write_menus_states(self.menus_states)
        send_info_to_controller(self.attributs)

    # def create_new_tournament(self):  # TO BE MODIFIED
    #     """ create a new tournament with all variables """
    #     for elem, attribut in zip(self.data, self.attributs):
    #         print(attribut, elem)
    #         # try:
    #         #     setattr(self.master.master.new_tournament, attribut, elem['tk_object'].get())
    #         # except Exception:
    #         #     setattr(self.master.master.new_tournament, attribut, elem['tk_object'])
    #     self.tournament_created = True

class AddPlayers(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.players = []
        self.destroy_previous_window()
        self.display(master)

    def display(self, master):
        """ displays  the window """
        labels = ['Nom de famille', 'Prénom', 'Date de naissance', 'Sexe', 'Classement']
        for index, elem in enumerate(labels):
            self.my_line(master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(master, 'ajouter le joueur', 0, len(labels) + 1, self.display_variables)
        self.my_button(master, 'créer un autre joueur', 1, len(labels) + 1, self.add_new_player)

    def add_new_player(self, master):  # TO BE DONE
        """  """
        self.reset(master)
        self.display(master)


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
        """ displays  the window that allows the user to enter scores for the round that just stoped"""
        for index, elem in enumerate(list_players):
            self.my_line(master, elem, index, 0, 1, 1, 10, 10)
        self.my_button(master, 'Valider les scores', 0, len(list_players)+1, self.validate_scores)

    def validate_scores(self):
        """ method to save scores of one round """
        print('VALIDATION DES SCORES à créer')


if __name__ == "__main__":
    print('ok')
