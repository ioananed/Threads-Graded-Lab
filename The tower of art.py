import os
import threading
import time
from threading import Thread


N_WIZARDS = 0
MAX_PERSONS_TOWER = 0
MAX_WIZARDS_ELEVATOR = 0
ELEVATOR_TRIP_TIME = 0      #ms
N_BOOKS_LIBRARY = 0
MAX_BOOKS_LIBRARY = 0
N_WITCHES = 0

#WIZARDS
#elevator only operates when it is full or no more wizards want to go up or down
#elevator (and also Moist von Lipwig) starts at ground floor and finishes its execution once all wizards have gone up and down the tower.
#at the top floor --> library and wizard takes book
#read for a random amount of time and then wait for elevator to go down
#if no books, wizard must wait for new book to arrive
#dont go to top of tower if witches are there
#no starvation
#magicians and witches must have a fair access to the tower


#Book hunters: find new books for library.
#Team:  Susan Sto Helig, the Luggage and Cohen the Barbarian.
#Must repeat 3 times:
# 1. Go to random place of Discworld --> find 2 books.
# 2. When found two books --> go to the library --> wait until other two book hunters arrive.
# 3. When all book hunters at library --> enter together --> warn Librarian --> wait until Librarian processes the books.
# 4. They will stay at the library a random amount of time before going to find a new book.

#WITCHES:
#arrive to tower --> stay random amount of time --> leave tower
#each witch will go to the tower 3 times


#Solution:
#no startvation
#no deadlocks
#no mutual exclusion: no all magicians to tower and then all witches
#must ensure interleaving
#wizards, witches, librarians and book hunters are threads


#EXERCISE 1: ONLY CONDITIONAL VARIABLES (no semaphores or others)

class Tower(Thread):
    def __init__(self):
        self.wizards = 0
        self.witches = 0


class Library(Thread):
    def __init__(self):
        self.books = 0

class Elevator(Thread):
    def __init__(self):
        self.wizardsInside = 0
        self.witches = 0
        self.wizardsWaitingUp = 0
        self.wizardsWaitingDown = 0
        self.numberOfFloors = 0
    
class BookHuntersCoordinators(Thread):
    def __init__(self):
        self.counter = 0








