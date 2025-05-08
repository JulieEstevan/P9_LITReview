# LITReview

***

P9_LITReview is a web application using the Django framework. It behaves like a social network dedicated to literature where users can post, request book reviews and follow other users.

***


## Installation for Windows

Open your Shell terminal then:

Target the file:
```
cd ..\P9_LITReview
```
Install and create a virtual environment:
```
python -m pip install virtualenv
python -m venv env
```
Activate this environment:
```
env\Scripts\activate
```
Install the requirements:
```
pip install -r requirements.txt
```

## Installation for MacOs/Linux

Open your terminal then:

Target the file:
```
cd ..\P9_LITReview
```
Install and create a virtual environment:
```
python3 -m pip install virtualenv
python3 -m venv env
```
Activate this environment:
```
source env\bin\activate
```
Install the requirements:
```
pip install -r requirements.txt
```

***


## Application

After installation, start the server using your terminal:

```
python3 manage.py runserver
```
Then connect to the local server on your browser at:
http://127.0.0.1:8000/

You also have the posibility to start the server on an other port with the following command:

```
python3 manage.py runserver *port_number*
```

The address will then be:
 http://127.0.0.1:*port_number*/


# LITReview

***

P9_LITReview est une application web utilisant le framework Django. Elle se comporte comme un réseau social dédié à la littérature où les utilisateurs peuvent publier, demander des critique de livres et suivre d'autres utilisateur.

***


## Installation pour Windows

Ouvrez votre terminal Shell puis:

Ciblez le fichier:
```
cd ..\P9_LITReview
```
Installez et créez un environement virtuel:
```
python -m pip install virtualenv
python -m venv env
```
Activez cet environement:
```
env\Scripts\activate.bat
```
Installez le requirements:
```
pip install -r requirements.txt
```

## Installation pour MacOs/Linux

Ouvrez votre terminal puis:

Ciblez le fichier:
```
cd ..\P9_LITReview
```
Installez et créez un environement virtuel:
```
python3 -m pip install virtualenv
python3 -m venv env
```
Activez cet environement:
```
source env\bin\activate
```
Installez le requirements:
```
pip install -r requirements.txt
```

***


## Utilisation

Après l’installation, lancez le serveur via votre terminal:

```
python3 manage.py runserver
```
Puis connectez-vous au serveur local via votre navigateur à l'adresse:
http://127.0.0.1:8000/

Vous avez aussi la possibilité de lancer le serveur sur un autre port avec la commande suivante: 

```
python3 manage.py runserver *numero_du_port*
```

L'adresse sera alors:
http://127.0.0.1:*numero_du_port*/
