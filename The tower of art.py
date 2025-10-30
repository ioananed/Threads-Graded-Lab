import os
import threading
from time import sleep
from threading import Thread, Condition
import threading as th
import random, sys


N_WIZARDS = 10
MAX_PERSONS_TOWER = 5
MAX_WIZARDS_ELEVATOR = 4 
ELEVATOR_TRIP_TIME = 0.5  # ms
N_BOOKS_LIBRARY = 10
MAX_BOOKS_LIBRARY = 20
N_WITCHES = 0

# ELEVATOR
# elevator only operates when it is full or no more wizards want to go up (only up)
# Once all wizards (MAX_WIZARDS_ELEVATOR or the remaining) are inside the elevator,
# Moist takes them to the top of the Tower (ELEVATOR_TRIP_TIME) and waits for them to leave
# the elevator. Once the elevator is empty, Moist takes the elevator to the ground (ELEVATOR_TRIP_TIME).


# WIZARDS
# at the top floor --> library --> wizard takes book
# read for a random amount of time and then wait for elevator to go down
# if no books, wizard must wait for new book to arrive
# dont go to top of tower if witches are there
# no starvation
# magicians and witches must have a fair access to the tower


# BOOK HUNTERS:
# find new books for library.
# Team:  Susan Sto Helig, the Luggage and Cohen the Barbarian.
# not taken into account as people in tower
# Must repeat 3 times:
# 1. Go to random place of Discworld --> find 2 books.
# 2. When found two books --> go to the library --> wait until other two book hunters arrive.
# 3. When all book hunters at library --> enter together --> warn Librarian --> wait until Librarian processes the books.
# 4. They will stay at the library a random amount of time before going to find a new book.

# WITCHES:
# arrive to tower --> stay random amount of time --> leave tower
# not taken into account as people in tower
# each witch will go to the tower 3 times


# Solution:
# no startvation
# no deadlocks
# no mutual exclusion: no all magicians to tower and then all witches
# must ensure interleaving
# wizards, witches, librarian and book hunters are threads


# EXERCISE 1: ONLY CONDITIONAL VARIABLES (no semaphores or others)


# referencia de conditioning:
class Shared:
    def __init__(self):
        self.condition = th.Condition()  # define condition
        self.counter = 0

    def increment_and_wait(self):
        with self.condition:  # acquire() and release() automatically
            self.counter += 1
        while self.counter == 1:  # while its Leia’s turn, Luke waits
            self.condition.wait()  # until Luke receives notify()

    def increment(self):
        with self.condition:
            self.counter += 1

    def notifying(self):  # Leia notifes Luke
        with self.condition:
            self.condition.notify()


class Tower:
    def __init__(self, max_persons):
        self.condition = threading.Condition()
        self.wizardsInside = 0
        self.wizardsWaiting = 0
        self.witchesInside = 0
        self.witchesWaiting = 0
        self.max_persons = max_persons
        self.turn = "wizard"

    def wizardEntersTower(self, wizard_id):
        with self.condition:
            self.wizardsWaiting += 1
        # condition to enter the tower:
        while (
            self.witchesInside > 0
            or (self.wizardsInside + self.witchesInside) >= self.max_persons
            or (self.witchesWaiting > 0 and self.turn == "witch")
        ):
            self.condition.wait()

        # wizard enters the tower:
        self.wizardsWaiting -= 1
        self.wizardsInside += 1
        print(f"Wizard {wizard_id} entering the Tower. Tan Tan Tan")

    def wizardLeavesTower(self, wizard_id):
        with self.condition:
            self.wizardsInside -= 1
            print(f"Wizard {wizard_id} is leaving the Tower")

            # is the wizards is the last wizard to get out of the tower:
            if self.wizardInside == 0:
                self.turn = "witch"
                self.lock.notify_all()
            else:
                self.lock.notify_all()

    def witchEntersTower(self, witch_id):
        self.witchesInside += 1
        print(f"Witch {witch_id} is entering the tower")

        with self.Condition:
            self.witchesWaiting -= 1

        while (
            (self.wizardsInside > 0)
            or (self.wizardsInside + self.witchesInside >= self.max_persons)
            or (self.wizardsWaiting > 0 and self.turn == "wizard")
        ):
            self.condition.wait()

    def witchLeavesTower(self, witch_id):
        with self.condition:
            self.wichesInside -= 1
            self.print(f"Witch with {witch_id} is left the Tower")

        if self.witchesInside == 0:
            self.turn = "wizard"
            self.condition.notify_all()
        else:
            self.condition.notify_all()


class Elevator:
    def __init__(self):
        self.condition = threading.Condition()
        self.name = "Moist von Lipwig"
        self.wizardsInside = 0
        self.witches = 0
        self.wizardsWaitingUp = 0  # only goes up
        self.numberOfFloors = 0
        self.wizardPos = "ground"
    
    def ascendToLibrary(self):
        with self.condition:
            while not self.canUseElevator():
                print(f"[{self.name}]: Clutch fast your hats, dear travellers, for we shall ascend!")
                sleep(ELEVATOR_TRIP_TIME)
                self.wizardPos = "library"
                self.wizardsInside = 0
            if self.wizardsInside == 0:
                print(f"[{self.name}]: Now shall descend the empty vessel")
                sleep(ELEVATOR_TRIP_TIME)
            self.condition.notify_all()  # despierta a todos los threads q esten esperando a que el elevator se libere

    def canUseElevator(self):
        if self.wizardsInside == MAX_WIZARDS_ELEVATOR or self.wizardsWaitingUp == 0:
            return False
        else:
            return True


class Library:  # for actions regarding books
    def __init__(self):
        self.books = 0
        self.new_books = 0
        self.witches = 0
        self.hunters = 0
        self.name = "Librarian"
        # self.wizardPos = "library"               
                
    #si hay witches o no en library se mira en tower
    def wizardGetBook(self, wizard_id):
        with self.condition:
            while self.books == 0:
                print(f"Wizard {wizard_id} is waiting for a book")
                self.condition.wait()  # no books, waits a q hayan
                #SELF.CONDITION.WAIT() O WIZARD.CONDITION.WAIT()
            self.books -= 1
            print(f"Wizard {wizard_id} is reading a book")
            sleep(random.random())

    def huntersDeliverBooks(self, hunter_id, num_hunters):
        with self.condition:
            self.num_hunters += 1    #llega un hunter y se suma uno (luego tiene q esperar a q llegue el resto)
            print(f"Hunter {hunter_id} has arrived to the library")
            while self.num_hunters < 3:
                self.condition.wait()   #esperan los q han llegado a q lleguuen los tres
            self.condition.notify_all()     #cuando llega el tercero tiene q avisar q ha llegado para despertar a los otros hunters y q se procesen los libros    
            print("All 3 hunters have arrived to the library")
            #ahora el librarian tiene q procesar los libros nuevos
            while 0 < self.new_books and self.new_books < 2:    #hay books to process
                self.condition.wait()   #esperan a que se procesen los libros

    def processingBooks(self, new_books):
        with self.condition:
            print(f"[{self.name}] By the Beard of Archancellor, these {new_books} dreadful parchments yet await their proper docket and inscription")
            while self.new_books == 0:      #mientras no haya libros para procesar
                self.condition.wait()
            self.books += self.new_books
            print(f"[{self.name}] Behold!, these {new_books} dreadful parchments yet await their proper docket and inscription")
            self.new_books = 0  #vuelves a poner q no hayan libros nuevos para q los hunter vuelvan a irse a buscar nuevos
            self.condition.notify_all()


class Wizard(Thread):
    def __init__(self, wizard_id, tower, elevator, librarian, wizardPos):
        self.wizard_id = wizard_id
        self.tower = tower
        self.elevator = elevator
        self.library = librarian
        self.wizardPos = wizardPos

    def run(self):
        thread = threading.current_thread()
        thread.name = "Wizard"
    
class Librarian(Thread):
    def __init__(self, tower, elevator, witches, wizards):
        self.witches = witches
        self.wizards = wizards
        self.tower = tower  # may not be necessary

    def run(self):
        thread = threading.current_thread()
        thread.name = "Librarian"


class Witch(Thread):
    def __init__(self, witch_id, tower, elevator, librarian):
        self.books = 0
        self.witch_id = witch_id

    def run(self):
        thread = threading.current_thread()
        thread.name = "Witch"


class BookHunter(Thread):
    def __init__(self, hunter_id, num_hunters):
        self.hunter_id = hunter_id
        self.num_hunters = num_hunters
        self.counter = 0

    def run(self):
        thread = threading.current_thread()
        thread.name = "BookHunter"


def main():
    elevator = Elevator()
    librarian = Librarian()
    witches = Witch()
    bookHunters = BookHunter()
    wizard = Wizard()

    elevator.start()
    librarian.start()
    witches.start()
    bookHunters.start()
    wizard.start()

    elevator.join()
    librarian.join()
    witches.join()
    bookHunters.join()
    wizard.join()


if __name__ == "__main__":
    main()
