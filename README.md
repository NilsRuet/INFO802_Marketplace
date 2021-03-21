# Info802
Rendu du TP d'Info802 sur un marketplace. Il se divise en deux parties, une partie site web et une partie webservice soap. La partie site web s'exécute à l'aide de Flask sous python 3.8, les dépendances sont listées dans le fichier "/Client/requirements.txt". La partie webservice soap s'exécute sous java 8, le projet est un projet maven donc les dépendances sont inclues dans "/SOAPDelivery/pom.xml".

Le site est en interaction avec le webservice soap, avec l'api mangopay via rest et avec l'api back4app (stockage des données) via graphql. Pour pouvoir le déployer, il est nécessaire de fournir des clés apis ou autres informations pour que les requêtes s'exécutent correctement. Pour cela, il faut compléter le fichier "Client/config.json".

## Version déployée
Une version déployée du site peut-être trouvée ici : http://info802-marketplace.azurewebsites.net/
Le webservice SOAP est quand à lui déployé ici : https://app-soapdelivery.azurewebsites.net/SOAPLivraison-1.0-SNAPSHOT/services/DeliveryCost?wsdl

Le site n'a pas vraiment de système d'authentification, l'inscription comme la connexion se font donc uniquement via prénom et nom (case sensitive). Pour alimenter son portefeuille une fois connecté, il faut utiliser une carte de crédit de test. La liste des cartes de crédit de test valides est disponible ici : https://docs.mangopay.com/guide/testing-payments
