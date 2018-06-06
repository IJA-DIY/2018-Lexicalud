# -*- coding: utf-8 -*-
#
#Voici le code principale du projet 'Lexicalud'. La programme dans sa totalité est principalement écrit
#sur deux programme : ce programme (mainpy.py) et le programme du raspberry esclave (slavepy.py). Afin
#d'éviter toute redondance, seulement ce programme est commenté dans sont intégralité. Une majeure partie
#des variables, fonctions, et processus du programme slavepy.py sont (très) similaires à celle du programme
#principal.
#
#
#
######################################################################################################
from random import *	#Module utilisé pour tirer un mot aléatoire
import os				#Module utilisé pour entrer des commandes dans le terminal
import serial			#Module de connexion inter-raspberry's
import time				#Module utilisé pour effectuer des pauses afin de synchroniser les raspberry's
######################################################################################################

#Mise en place de la connexion Sérial entre les deux raspberry : ttyS0 défini le port et baudrate la fréquence. Les deux raspberry's doivent avoir les même.
ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=300)


#Définition des éléments 'mémoire' pour les mots. Réinitialisables possible dans le menu plus bas
lettres_interdites = []
mots_interdits = []


#Ce dictionnaire a pour but d'aider le synthétiseur vocal à prononcer les lettres individuellement.
prononciation = {'a':'a', 'b':'b', 'c':'c','d':'d','e':'eux','f':'f','g':'g','h':'hache','i':'i','j':'j','k':'ca','l':'elle','m':'aime','n':'haine','o':'eau',
'p':'p','q':'ku','r':'aire','s':'est-ce','t':'thé','u':'eu','v':'v','w':'double\ v','x':'x','y':'igrek','z':'zaide','\xc3':' ','\xa9':'euh\ accent\ aigu',
'\xa8':'euh\ accent\ grave','\xaa':'euh\ accent\ circonflexe','\xab':'eux\ trémas','\xa2':'a\ accent\ circonflexe','\xaf':'i\ tréma',
'\xae':'i\ accent\ circonflexe','\xb4':'eau\ accent\ circonflexe','\xb9':'eu\ accent\ grave','\xa7':'c\ sédille','\xbb':'eu\ accent\ circonflexe'}


mini = 1	#Variable 'limites' utilisés dans le menu
maxi = 4	#pour éviter les 'débordements'


###################################################################################
def parler(text): 					#Fonction de synthèse vocal 'TTS' avec PicoTTS
	os.system("./dit.sh "+text)		#Cette fonction fait appel à un script afin de
#d'abord créer un fichier wav, le lire, puis le supprimer afin d'éviter de créer et
#de conserver des données inutilements.
###################################################################################


#################################################################################################################
#Fonction permettant la reconnaissance des clés entrées au clavier. Pour se faire, il est nécessaire d'importer
def getch(): 													#les modules sys, tty et termios qui sont des 
	import sys, tty, termios									#modules propres à Linux et qui permettent ici
	fd = sys.stdin.fileno()										#de désactiver la nécessité d'appuyer sur entrée
	old_settings = termios.tcgetattr(fd)						#pour valider une saisie. Parce qu'il n'y a plus
	try:														#de moyen pour valider, la fonction demande à ne
		tty.setraw(sys.stdin.fileno())							#lire qu'un seul charactère dans le stdin. Cette
		ch = sys.stdin.read(1)									#fonction est ainsi capable de lire toutes les 
	finally:													#clés du clavier et renvoi une valeur utilisable.
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)	#Les réglages du stdin sont par la suite
	return ch													#réinitialisé aux réglages d'avant la fonction
#afin de réactiver la validation de la saisie par la touche entrée, nécessaire dans la suite du programme.
#################################################################################################################



parler("Souhaitez-vous\ jouer\ avec\ un\ second\ joueur?")
duo = True
repp = 'oui'
slcct = 1
while slcct != 13:
	if repp == 'oui':
		parler("oui")
		while slcct != 27 and slcct !=13:
			slcct = ord(getch())
		if slcct == 27:
			slcct = getch()
			slcct = ord(getch())
			repp = 'non'
			duo = False
	elif repp == 'non':
		parler("non")
		while slcct != 27 and slcct !=13:
			slcct = ord(getch())
		if slcct == 27:
			slcct = getch()
			slcct = ord(getch())
			repp = 'oui'
			duo = True




if duo:
	print('waitin j2')
	parler("En\ attente\ de\ j2")
	x = ser.readline()
	time.sleep(3)
	ser.write('p\n')

	
parler("Vous\ êtes\ dans\ le\ menu")


#############################################################################################################
#Création du dictionnaire à l'aide du fichier externe présent dans le même fichier que ce code. Le fichier
dictionnaire=[]												#est ici converti en tant que liste de string
with open('liste.de.mots.francais.latin1.txt') as dicoco:	#tous terminé par un "\n".
   dictionnaire.append(dicoco.readlines())					#
dictionnaire=dictionnaire[0]								#Cette ligne est nécessaire pour simplifier le
#code par la suite. En effet la création de la liste engendre une liste contenant elle même une (et seulement
#une) la liste contenant les mots. En quelque sorte ici nous 'enlevons un étage de crochets'.
#############################################################################################################


	

#####################################################################################
def eteindre(): #DO NOT USE -Arrêt ## Fonction permettant l'arrêt total du raspberry.
	os.system("sudo shutdown now") ## À utiliser avec précaution...
#####################################################################################



#################################################################################################
#Fonction permettant de selectionner un mot dans le dictionnaire tout en évitant les répétitions.
def selection(dico): 													#Ce programme fait appel
	mot = dico[int(random()*len(dico))].decode("latin1")				#à la liste dictionnaire
	if len(lettres_interdites)>6:										#définie plus haut.
		del lettres_interdites[0]										#On évite également les
																		#répétitions à l'aide des
	while (mot[0] in lettres_interdites) or (mot in mots_interdits):	#variables définies plus
		mot = dico[int(random()*(len(dico)-1))].decode("latin1")		#haut.
	mot = mot[:len(mot)-1]												#
	return mot															#
#################################################################################################


def precision():		#Premier mode de jeu.
	parler("Combien\ de\ parties\ souhaitez-vous\ jouer?")
	slct = 1
	nombre_parties = 2
	while slct != 13:	#Pseudo menu servant à la selection du nombre de parties.
		if nombre_parties == 2:
			parler("2")
			while slct != 27 and slct !=13:
				slct = ord(getch())
			if slct == 27:
				slct = getch()
				slct = ord(getch())
				if slct == 66 or slct == 67:
					nombre_parties = 5
				else:
					nombre_parties = 20
		elif nombre_parties == 5:
			parler("5")
			while slct != 27 and slct !=13:
				slct = ord(getch())
			if slct == 27:
				slct = getch()
				slct = ord(getch())
				if slct == 66 or slct == 67:
					nombre_parties = 10
				else:
					nombre_parties = 2
		elif nombre_parties == 10:
			parler("10")
			while slct != 27 and slct !=13:
				slct = ord(getch())
			if slct == 27:
				slct = getch()
				slct = ord(getch())
				if slct == 66 or slct == 67:
					nombre_parties = 15
				else:
					nombre_parties = 5
		elif nombre_parties == 15:
			parler("15")
			while slct != 27 and slct !=13:
				slct = ord(getch())
			if slct == 27:
				slct = getch()
				slct = ord(getch())
				if slct == 66 or slct == 67:
					nombre_parties = 20
				else:
					nombre_parties = 10
		elif nombre_parties == 20:
			parler("20")
			while slct != 27 and slct !=13:
				slct = ord(getch())
			if slct == 27:
				slct = getch()
				slct = ord(getch())
				if slct == 66 or slct == 67:
					nombre_parties = 2
				else:
					nombre_parties = 15
	
	j1 = 0							#Initialisation des points de J1
	j2 = 0							#Initialisation des points de J2
	if duo:
		ser.write(nombre_parties)		#Transmission du nombre de parties au second raspberry.
		ser.write('\n')
	parler("Vous\ jouez\ pour")
	parler(str(nombre_parties))
	parler("parties.")
	parler("C'est\ parti\ !")
	for i in range(nombre_parties):
		mot = selection(dictionnaire)	#Selection d'un mot.
		if duo:
			ser.write(mot.encode('utf-8')+"\n")	#Transmission du mot sélectioné au second raspberry.
		parler(mot.encode('utf-8'))  #à mettre sur le haut parleur / HDMI / Bluetooth
		happy = False
		while not happy:				#Boucle permettant à l'utilisateur de vérifier et valider sa réponse.
			reponse1 = raw_input()
			parler("Vous\ avez\ écrit")
			for lettre in reponse1:
				parler(prononciation[lettre])
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
		if duo:
			reponse2 = ser.readline()	#En attente de la réponse du second raspberry.
			reponse2 = reponse2[:len(reponse2)-1]
			if reponse1 == mot.encode('utf-8'):
				j1+=1
				ser.write('a\n')			#Ici il s'agit en quelque sorte d'une communication binaire.
											#Soit la raspberry maître envoie une chaîne de 2 charactères
				parler("+1\ pour\ J1!")		#signifiant que la réponse est correcte, soit une chaîne de 
			else:							#1 charactère signifiant que la réponse est fausse. Une chaîne
				ser.write('\n')				#de taille 0 n'est pas utilisée pour éviter toute erreur.
											#Le second raspberry traîte lui-même cette information.
				parler("+0\ pour\ J1")
			if reponse2 == mot.encode('utf-8'):
				j2+=1
				ser.write('a\n')
				parler("+1\ pour\ J2!")
			else:
				ser.write('\n')
				parler("+0\ pour\ J2")
		else:
			if reponse1 == mot.encode('utf-8'):
				parler("Vous\ gagnez\ un\ point")
				j1+=1
			else:
				parler("Vous\ ne\ gagnez\ pas\ de\ point")
		lettres_interdites.append(mot[0])	#Ajout du mot et de la lettre aux listes mémoire.
		mots_interdits.append(mot+"\n")
	if duo:
		parler("j1\ finit\ avec")
		parler(str(j1))
		parler("points,\ et\ j2\ finit\ avec")
		parler(str(j2))
		parler("points.")
	else:
		parler("Vous\ finissez\ avec")
		parler(str(j1))
		parler("points.")
	parler("retour\ au\ menu.")



def mode2(): #second mode de jeu
	print("le mode mode2 a été lancé\n")



def mode3(): #troisième mode de jeu
	print("le mode mode3 a été lancé\n")



def mode4(): #quatrième mode de jeu
	print("le mode mode4 a été lancé\n")




life = 1 #Variable de 'vie' de la mainloop.


while life:	#Menu Principal.
	assert 0 < life < 5, "erreur life"  #Assert... au cas où.
	if life == 1:
		parler("jouer\ le\ mode\ précision?")
		lanceur = 0
		while lanceur != 13 and lanceur != 27 and lanceur != 114:  # 13 = ENTER /  27 = ARROWS or ESC  / 114 = 'r' KEY
			lanceur = ord(getch())
		
		if lanceur == 13:
			print("début de précision")
			
			ser.write('one\n')
			time.sleep(1)
			precision()
		
		elif lanceur == 27:
			lanceur = ord(getch())
			if lanceur == 27: #Double ESC
				print("début de l'arrêt")
				ser.write('stop\n')
				life = 0
			else: #Automatiquement sélectionné si une clé est entrée.
				lanceur = ord(getch())
				if lanceur == 66 or lanceur == 67: #Flèches Bas/Droite.
					print("incrémentation de life de 1\n")
					life+=1
			
				elif lanceur == 65 or lanceur == 68: #Flèches Haut/Gauche.
					print("passage de life à max\n")
					life = maxi
		elif lanceur == 114: #Lettre 'r'. Réinitialise les listes. Assez peu utile en soi.
			parler("Réinitialisation\ des\ listes.")
			lettres_interdites = []
			mots_interdits = []
		
		else:
			print("commande introuvable")
	
	elif life == 2:
		print("jouer le mode mode2 ?")
		parler("jouer\ le\ mode\ mode2?")
		lanceur = 0
		while lanceur != 13 and lanceur != 27 and lanceur != 114:
			lanceur = ord(getch())
		
		if lanceur == 13:
			print("début de mode2")
			ser.write('two\n')
			time.sleep(1)
			mode2()
			
		elif lanceur == 27:
			lanceur = ord(getch())
			if lanceur == 27:
				print("début de l'arrêt")
				ser.write('stop\n')
				life = 0
			else:
				lanceur = ord(getch())
				if lanceur == 66 or lanceur == 67:
					print("incrémentation de life de 1\n")
					life+=1
			
				elif lanceur == 65 or lanceur == 68:
					print("décrémentation de life de 1\n")
					life-=1
		
		elif lanceur == 114:
			parler("Réinitialisation\ des\ listes.")
			lettres_interdites = []
			mots_interdits = []
			
		else:
			print("commande introuvable")
	
	elif life == 3:
		print("jouer le mode mode3 ?")
		parler("jouer\ le\ mode\ mode3?")
		lanceur = 0
		while lanceur != 13 and lanceur != 27 and lanceur != 114:
			lanceur = ord(getch())
		
		if lanceur == 13:
			print("début de mode3")
			ser.write('three\n')
			time.sleep(1)
			mode3()
			
		elif lanceur == 27:
			lanceur = ord(getch())
			if lanceur == 27:
				print("début de l'arrêt")
				ser.write('stop\n')
				life = 0
			else:
				lanceur = ord(getch())
				if lanceur == 66 or lanceur == 67:
					print("incrémentation de life de 1\n")
					life+=1
			
				elif lanceur == 65 or lanceur == 68:
					print("décrémentation de life de 1\n")
					life-=1
		
		elif lanceur == 114:
			parler("Réinitialisation\ des\ listes.")
			lettres_interdites = []
			mots_interdits = []
		
		else:
			print("commande introuvable")

	elif life == 4:
		print("jouer le mode mode4 ?")
		parler("jouer\ le\ mode\ mode4?")
		lanceur = 0
		while lanceur != 13 and lanceur != 27 and lanceur != 114:
			lanceur = ord(getch())
		
		if lanceur == 13:
			print("début de mode4")
			ser.write('four\n')
			time.sleep(1)
			mode4()
			
		elif lanceur == 27:
			lanceur = ord(getch())
			if lanceur == 27:
				print("début de l'arrêt")
				ser.write('stop\n')
				life = 0
			else:
				lanceur = ord(getch())
				if lanceur == 66 or lanceur == 67:
					print("passage de life à mini\n")
					life = mini
			
				elif lanceur == 65 or lanceur == 68:
					print("décrémentation de life de 1\n")
					life-=1
		
		elif lanceur == 114:
			parler("Réinitialisation\ des\ listes.")
			lettres_interdites = []
			mots_interdits = []
		
		else:
			print("commande introuvable")
	
	else: print("Something is wrong")
			
parler("Arrêt\ en\ cours")		
print("Arrêt")
#eteindre()
			
