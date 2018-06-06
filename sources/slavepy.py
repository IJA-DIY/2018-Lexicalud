# -*- coding: utf-8 -*-
#
#Parce que le programme principal mainpy.py est le plus complexe et que (presque) tous les éléments du programme slavepy.py
#sont issus de ce dernier, le programme slavepy.py n'est que peu commenté. Toute information d'une commande non expliqué ici
#devrait en théorie être expliquée dans le programme mainpy.py.
#

from random import *
import os
import serial
import time

#Connexion Serial. IDENTIQUE AU RASPBERRY MAÎTRE. (sauf timeout)
ser = serial.Serial("/dev/ttyS0", timeout=180)


lettres_interdites = []
mots_interdits = []

prononciation = {'a':'a', 'b':'b', 'c':'c','d':'d','e':'eux','f':'f','g':'g','h':'hache','i':'i','j':'j','k':'ca','l':'elle','m':'aime','n':'haine','o':'eau',
'p':'p','q':'ku','r':'aire','s':'est-ce','t':'thé','u':'eu','v':'v','w':'double\ v','x':'x','y':'igrek','z':'zaide','\xc3':' ','\xa9':'euh\ accent\ aigu',
'\xa8':'euh\ accent\ grave','\xaa':'euh\ accent\ circonflexe','\xab':'eux\ trémas','\xa2':'a\ accent\ circonflexe','\xaf':'i\ tréma',
'\xae':'i\ accent\ circonflexe','\xb4':'eau\ accent\ circonflexe','\xb9':'eu\ accent\ grave','\xa7':'c\ sédille','\xbb':'eu\ accent\ circonflexe'}

def parler(text):
	os.system("./dit.sh "+text)


ser.write('\n')
parler("En\ attente\ de\ J1.")
y = ser.readline()
print('done')




dictionnaire=[]
with open('liste.de.mots.francais.latin1.txt') as dicoco:
   dictionnaire.append(dicoco.readlines())
dictionnaire=dictionnaire[0]


def getch():
	import sys, tty, termios
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


	

####################################
def eteindre(): #DO NOT USE -Arrêt #
	os.system("sudo shutdown now") #
####################################



def selection(dico): 						
	mot = dico[int(random()*len(dico))].decode("latin1")
	if len(lettres_interdites)>6:
		del lettres_interdites[0]
	
	while (mot[0] in lettres_interdites) or (mot in mots_interdits):
		mot = dico[int(random()*(len(dico)-1))].decode("latin1")
	mot = mot[:len(mot)-1]
	return mot

def precision():
	parler("J1\ est\ en\ train\ de\ choisir\ le\ nombre\ de\ parties.\ Patientez.")
	#selection du nombre de parties par j1
	n = ser.readline()
	n = len(n)-1
	j1 = 0
	j2 = 0
	print(n)
	print("debut de la partie pour",n,"parties")
	parler("Vous\ jouez\ pour")
	parler(str(n))
	parler("parties.")
	parler("C'est\ parti!")
	for i in range(int(n)):
		#en attente de l'envoi du mot par j1
		mot = ser.readline()
		mot = mot[:len(mot)-1]
		print(mot)
		parler(mot)
		#baffle parler(mot)
		happy = False
		while not happy:
			reponse2 = raw_input()
			parler("Vous\ avez\ écrit")
			for i in reponse2:
				parler(prononciation[i])
			parler("Ce\ mot\ vous\ convient-il?")
			satisfaction = 'oui'
			slcct = 1
			while slcct != 13:
				if satisfaction == 'oui':
					parler("oui")
					while slcct != 27 and slcct !=13:
						slcct = ord(getch())
					if slcct == 27:
						slcct = getch()
						slcct = ord(getch())
						satisfaction = 'non'
				elif satisfaction == 'non':
					parler("non")
					while slcct != 27 and slcct !=13:
						slcct = ord(getch())
					if slcct == 27:
						slcct = getch()
						slcct = ord(getch())
						satisfaction = 'oui'
			if satisfaction == 'oui':
				parler("Réponse\ enregistrée.")
				happy = True
			else:
				parler("Retapez\ votre\ mot")
		ser.write(reponse2+"\n")
		z = ser.readline()
		if z:
			j1 = j1 + len(z) - 1
		if len(z) == 2:
			parler("+1\ pour\ J1")
			print("+1")
		else:
			parler("+0\ pour\ J1")
			print("+0")
		z = ser.readline()
		if z:
			j2 = j2 + len(z) - 1
		if len(z) == 2:
			parler("+1\ pour\ J2")
			print("+1")
		else:
			parler("+0\ pour\ J2")
			print("+0")
	
	
	parler("j1\ finit\ avec")
	parler(str(j1))
	parler("points,\ et\ j2\ finit\ avec")
	parler(str(j2))
	parler("points.")
	parler("retour\ au\ menu")
	parler("reprise\ de\ la\ main\ par\ J1")


def mode2(): #second mode de jeu
	print("le mode mode2 a été lancé\n")



def mode3(): #troisième mode de jeu
	print("le mode mode3 a été lancé\n")



def mode4(): #quatrième mode de jeu
	print("le mode mode4 a été lancé\n")




life = 1
if not y:
	life = 0
while life:
	assert 0 < life < 5, "erreur life"
	slv = ser.readline()
	if slv == 'one\n': precision()
	elif slv == 'two\n': mode2()
	elif slv == 'three\n': mode3()
	elif slv == 'four\n': mode4()
	elif slv == 'stop\n': life = 0
	else: print("En attente")
			
parler("Arrêt\ en\ cours")		
print("Arrêt")		
#eteindre()			
			
