# -*- coding: utf-8 -*-

# la ligne ci-dessous est de-commentée si on se sert de python3 (il faut alors mettre la suivante en commentaire)
# import urllib.request as urllib2
import urllib2
import csv
from bs4 import BeautifulSoup
import requests
from time import sleep

# scraper écrit en mars 2014 pour extraction d'autres données relatives aux fondations publiques québécoises sur le site de l'Agence du revenu du Canada

# définition des trois parties fixes de l'URL qu'on va harnacher

url1 = "http://www.cra-arc.gc.ca/ebci/haip/srch/t3010form"
url2 = "sched6-fra.action?b="
url3 = "&fpe="

# création d'une liste des numéros d'enregistrement, des dates de dépôt des états financiers correspondants et de leurs sources à partir d'un fichier csv préalablement constitué par le scraper fondations.py

numero = []
etats =[]
source = []

with open("Fondations-2.csv", "rb") as enregistrements:
	numeros = csv.reader(enregistrements, delimiter=";")
	for row in numeros:
		numero.append(row[1])
		etats.append(row[3])
		source.append(row[4])

a = 0 # compteur pour diagnostiquer les bogues
e = 0 # compteur pour les états financiers et leur source

# le robot commence ici

autresLignes = []

for n in numero:
	d = etats[e]
	print ("")
	print ("Fondation num %i") % (e+1)
	print ("Les états financiers de %s ont été déposés le %s (source: %s)") % (numero[e], etats[e], source[e])
	e +=1

	for i in range (22,24): # deux cas doivent être testés car les URLs comportent parfois un 22, parfois un 23
		if etats[e-1] == "Aucune":
			break
		if source[e-1] == "Section D":
			break

		url = "%s%s%s%s%s%s" % (url1,i,url2,n,url3,d)
		a +=1
		print (url)

		r = requests.get(url)
		data = r.text

		soup = BeautifulSoup(data)

		if soup.find("em", text="Renseignements financiers détaillés"):

			print ("cas %s: vide pour %s" % (i,n)) # affichage dans la console pour suivre la progression de l'extraction
			sleep(1) # temps d'arret d'une seconde pour laisser le serveur de l'ARC souffler un brin

		else:

			ligne4500 = soup.find("div", class_="linenumber1", text="4500")
			print (ligne4500)
			revenu4500 = ligne4500.findNext("div").text
			revenu4500 = revenu4500.encode('utf-8')
			print ("cas %s: revenus de %s pour %s à ligne 4500" % (i, revenu4500, n)) # affichage dans la console pour suivre la progression de l'extraction

			ligne4510 = soup.find("div", class_="linenumber1", text="4510")
			print (ligne4510)
			revenu4510 = ligne4510.findNext("div").text
			revenu4510 = revenu4510.encode('utf-8')
			print ("cas %s: revenus de %s pour %s à ligne 4510" % (i, revenu4510, n)) # affichage dans la console pour suivre la progression de l'extraction

			ligne4530 = soup.find("div", class_="linenumber1", text="4530")
			print (ligne4530)
			revenu4530 = ligne4530.findNext("div").text
			revenu4530 = revenu4530.encode('utf-8')
			print ("cas %s: revenus de %s pour %s à ligne 4530" % (i, revenu4530, n)) # affichage dans la console pour suivre la progression de l'extraction

			ligne4575 = soup.find("div", class_="linenumber1", text="4575")
			print (ligne4575)
			revenu4575 = ligne4575.findNext("div").text
			revenu4575 = revenu4575.encode('utf-8')
			print ("cas %s: revenus de %s pour %s à ligne 4575" % (i, revenu4575, n)) # affichage dans la console pour suivre la progression de l'extraction

			ligne4630 = soup.find("div", class_="linenumber1", text="4630")
			print (ligne4630)
			revenu4630 = ligne4630.findNext("div").text
			revenu4630 = revenu4630.encode('utf-8')
			print ("cas %s: revenus de %s pour %s à ligne 4630" % (i, revenu4630, n)) # affichage dans la console pour suivre la progression de l'extraction

			ligne4950 = soup.find("div", class_="linenumber1", text="4950")
			print (ligne4950)
			depense4950 = ligne4950.findNext("div").text
			depense4950 = depense4950.encode('utf-8')
			print ("cas %s: dépenses de %s pour %s à ligne 4950" % (i, depense4950, n)) # affichage dans la console pour suivre la progression de l'extraction
			print ("")

	autresLignes.append([n,d,revenu4500,revenu4510,revenu4530,revenu4575,revenu4630,depense4950])

	print (autresLignes) # affichage de la liste dans la console à chaque passage aux fins de vérification

sleep(1) # temps d'arret d'une seconde pour laisser le serveur de l'ARC souffler un brin

# écriture des resultats dans un fichier csv

final =  open("RevenusDepensesFondations.csv", "w")

for row in autresLignes:
	for column in row:
		final.write("%s;" % column)
	final.write("\n")

final.close()
