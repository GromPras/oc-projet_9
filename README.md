# Développez une application Web en utilisant Django

## Français

### Introducion

Une application Django qui permet aux utilisateurs connectés de demander ou poster des critiques d'articles ou de livres.

# Installation

Pré-requis:

- Python >= 3.12
- Git 2.x (only if cloning the repo)

```sh
git clone https://github.com/GromPras/oc-projet_9.git
```

`Ou téléchargez le fichier ZIP depuis https://github.com/GromPras/oc-projet_4/archive/refs/heads/main.zip`

Créez un environement virtuel à l'intérieur du dossier cloné:

```sh
cd oc-projet_9
python3 -m venv {/path/to/virtual/environment}
```

Sur Windows, appelez la commande venv comme suit :

```sh
c:\>c:\Python3\python -m venv c:\path\to\myenv
```

Activer l'environement virtuel :

````sh
source {/path/to/virtual/environment}/bin/activate

Sur Windows, appelez la commande venv comme suit :

```sh
C:\> <venv>\Scripts\activate.bat
````

Installez les packages requis :

```sh
pip install -r requirements.txt
```

Ou sur Windows :

```sh
py -m pip install -r requirements.txt
```

Si vous avez un problème avec la création de l'environnement consultez la documentation : `https://docs.python.org/fr/3/library/venv.html#creating-virtual-environments`

### Post Installation

#### Pour lancer le programme, exécutez la commande suivante :

```sh
cd litrevu
python3 manage.py runserver
```
