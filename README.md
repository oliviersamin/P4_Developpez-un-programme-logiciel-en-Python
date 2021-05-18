# P4_Developpez-un-programme-logiciel-en-Python

## Program surroundings

This program is the fourth one on thirteen projects to be validated in order to get a degree as a developer in Python applications.  

For more info on that subject please visit the following website:  
https://openclassrooms.com/fr/paths/322-developpeur-dapplication-python
  

**The aim of this project is to create an appliation to manage a chess tournament following stricts specifications (MVC model and PEP8 mainly)**  


## Preliminary remarks
**This program has been tested with Python version 3.8.5(default, Jan 27 2021, 15:41:15)**     


## Steps to launch the program  

1. Clone the GitHub repository 
2. Create your virtual environment and use requirements.txt to get all the needed modules   
3. Once launched your virtual environment and placed in the root folder, **execute the program using the following command line: python main.py**   

## How to use the program  
**The program is implemented with a GUI for a better end user experience**   
1. Open the 'Tournoi actuel' menu and follow its several steps to go through all the steps of a tournament. 
2. The tournament is automatically saved after each user step. Therfore if the program is closed at any time, it will restart at the last step
of the tournament.
3. The program does not manage several tournaments at the same time, therefore when a tourament is not finished, it must be ended before creating another one.
4. When a tournament is ended, the program does not manage to create a new one. Therefore if the user wants to create a new tournament, he must close the program and relaunch it.
5. The creation of the reports can be done at any time of the tournament. 
6. If a report is not created (example: players of a tournament), it means that there is no data existing (example: no player has been created for this tournament).
   
## Steps to generate a flake8-html file 

1. Once launched your virtual environment and in the root folder, launch the following command line:   
**flake8 --config=config_flake8.ini main.py config.py Controleurs/controleurs.py Vues/gui.py Modeles/modeles.py**
