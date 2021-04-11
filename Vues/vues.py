"""
Project 4 of OpenClassRooms Cursus:
Développez un programme logiciel en Python
"""
import os
import tkinter as tk


class GUI(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self)
        self.title("Centre d'échecs")
        self.frame = tk.Frame(self)
        self.geometry("600x100")
        self.frame.grid(row=0, column=0)
        self.lancer()

    def lancer(self):
        # print ('dans lancer')
        self.menubar = tk.Menu(self)
        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="changer dossier", command=self.test, accelerator="Alt+D")
        self.menubar.add_cascade(label="Dossier de travail", menu=self.menu1)

        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Créer le tournaoi", command=self.test)
        # self.menu2.add_command(label=tk.Entry(self),command=self.nada)
        self.menu2.add_command(label="Ajouter les joueurs", command=self.test)
        # self.menu2.add_separator()
        self.menu2.add_command(label="Lancer le tour", command=self.test)
        self.menu2.add_command(label='Cloturer le tour', command=self.test)
        self.menubar.add_cascade(label="tournoi actuel", menu=self.menu2)

        self.menu4 = tk.Menu(self.menubar, tearoff=0)
        self.menu4.add_command(label="Ouvrir un tournoi suavegardé", command=self.test)
        self.menu4.add_command(label="Sauvegarder le tournoi en cours", command=self.test)
        # self.menu4.add_separator()
        # self.menu4.add_command(label="concatener images  vertical", command=self.destroy)
        # self.menu1.add_command(label='menu1 - 4', command=self.destroy)
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
        self.bind_all("<Alt-d>", self.test)

    def test(self):
        """ """
        print('methode test')


if __name__ == "__main__":
    GUI().mainloop()