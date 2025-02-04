#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNRM, Université de Toulouse, Météo-France, CNRS, Toulouse, France
Version 11 décembre 2024 - Marc Mandement - marc.mandement@meteo.fr    
Script d'extraction automatique des observations horaires de la BDCLIM via l'API Météo-France
Ce script est un exemple d'extraction des observations de l'ensemble d'un département. 
En faisant des boucles et en respectant les limites du nombre de requêtes, il peut être étendu à toute la France

Prérequis : 
1) Se créer gratuitement un compte sur le portail des API : https://portail-api.meteofrance.fr
2) Aller sur la page : https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesClimatologie
3) Cliquer sur Souscrire à l'API gratuitement
4) Puis "Configurer l'API"
5) Cliquer sur "type de TOKEN" puis "API Key", durée mettre "3600" pour 1 heure par exemple
6) Remplacez dans le code ci-dessous la chaîne de caractère dénommée "cle_API" par votre clef

Pour aller plus loin, n'hésitez pas à consulter la FAQ : https://portail-api.meteofrance.fr/web/fr/faq
Notamment si vous voulez utiliser le système OAuth2 d'authentification, plus complexe pour les débutants mais permettant
d'automatiser la connexion aux serveurs de MF via la demande de jetons (tokens) notamment si vous effectuez fréquemment des requêtes 
"""
import requests, time

## A MODIFIER
cle_API="eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJtYW5kZW1lbnRtQGNhcmJvbi5zdXBlciIsImFwcGxpY2F0aW9uIjp7Im93bmVyIjoibWFuZGVtZW50bSIsInRpZXJRdW90YVR5cGUiOm51bGwsInRpZXIiOiJVbmxpbWl0ZWQiLCJuYW1lIjoiRGVmYXVsdEFwcGxpY2F0aW9uIiwiaWQiOjcxODAsInV1aWQiOiIzN2Q3YjFlOS1kYjM4LTQxODUtYWRiZS0zYzk0NzM1NDU2M2UifSwiaXNzIjoiaHR0cHM6XC9cL3BvcnRhaWwtYXBpLm1ldGVvZnJhbmNlLmZyOjQ0M1wvb2F1dGgyXC90b2tlbiIsInRpZXJJbmZvIjp7IjUwUGVyTWluIjp7InRpZXJRdW90YVR5cGUiOiJyZXF1ZXN0Q291bnQiLCJncmFwaFFMTWF4Q29tcGxleGl0eSI6MCwiZ3JhcGhRTE1heERlcHRoIjowLCJzdG9wT25RdW90YVJlYWNoIjp0cnVlLCJzcGlrZUFycmVzdExpbWl0IjowLCJzcGlrZUFycmVzdFVuaXQiOiJzZWMifX0sImtleXR5cGUiOiJQUk9EVUNUSU9OIiwic3Vic2NyaWJlZEFQSXMiOlt7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiQVJPTUUiLCJjb250ZXh0IjoiXC9wdWJsaWNcL2Fyb21lXC8xLjAiLCJwdWJsaXNoZXIiOiJhZG1pbl9tZiIsInZlcnNpb24iOiIxLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoiNTBQZXJNaW4ifSx7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiRG9ubmVlc1B1YmxpcXVlc0NsaW1hdG9sb2dpZSIsImNvbnRleHQiOiJcL3B1YmxpY1wvRFBDbGltXC92MSIsInB1Ymxpc2hlciI6ImFkbWluX21mIiwidmVyc2lvbiI6InYxIiwic3Vic2NyaXB0aW9uVGllciI6IjUwUGVyTWluIn0seyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6IkRvbm5lZXNQdWJsaXF1ZXNSYWRhciIsImNvbnRleHQiOiJcL3B1YmxpY1wvRFBSYWRhclwvdjEiLCJwdWJsaXNoZXIiOiJNRVRFTy5GUlwvbWFydGlubCIsInZlcnNpb24iOiJ2MSIsInN1YnNjcmlwdGlvblRpZXIiOiI1MFBlck1pbiJ9LHsic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJEb25uZWVzUHVibGlxdWVzT2JzZXJ2YXRpb24iLCJjb250ZXh0IjoiXC9wdWJsaWNcL0RQT2JzXC92MSIsInB1Ymxpc2hlciI6ImJhc3RpZW5nIiwidmVyc2lvbiI6InYxIiwic3Vic2NyaXB0aW9uVGllciI6IjUwUGVyTWluIn1dLCJleHAiOjE3MzM5NDA2MTQsInRva2VuX3R5cGUiOiJhcGlLZXkiLCJpYXQiOjE3MzM5MzcwMTQsImp0aSI6IjRmOWQyYjU4LTZhYWItNGZhNi04ZDY4LTEwYmY4NmY4NDdiNCJ9.DT5RwpCJ6zQg3pfhU2t367YOMjt3kazyQ11rLzajDfjCybXTG2oSb6RAuIgTQOEzXhcKbCJLAT41W3bT_zs2QTSCyELYOEVl85MhsFB62935mOshdvsAFJ4N8SG4TuOdr6pKUmNPns_owBm5iW7nnFOt_bM7f3UYUhIFebIdtEDBZbqslv9y9Y8wotvtYeF3Cx72b6gjk8YsF-U9T2Ozxf7jM4nu2srlhC921SdqC0vmYuAUMnXc3CvZPTUyO6qlLpA2BhBbsipetxClF5GeeUX7JpWZs2HkYtp5RdMczlYjEpVsLreJBiV1cUn8MVgJqJVvwz213awAJ8A-7-zHsw=="
dossier_stockage_observations="/home/mandementm/OBS/"

numero_departement = "50"
debut_periode="2024-11-01T00:00:00Z"
fin_periode="2024-11-03T00:00:00Z"

############### ETAPE 1 ###################
# On récupère la liste des stations que l'on souhaite extraire via l'API 
# Par exemple je veux connaitre les informations sur toutes les stations du département de la Manche disponibles (50)

params={'id-departement':numero_departement,
        'apikey': cle_API}
reponse = requests.get("https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/horaire", params=params)
print(reponse.json())

liste_postes = reponse.json() 
print(liste_postes)

# Liste contenant tous les identifiants
liste_identifiant_postes=[liste_postes[i]['id'] for i in range(len(liste_postes))]

############### ETAPE 2 ###################
# Le mécanisme est d'envoyer une commande au serveur Météo-France, qui répond avec un numéro de commande
# A l'aide de ce numéro de commande on récupère un fichier csv juste après
# On réaliser une boucle sur l'ensemble des postes du département obtenus à l'étape 1

for id_station in liste_identifiant_postes:
    print("Téléchargement des données de la station numéro ",id_station)
    params={'id-station':id_station,
            'date-deb-periode': debut_periode,
            'date-fin-periode': fin_periode,
            'apikey': cle_API}    
    reponse = requests.get("https://public-api.meteofrance.fr/public/DPClim/v1/commande-station/horaire", params=params)
    numero_commande = reponse.json()['elaboreProduitAvecDemandeResponse']['return']
    print(reponse.json())
    # On attend 2 secondes que la réponse soit traitée
    # Et cela permet de respecter le nombre maximum de requêtes qui est de 50 par minute par exemple sur l'API climatologique.
    time.sleep(2)
    params={'id-cmde': numero_commande,
            'apikey': cle_API}    
    reponse = requests.get("https://public-api.meteofrance.fr/public/DPClim/v1/commande/fichier", params=params)
    
    with open(dossier_stockage_observations+'ObsMF_'+id_station+'_'+debut_periode+'_'+fin_periode+'.csv','w',encoding="utf-8") as f:
        f.write(reponse.text)
