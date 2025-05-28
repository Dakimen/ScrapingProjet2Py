# English

## Python Scraper for BooksToScrape website

This program serves the purpose of generating a .csv file and downloading the cover images of every book on the bookstoscrape.com website (https://books.toscrape.com/).
On proper execution, the scraper generates an "images" folder containing a .png of the cover of each listed book, as well as a .csv file containing the following information for each entry:

1. The url of the book's page on books.toscrape.com
2. The listed universal product code (UPC)
3. Title
4. Price including tax
5. Price excluding tax
6. Number of available copies
7. Listed description or an empty string in the case of it's absence
8. Listed category
9. Rating out of 5 stars
10. The url of it's cover image

## To run this program:

1. Copy this repostory on your machine.
2. Set up a virtual environment by executing the following commands in the terminal:

   python -m venv [name of your virtual environment]
   For example:
   python -m venv myenv

   Followed by this command, to activate your environment:

   [name of your virtual environment]\Scripts\activate
   Example:
   myenv\Scripts\activate

3. Install the necessary dependencies with: pip install -r requirements.txt

4. Execute main.py in Visual Studio Code or any other IDE capable of executing python code (only tested on Visual Studio Code)

5. Wait for the program to finish it's execution, it can take a few minutes. The program will print urls of each book analysed to visualize the progression of the code's execution

This project was realized as part of an educational program on Python application development.

# Français

## Scraper Python pour le site BooksToScrape

Ce programme permet de générer un fichier .csv et de télécharger les images de couverture de chaque livre du site bookstoscrape.com (https://books.toscrape.com/).
Une fois exécuté correctement, le scraper génère un dossier « images » contenant un fichier .png de la couverture de chaque livre répertorié, ainsi qu'un fichier .csv contenant les informations suivantes pour chaque entrée :

1. L'URL de la page du livre sur books.toscrape.com
2. Le code produit universel (CUP) répertorié
3. Le titre
4. Le prix TTC
5. Le prix hors taxes
6. Le nombre d'exemplaires disponibles
7. La description de l'ouvrage ou une chaîne vide en son absence
8. La catégorie répertoriée
9. La note sur 5 étoiles
10. L'URL de l'image de couverture

## Pour exécuter ce programme :

1. Copiez ce dépôt sur votre ordinateur.
2. Configurez un environnement virtuel en exécutant les commandes suivantes dans le terminal :

`python -m venv [nom de votre environnement virtuel]`
Par exemple :
`python -m venv myenv`

Pour activer votre environnement, exécutez ensuite la commande suivante :

`[nom de votre environnement virtuel]\Scripts\activate`
Exemple :
`myenv\Scripts\activate`

3. Installez les dépendances nécessaires avec : pip install -r requirements.txt

4. Exécutez main.py dans Visual Studio Code ou tout autre IDE capable d'exécuter du code Python (testé uniquement sur Visual Studio Code).

5. Attendez la fin de l'exécution du programme, qui peut prendre quelques minutes. Le programme affichera les URL de chaque livre analysé afin de visualiser la progression de l'exécution du code.

Ce projet a été réalisé dans le cadre d'un programme éducatif sur le développement d'applications Python.
