# BrainMapperV2

Nous conseillons l'utilisations d'environnement python via [virtualenv](https://virtualenv.pypa.io/en/latest/) ou  [venv](https://docs.python.org/3/library/venv.html)

## Installer qt pour python3
## MacOS
See the installation folder

### Linux

```bash
sudo apt-get install python3-pyqt4
sudo apt-get install python3-pyqt4.qtopengl
```

### Windows

Télécharger le fichier pyqt4 avec la version correspondante à votre version de python: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4

Lancer dans un powershell la commande suivante :
```powershell
pip install C:\path\where\wheel\is\PyQt4-4.11.4-cp36-cp36m-win_amd64.whl  ( cette exemple est fait avec une version de pyqt4 pour python 3.6)
```

## Autres dépendances

Vous pouvez les installer à la main :
```bash
python3 -m pip install nibabel
python3 -m pip install -U numpy
python3 -m pip install -U scikit-learn
python3 -m pip install pyqtgraph
python3 -m pip install pyopengl
python3 -m pip install nilearn
```

Ou via le fichier requirement.txt

```bash
pip install -r requirement.txt
```
