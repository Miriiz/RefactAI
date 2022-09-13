# RefactAI
Ce projet est inspiré du projet Code Defect AI d’Altran
RefactAI est un programme qui s'ajoute dans une chaîne de CI/CD github actions.

Ce programme possède trois parties :
- La première va permettre de générer la documentation d’un projet python, pour obtenir une description de l’ensemble des fonctions de ce projet. 
- La seconde partie va permettre d’identifier de potentiels bugs dans ce même code, notamment via un fichier de logs qui indiquera les fonctions où ces bugs pourront possiblement apparaître. 
- La dernière partie, quant à elle, va permettre d’identifier si les commentaires au-dessus d’une fonction correspondent bien avec celle-ci. 

## Architecture AWS
![image](https://user-images.githubusercontent.com/37442009/189965598-4ced2a00-f1c5-485b-8d95-04d4bf64fd4d.png)

## Dataset
Les données utilisées pour entraîner le modèle 

## Comparaison des commentaires
Nous afficherons le pourcentage de compatibilité entre le commentaire au-dessus de la fonction et ce que notre modèle prédit. Cette option permettra aux utilisateurs d’avoir une indication sur leurs commentaires. 

![image](https://user-images.githubusercontent.com/37442009/189966754-700a68a2-f41b-4992-bc57-b82e65fdd8a8.png)
![image](https://user-images.githubusercontent.com/37442009/189966777-25498276-e81a-44d9-8c11-c719fac1376c.png)
