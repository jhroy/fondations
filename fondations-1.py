# -*- coding: utf-8 -*-

# Jean-Hugues Roy GPL v2

# la ligne ci-dessous est de-commentée si on se sert de python3 (il faut alors mettre la suivante en commentaire)
# import urllib.request as urllib2
import urllib2
import csv
from bs4 import BeautifulSoup
import requests
from time import sleep

# scraper écrit en mars 2014 pour extraction des actifs de fondations sur le site de l'Agence du revenu du Canada

# définition des trois parties fixes de l'URL qu'on va harnacher

url1 = "http://www.cra-arc.gc.ca/ebci/haip/srch/t3010form"
url2 = "sched6-fra.action?b="
url3 = "&fpe="

# création d'une liste de toutes les dates de dépôt des états financiers, car plusieurs cas sont possibles

etats =[]

for annee in range(2012,2014):

	for mois in range(1,13):

		if mois < 10: # ajout d'un zéro devant les 9 premiers mois
			mois = "%02d" % (mois,)

			if mois == "01":
				date = "%s-%s-31" % (annee,mois)
				etats.append(date)

			elif mois == "02": # changer la date de fin de février dans le cas de 2012, année bisextile 
				if annee == 2012:
					date = "%s-%s-29" % (annee,mois)
				else:
					date = "%s-%s-28" % (annee,mois)
				etats.append(date)

			elif mois == "03":
				date = "%s-%s-31" % (annee,mois)
				etats.append(date)

			elif mois == "04":
				date = "%s-%s-30" % (annee,mois)
				etats.append(date)

			elif mois == "05":
				date = "%s-%s-31" % (annee,mois)
				etats.append(date)

			elif mois == "06":
				date = "%s-%s-30" % (annee,mois)
				etats.append(date)

			elif mois == "07":
				date = "%s-%s-31" % (annee,mois)
				etats.append(date)
			elif mois == "08":
				date = "%s-%s-31" % (annee,mois)
				etats.append(date)
			elif mois == "09":
				date = "%s-%s-30" % (annee,mois)
				etats.append(date)

		if mois == 10:
			date = "%s-%s-31" % (annee,mois)
			etats.append(date)
		elif mois == 11:
			date = "%s-%s-30" % (annee,mois)
			etats.append(date)
		elif mois == 12:
			date = "%s-%s-31" % (annee,mois)
			etats.append(date)

'''

# on pourrait aussi procéder ainsi; moins élégant, mais plus adaptable dans le temps

etats = [
"2012-01-31",
"2012-02-29",
"2012-03-31",
"2012-04-30",
"2012-05-31",
"2012-06-30",
"2012-07-31",
"2012-08-31",
"2012-09-30",
"2012-10-31",
"2012-11-30",
"2012-12-31",
"2013-01-31",
"2013-02-28",
"2013-03-31",
"2013-04-30",
"2013-05-31",
"2013-06-30",
"2013-07-31",
"2013-08-31",
"2013-09-30",
"2013-10-31",
"2013-11-30",
"2013-12-31",
]

for date in etats:
	etats.append(date)

'''

# création d'une liste des numéros d'enregistrement à partir d'un fichier csv préalablement constitué par une autre extraction

numero = []

with open("Fondations.csv", "r") as enregistrements:
	numeros = csv.reader(enregistrements, delimiter=";")
	for row in numeros:
		numero.append(row[1])

a = 0 # compteur pour suivre la progression de l'extraction dans la console

# le robot commence ici
# il est programmé pour effectuer 54624 requêtes; à une seconde chacune, l'ensemble de l'opération prend 15 heures; il est donc recommandé de la briser en plusieurs « passes »

actifs = []

for n in numero:

	for d in etats:

		for i in range (22,24): # deux cas doivent être testés car les URLs comportent parfois un 22, parfois un 23

			url = "%s%s%s%s%s%s" % (url1,i,url2,n,url3,d)
			a = a+1
			print (a)
			print (url)

			r = requests.get(url)
			data = r.text

			soup = BeautifulSoup(data)

# quand la page est vide, elle contient toujours les mots « Renseignements financiers détaillés » en italique

			if soup.find("em", text="Renseignements financiers détaillés"):

				print ("numéro %s pour cette date (%s) est vide" % (n,d)) # affichage dans la console pour suivre la progression de l'extraction
				print ("")
				sleep(1) # temps d'arret d'une seconde pour laisser le serveur de l'ARC souffler un brin

# s'il y a des états financiers, on cherche un div contenant «4200» (le numéro de ligne des actifs) et on extrait le contenu du div suivant, qui contient le montant des actifs

			else:

				ligne = soup.find("div", class_="linenumber1", text="4200")

# exclusion de certaines fondations dont la ligne des états financiers est vide				
				
				if n == "101835536RR0001":
					actif = "0 $"
				else:
					actif = ligne.findNext("div").contents[0]

				print (actif)
				print ("la fondation %s a declare %s d'actifs le %s" % (n, actif, d)) # affichage dans la console pour suivre la progression de l'extraction
				print ("")
				
				actif = actif.encode('utf-8')

				actifs.append([n,d,actif])

				print(actifs) # affichage de la liste dans la console à chaque fois qu'on trouve un actif aux fins de vérification

				sleep(1) # temps d'arret d'une seconde pour laisser le serveur de l'ARC souffler un brin

# écriture des resultats dans un fichier csv

final =  open("actifs.csv", "w")

for row in actifs:
	for column in row:
		final.write("%s;" % column)
	final.write("\n")

final.close()
