#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programme qui se connecte à une API et renvoit les données concernant un produit de bourse particulier.
Ne semble malheureusement pas disponible pour les actions européennes.

To claim your free API key with lifetime access, visit this page :
    https://www.alphavantage.co/support

"""

import pprint
import json
import os
import requests
from dotenv import load_dotenv

# fonction qui récupère les variables d'environnement dans le fichier .env
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'

# le produit financier dont on veut récupérer les données
stock = 'IBM'

# on crée un dictionnaire au format texte avec la réponse à une requête reçue en json
response = requests.get(API_url.format(stock, API_KEY))
response = json.loads(response.text)

# on crée des listes à partir des clés et des valeurs du dictionnaire
key_list = list(response['Time Series (Daily)'].keys())
value_list = [list(element.values()) for element in list(response['Time Series (Daily)'].values())]

# on réorganise la liste [open, high, low, close, volume] pour avoir [close, open, high, low]
for element in value_list:
    element.insert(0, element[-2])
    del element[-2], element[-1]

# on recrée la structure du dictionnaire mais sous forme d'une liste de tuples
data_list = list(zip(key_list, value_list))

# on transforme la liste de tuples en liste de listes
data_list = [list(element) for element in data_list]

# enfin on fait disparaître la sous-liste de chaque élément pour ne garder que des listes composées de strings formatées
result = []
for element in data_list:
    flat_list = [element[0]]
    for each_element in element[1]:
        flat_list.append(str(float(each_element)))  # on formate les nombres à 2 décimales
    result.append(flat_list)

# on slice la liste pour afficher les 10 premiers résultats (sous la forme [date, close, open, high, low])
sample = result[:10]

# on affiche la liste avec pprint.pprint, ce qui permet d'avoir un seul élément par ligne
pprint.pprint(sample)

# url qui renvoit le RSI 14 jours. A compléter par symbol=ACTION (ne pas oublier l'API_KEY)
# https://www.alphavantage.co/query?function=RSI&symbol={}&interval=daily&time_period=14&series_type=close&apikey={}
