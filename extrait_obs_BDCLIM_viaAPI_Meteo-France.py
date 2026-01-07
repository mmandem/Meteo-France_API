#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Météo-France, CNRS, Univ. Toulouse, CNRM, Toulouse, France
11 décembre 2024 - Marc Mandement - marc.mandement@meteo.fr    
MAJ 7 janvier 2026
Script d'extraction automatique des observations horaires de la BDCLIM via l'API Météo-France
Ce script est un exemple d'extraction des observations de l'ensemble d'un département. 
En faisant des boucles et en respectant les limites du nombre de requêtes, il peut être étendu à toute la France

Prérequis : 
1) Se créer gratuitement un compte sur le portail des API : https://portail-api.meteofrance.fr
2) Aller sur la page : https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesClimatologie
3) Cliquer sur Souscrire à l'API gratuitement
4) Puis "Configurer l'API"
5) Cliquez sur "type de TOKEN" puis "API Key" pour la méthode 1, durée mettre "3600" pour 1 heure par exemple
6) Remplacez dans le code ci-dessous la chaîne de caractère dénommée "cle_API" par votre clef

N'hésitez pas à consulter la FAQ : https://portail-api.meteofrance.fr/web/fr/faq
"""
import requests
import time

dossier_stockage_observations = "/cnrm/precip/users/mandement/OBS/"
methodes_authentification = ["API_Key","Oauth2"]
methode_choisie           = methodes_authentification[1]

if methode_choisie=="API_Key":
    # Attention à bien copier la clef API, elle est parfois très longue (plus de 2000 caractères !!)
    cle_API =  "VOTRE_CLEF"
elif methode_choisie=="Oauth2":
    # Permet d'automatiser la connexion aux serveurs de MF via la demande de jetons (tokens) si vous effectuez fréquemment des requêtes
    # La demande d'un nouveau jeton efface le précédent
    APPLICATION_ID = "VOTRE_APPLICATION_ID"
    data = {'grant_type': 'client_credentials'}
    headers = {'Authorization': 'Basic ' + APPLICATION_ID}
    reponse = requests.post("https://portail-api.meteofrance.fr/token",data=data, headers=headers)
    token_API=reponse.json()["access_token"]

numero_departement = "50"
debut_periode="2024-11-01T00:00:00Z"
fin_periode="2024-11-03T00:00:00Z"

############### ETAPE 1 ###################
# On récupère la liste des stations que l'on souhaite extraire via l'API 
# Par exemple je veux connaitre les informations sur toutes les stations du département de la Manche disponibles (50)    

params={'id-departement':numero_departement}
if methode_choisie=="API_Key": params.update({'apikey': cle_API})
elif methode_choisie=="Oauth2":  params.update({'tokenOauth2': token_API})
    
reponse = requests.get("https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/horaire", params=params)
print(reponse.json())

liste_postes = reponse.json() 
print(liste_postes)

# Liste contenant tous les identifiants
liste_identifiant_postes=[liste_postes[i]['id'] for i in range(len(liste_postes))]

############### ETAPE 2 ###################
# Le mécanisme est d'envoyer une commande au serveur Météo-France, qui répond avec un numéro de commande
# A l'aide de ce numéro de commande on récupère un fichier csv juste après
# On peut réaliser une boucle sur l'ensemble des postes du département obtenus à l'étape 1

for id_station in liste_identifiant_postes:
    print("Téléchargement des données de la station numéro ",id_station)
    params={'id-station':id_station,
            'date-deb-periode': debut_periode,
            'date-fin-periode': fin_periode}  
    if methode_choisie=="API_Key": params.update({'apikey': cle_API})
    elif methode_choisie=="Oauth2":  params.update({'tokenOauth2': token_API})
    reponse = requests.get("https://public-api.meteofrance.fr/public/DPClim/v1/commande-station/horaire", params=params)
    numero_commande = reponse.json()['elaboreProduitAvecDemandeResponse']['return']
    print(reponse.json())
    # On attend 1,5 secondes que la réponse soit traitée
    # Et cela permet de respecter le nombre maximum de requêtes qui est de 50 par minute par exemple sur l'API climatologique.
    time.sleep(1.5)
    params={'id-cmde': numero_commande}    
    if methode_choisie=="API_Key": params.update({'apikey': cle_API})
    elif methode_choisie=="Oauth2":  params.update({'tokenOauth2': token_API})    
    reponse = requests.get("https://public-api.meteofrance.fr/public/DPClim/v1/commande/fichier", params=params)
    
    with open(dossier_stockage_observations+'ObsMF_'+id_station+'_'+debut_periode+'_'+fin_periode+'.csv','w',encoding="utf-8") as f:
        f.write(reponse.text)
