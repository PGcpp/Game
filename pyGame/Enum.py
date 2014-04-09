#Turbo wazne!!!
#trzeba BARDZO uwazac zeby kolejne klasy 'enumow' sie nie zazebialy
#czyli zeby nie bylo w nich takich samych wartosci
#np : STATE.EXIT = 1 i MENU.PLAY = 1  => to prowadzi do lipy
#moja propozycja [b brzydka] jest taka zeby kolejne klasy
#zaczynaly sie kolejnymi setkami :) - 100 enumow to sporo jak na
#jedna klase

class STATE:
    STOPPED = 1
    RUNNING = 2
    EXIT = 3
    SUSPEND = 4

class MENU:
    PLAY = 101
    OPTIONS = 102
