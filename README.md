Météo-France, CNRS, Univ. Toulouse, CNRM, Toulouse, France

Script d'extraction automatique des observations horaires de la BDCLIM via l'API Météo-France.
Ce script est un exemple d'extraction des observations de l'ensemble d'un département. 
En faisant des boucles et en respectant les limites du nombre de requêtes, il peut être étendu à toute la France

Prérequis : 
1) Se créer gratuitement un compte sur le portail des API : https://portail-api.meteofrance.fr
2) Aller sur la page : https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesClimatologie
3) Cliquer sur Souscrire à l'API gratuitement
4) Puis "Configurer l'API"
5) Cliquer sur "type de TOKEN" puis "API Key", durée mettre "3600" pour 1 heure par exemple
6) Remplacez dans le code ci-dessous la chaîne de caractère dénommée "cle_API" par votre clef

Pour aller plus loin, n'hésitez pas à consulter la FAQ : https://portail-api.meteofrance.fr/web/fr/faq.
Notamment si vous voulez utiliser le système OAuth2 d'authentification, plus complexe pour les débutants mais permettant
d'automatiser la connexion aux serveurs de MF via la demande de jetons (tokens) notamment si vous effectuez fréquemment des requêtes 
