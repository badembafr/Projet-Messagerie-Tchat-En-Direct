# 📢 Projet Final : Tchat

Bienvenue dans le projet **Tchat**, développé dans le cadre du cours *Systèmes et Réseaux* (2023-2024) à l'Université Paris 8.

## 👨‍🎓 Informations Générales

- **Nom** : Bademba SANGARE
- **Formation** : Licence Informatique
- **Année** : 2023-2024
- **Cours** : [Systèmes et Réseaux](https://pablo.rauzy.name/teaching/sr/)
- **Professeur** : PR (<pr@up8·edu>)

---

## 📌 Prérequis

Avant de lancer le projet, assurez-vous d'avoir les éléments suivants installés et configurés :

### 🖥️ Serveur Web Local (ex : XAMPP)
- **PhpMyAdmin**
- **Base de données** : Insérez `bdd/tchat.sql`
- **Configuration de connexion** : Définissez `localhost`, `user`, `passwd`
- **Vérification du port** : Le port par défaut est `12345`, assurez-vous qu'il soit libre avec la commande :
  ```bash
  netstat -tunl
  ```
- **Navigateur web**

### 🐍 Python
- Installez les dépendances avec :
  ```bash
  pip install socket threading datetime time tkinter
  ```
  *(Certains modules sont inclus par défaut dans Python)*
- Terminal `CMD`

---

## 📂 Structure du Projet

Le projet est organisé en trois dossiers principaux :

### 🗃️ `bdd/` (Base de données)
- Contient la base de données **SQL** (`tchat.sql`)

### 🐍 `python/` (Serveur & Client)
- `serveur.py` : Serveur web basé sur **sockets**
- `client.py` : Interface utilisateur **Tkinter**
- `notice.txt` : Ouvrable via l'interface client

### 🌍 `web/` (Interface Web)
- `index.php` : Interface web **administrateur**
  - ⚠️ **Assurez-vous d’activer l'extension socket en PHP !** 🔧
  - 📌 Aide : [Activer socket en PHP](https://stackoverflow.com/questions/1361925/how-to-enable-socket-in-php)
- `socket.php` : **Tchat interactif** avec le serveur Python
  - 🚧 **Limitation** : Nécessite un rechargement de page à chaque envoi, ce qui entraîne une perte du suivi de session **contrairement au terminal Python** qui maintient une connexion persistante.
- `style.css` : Fichier CSS pour le **design** de `index.php` et `socket.php`

📢 **Conseil** : Placez le dossier `web/` dans `htdocs/` de **XAMPP** (ou autre hébergeur) pour un accès optimal !

---

🚀 **Bon développement et bon test du Tchat !** 🎉