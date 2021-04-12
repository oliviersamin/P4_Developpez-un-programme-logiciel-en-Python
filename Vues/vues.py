"""
Project 4 of OpenClassRooms Cursus:
Développez un programme logiciel en Python
"""
import tkinter as tk
import tkinter.messagebox as mb  # use it as follow: mb.showinfo(title=<TITRE>, message=<MESSAGE>)

from Controleurs import controleurs as ct

class GUI(tk.Tk):
    """ main window of the GUI """
    def __init__(self):
        tk.Tk.__init__(self)
        # size of the several windows dispayed during the program
        self.size_main = "550x300"
        self.size_tournament = "550x380"
        self.size_add_player = "550x350"
        self.size_left_window = "550x400"
        self.size_round_in_progress = "550x300"
        self.size_closing_round = "550x450"
        # title of the main window
        self.title("Centre d'échecs")
        # apply the size of the main window at start
        self.geometry(self.size_main)
        # build the two secondary windows to displays information
        self.frame_left = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_left.grid(row=0, column=0)
        self.window_left_info = None
        self.frame_right = tk.Frame(self, borderwidth=5, relief=tk.GROOVE)
        self.frame_right.grid(row=0, column=1)
        # stock the last created window to be able to reset it if needed
        self.last_created_window = None
        # launch the controlers check
        self.new_tournament = ct.Tournament()
        self.launch()

    def display_create_tournement_window(self):
        """ displays tournament window so the user can create
        a new tournament and enter all the needed data"""
        if not self.new_tournament.tournament_start:
            self.geometry(self.size_tournament)
            self.window_new_tournement = CreateNewTournement(master=self.frame_right, borderwidth=0, relief=tk.GROOVE)
            self.window_new_tournement.grid(row=1, column=0, padx=10, pady=20)
            self.last_created_window = self.window_new_tournement
        else:
            mb.showinfo(title='ATTENTION', message='UN TOURNOI EST DÉJA CRÉÉ')

    def display_add_new_player_window(self):
        """ displays tournament window so the user can create
        a new tournament and enter all the needed data"""
        if self.new_tournament.tournament_start:
            self.geometry(self.size_add_player)
            self.window_new_player = AddPlayers(master=self.frame_right, borderwidth=0, relief=tk.GROOVE)
            self.window_new_player.grid(row=1, column=0, padx=10, pady=20)
            self.last_created_window = self.window_new_player
        else:
            mb.showinfo(title='ATTENTION', message="Créez un tournoi avant de créer des joueurs")

    def display_left_window_informations(self):
        """ Displays the tournement information available """
        self.geometry(self.size_left_window)
        self.window_left_info = LeftWindow(master=self.frame_left, borderwidth=0, relief=tk.GROOVE)
        self.window_left_info.grid(row=1, column=0, padx=10, pady=20)

    def display_window_round_in_progress(self):
        """ Displays the round in progress window """
        self.geometry(self.size_round_in_progress)
        self.window_round_in_progress = LaunchRound(master=self.frame_right, borderwidth=0, relief=tk.GROOVE)
        self.window_round_in_progress.grid(row=1, column=0, padx=10, pady=20)
        self.last_created_window = self.window_round_in_progress

    def display_window_closing_round(self):
        """ Displays the round in progress window """
        self.geometry(self.size_closing_round)
        self.window_closing_round = CloseRound(master=self.frame_right, borderwidth=0, relief=tk.GROOVE)
        self.window_closing_round.grid(row=1, column=0, padx=10, pady=20)
        self.last_created_window = self.window_closing_round

    def launch(self):
        """ displays the main window of the GUI """
        self.display_left_window_informations()
        # print ('dans lancer')
        self.menubar = tk.Menu(self)
        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Créer le tournoi", command=self.display_create_tournement_window)
        # self.menu2.add_command(label=tk.Entry(self),command=self.nada)
        self.menu2.add_command(label="Ajouter les joueurs", command=self.display_add_new_player_window)
        # self.menu2.add_separator()
        self.menu2.add_command(label="Lancer le tour", command=self.display_window_round_in_progress)
        self.menu2.add_command(label='Cloturer le tour', command=self.display_window_closing_round)
        self.menubar.add_cascade(label="tournoi actuel", menu=self.menu2)

        self.menu4 = tk.Menu(self.menubar, tearoff=0)
        self.menu4.add_command(label="Ouvrir un tournoi sauvegardé", command=self.test)
        self.menu4.add_command(label="Sauvegarder le tournoi en cours", command=self.test)
        # self.menu4.add_separator()
        self.menubar.add_cascade(label="ouvrir / sauvegarder le tournoi", menu=self.menu4)

        self.menu3 = tk.Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="liste de tous les acteurs", command=self.test)
        self.menu3.add_command(label="liste des joueurs du tournoi actuel", command=self.test)
        self.menu3.add_command(label="liste de tous les tournois", command=self.test)
        self.menu3.add_command(label="liste de tous les tours d'un tournoi", command=self.test)
        self.menu3.add_command(label="liste de tous les matchs d'un tournoi", command=self.test)
        # self.menu3.add_separator()
        # self.menu1.add_command(label='menu1 - 4', command=self.destroy)
        self.menubar.add_cascade(label="générer les rapports", menu=self.menu3)

        self.config(menu=self.menubar)
        #  self.bind_all("<Alt-d>", self.test)

    def test(self):
        """ """
        print('methode test')


class GenericWindow(tk.Frame):
    """ This class define generic commands for all windows to be displayed inside the GUI"""
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.data = []  # data with following struture {'name': <NAME>, 'tk_object': <tkObject>}

    def my_line(self, name, r, c, rsp, csp, px, py):
        """ this method generates a line with a label in a column and an Entry in the column next to it
         It also saves the Entry in the self.data variable to be used later by the controller part
         """
        line = tk.Label(self, text=name, anchor='w')
        line.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        l2 = tk.Entry(self)
        l2.grid(row=r, column=c + 1, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        self.data.append({'name': name, 'tk_object': l2})

    def my_data(self, name1, name2, r, c, rsp, csp, px, py):
        """ this method generates two lines with one label each """
        line1 = tk.Label(self, text=name1, anchor='w', font="Helvetica 12 bold")
        line1.grid(row=r, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)
        line2 = tk.Label(self, text=name2, anchor='w')
        line2.grid(row=r+1, column=c, rowspan=rsp, columnspan=csp, padx=px, pady=py)

    def my_button(self, name, c, r, action):
        """ this method generates a button with a text and an action to perform when clicked"""
        b = tk.Button(self, text=name, command=action)
        b.grid(row=r, column=c, rowspan=1, columnspan=1, padx=10, pady=10)

    def reset(self):
        """ reset the all window """
        for index, elem in enumerate(self.winfo_children()):
            elem.destroy()

    def destroy_previous_window(self):
        """ destroy a previous window that might still be displayed """
        if self.master.master.last_created_window is not None:
            self.master.master.last_created_window.destroy()
            self.master.master.last_created_window = None

    def display_variables(self):
        """ test methos while the program is being built.
         TO BE ERASE AT THE END"""
        for elem in self.data:
            print(elem['tk_object'].get())
        self.destroy()
        self.master.master.geometry(self.master.master.size_main)


class LeftWindow(GenericWindow):
    """ display the information of the tournament to allow the user to see its evolution """
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.values = {'Statut tournoi': 'non créé', 'Joueurs': '0/8', 'Tour en cours': 'aucun'}
        self.display()

    def display(self):
        """ displays  the window """

        ligne = 0
        for key, value in self.values.items():
            self.my_data(key, value, ligne, 0, 1, 1, 2, 2)
            ligne +=2

    def update(self):
        """ update the display when changes occur """
        if self.master.master.new_tournament.tournament_start:
            self.values['Statut tournoi'] = 'en cours'
        if self.master.master.new_tournament.players_check:
            self.values['Joueurs'] = '8/8'
        for index, tour in enumerate(self.master.master.new_tournament.rounds_checks):
            if tour:
                self.values['Tour en cours'] = '{}/{}'.format(index+1, len(self.master.master.new_tournament.rounds_checks))
        self.reset()
        self.display()


class CreateNewTournement(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.attributs = ['name', 'location', 'date', 'round_number', 'time_control', 'description']
        self.destroy_previous_window()
        self.display()

    def display(self):
        """ displays  the window """
        labels = ['Nom du tournoi', 'Lieu', 'date', 'Nombre de tours', 'Contrôle du temps', 'Description']
        for index, elem in enumerate(labels):
            self.my_line(elem, index, 0, 1, 1, 10, 10)
        self.my_button('créer le tournoi', 0, len(labels)+1, self.create_new_tournament)  # self.display_variables)

    def create_new_tournament(self):
        """ create a new tournament with all variables """
        self.master.master.new_tournament.tournament_start = True
        for elem,attribut in zip(self.data,self.attributs):
            try:
                setattr(self.master.master.new_tournament, attribut, elem['tk_object'].get())
            except:
                setattr(self.master.master.new_tournament, attribut, elem['tk_object'])
        # print(self.master.master.new_tournament.__dict__)
        self.master.master.window_left_info.update()


class AddPlayers(GenericWindow):
    def __init__(self, master, **kwargs):
        GenericWindow.__init__(self, master, **kwargs)
        self.destroy_previous_window()
        self.display()

    def display(self):
        """ displays  the window """
        labels = ['Nom de famille', 'Prénom', 'Date de naissance', 'Sexe', 'Classement']
        for index, elem in enumerate(labels):
            self.my_line(elem, index, 0, 1, 1, 10, 10)
        self.my_button('ajouter le joueur', 0, len(labels)+1, self.display_variables)
        self.my_button('créer un autre joueur', 1, len(labels) + 1, self.add_new_player)

    def add_new_player(self):
        self.reset()
        self.display()


class LaunchRound(GenericWindow):
    def __init__(self, **kwargs):
        GenericWindow.__init__(self, **kwargs)
        self.destroy_previous_window()
        self.display()

    def display(self):
        """ displays  the window """
        self.my_data('TOUR N° ?', 'En cours....', 0, 0, 1, 1, 10, 10)
        self.my_button('Finir le tour', 0, 2, self.end_tour)

    def end_tour(self):
        """ end the tour in progress """
        print('Fonction à créer... Doit lancer la fenetre de remplissage des scores')
        self.reset()


class CloseRound(GenericWindow):
    def __init__(self, **kwargs):
        GenericWindow.__init__(self, **kwargs)
        self.destroy_previous_window()
        self.display(['john', 'papa', 'maman', 'luli', 'moi', 'papou', 'madou', 'jess'])

    def display(self, list_players):
        """ displays  the window that allows the user to enter scores for the round that just stoped"""
        for index, elem in enumerate(list_players):
            self.my_line(elem, index, 0, 1, 1, 10, 10)
        self.my_button('Valider les scores', 0, len(list_players)+1, self.validate_scores)

    def validate_scores(self):
        """ method to save scores of one round """
        print('VALIDATION DES SCORES à créer')


if __name__ == "__main__":
    GUI().mainloop()
