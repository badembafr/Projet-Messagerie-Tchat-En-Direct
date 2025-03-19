#importation des bibliotheques
import socket
import threading
import datetime
import time

# ici on va renseigner l'hote et le port du serveur
HOTE = '127.0.0.1'
PORT = 12345
CLIENTS_MAX = 100 #nombre maximum sur le server

import mysql.connector

# Se connecter à la base de donées
connexion = mysql.connector.connect(
    host="localhost",
    user="root", #par default personellement ici c'est root (à edit peut etre)
    password="", #ici j'utlise xampp et par default pas de mdp
    database="tchat" #il faut bien utliser le fichier tchat.sql et intégrer à votre phpmyadmin
)

curseur = connexion.cursor()

# on va stocker les informations sur les clients et des infos sur les groupes
groupes = {}
clients = {}
pseudos_utilises = []
connexions_clients = {}

# Permettre de constament gérer la connextion entre client
def gestion_client(client_socket, adresse_client):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                print(f"L'utlisateur {adresse_client} s'est déconnecté.")
                break
            gerer_message(data, client_socket)  
        except Exception as e:
            #print(f"Erreur client -> {adresse_client}: {e}")
            print(f"L'utilisateur {adresse_client}  s'est déconnecté.")
            gerer_deco(client_socket)  # deconnecer l'user
            break  

    client_socket.close()
    supp_client(adresse_client)  


# c'est là qu'on va gérer tous les messages que le client va nous envoyer
def gerer_message(message, client_socket):
    print("Messsage:", message) #permet de debugger
    print("\n")
    print("Client socket:\n", client_socket) #permet de debugger
    parts = message.split(' ')
    cmd = parts[0]

    if cmd == 'NAME':
        if len(parts) != 2:  # On vérifie le nombre de parametre(s)
            client_socket.sendall('NOPE 12\n'.encode('utf-8'))  # Renvoie l'erreur de nom invalide
        else:
            gerer_nom(parts[1], client_socket)
    elif cmd == 'CRGP':
        if len(parts) != 3:  # CRGP doit avoir trois parties: 'CRGP', <taille>, <nom_groupe>
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))
        else:
            # Est ce que le client est  bien identifié ?
            if client_socket in clients:
                creer_groupe(parts[1], parts[2], client_socket)
            else:
                client_socket.sendall('NOPE 10\n'.encode('utf-8'))
  
    elif cmd == 'JOIN':
        # vérifie si le nombre de parties dans la cmd est correct
        if len(parts) != 2:  # JOIN doit avoir deux parties: 'JOIN', <nom_groupe>
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))  
        else: 
            # Vérifier si le client est  bien identifié
            if client_socket in clients:
                rejoindre_groupe(parts[1], client_socket)  # Appeler la fonction pour rejoindre le groupe
            else: 
                client_socket.sendall('NOPE 10\n'.encode('utf-8'))  

    elif cmd == 'QUIT':
        if len(parts) != 2:
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))  
        else :
            if client_socket in clients:
                quitter_groupe(parts[1], client_socket)
            else:
                client_socket.sendall('NOPE 10\n'.encode('utf-8'))  
  
    elif cmd == 'EXIT':
        if len(parts) != 1:  # Vérifier si la cmd EXIT est bien entrée
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))  
        elif client_socket in clients:  # Vérifier si le client est bien co
            gerer_deco(client_socket) 
        else:    
            client_socket.sendall('NOPE 10\n'.encode('utf-8'))   
            

    elif cmd == 'MESS':
        if len(parts) < 3:  # On vérifie si le nombre de parties est insuffisant
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))    
        else:
            if client_socket in clients:
                envoyer_mess_grp(parts[1], ' '.join(parts[2:]), client_socket)  
            else:
                client_socket.sendall('NOPE 10\n'.encode('utf-8'))  

    elif cmd == 'PRIV':
        if len(parts) < 3:  # Vérifie si le nombre de parties est insuffisant
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))  
        else:
            if client_socket in clients:
                envoyer_mess_pv(parts[1], ' '.join(parts[2:]), clients[client_socket], client_socket)  
            else:
                client_socket.sendall('NOPE 10\n'.encode('utf-8'))  

    elif cmd == 'LIST':  
        if len(parts) != 1:  # Vérifie si la cmd LIST est bien entrée
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))  
        else:  
            lst_clients(client_socket)  
 
    elif cmd == 'GRPL':  
        if len(parts) != 1:  # Vérifie si la cmd GRPL est bien entrée
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))  
        else:
            #renvoyer la liste des groupes existants
            liste_grp(client_socket)
      
    elif cmd == 'MEMB':  
        if len(parts) != 2:  # Vérifie si le nombre de parties est incorrect
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))  
        else:  
            if client_socket in clients:  
                lst_membres_grp(parts[1], client_socket) 
            else:
                client_socket.sendall('NOPE 10\n'.encode('utf-8'))  
     
    elif cmd == 'PING':
        # Répondre au ping du client par un PONG
        client_socket.sendall('PONG\n'.encode('utf-8'))  

        #enregistrer le ping et la réponse dans les connexions_clients
        adresse_client = client_socket.getpeername()
        if adresse_client in connexions_clients:
            connexions_clients[adresse_client].append(('PING', datetime.datetime.now()))  
        else:
            connexions_clients[adresse_client] = [('PING', datetime.datetime.now())]
        
        # Afficher un message sur le serveur pour indiquer le ping et la réponse
        print(f"Le client {adresse_client} nous a envoyé un ping")
        print(f"Le serveur a répondu avec un PONG au client {adresse_client}")
    else:
        client_socket.sendall('NOPE 0\n'.encode('utf-8'))
    
# Gérer la cmd NAME du client
def gerer_nom(nom_utilisateur, client_socket):  
    if not nom_utilisateur:  # Est ce que le nom est vide ?
        client_socket.sendall('NOPE 12\n'.encode('utf-8'))  # Renvoie une erreur  car nom pas bon
    elif nom_utilisateur in pseudos_utilises:  
        # Le nom de ne doit pas etre pris par un autre client
        for socket_client, pseudo_client in clients.items():
            if pseudo_client == nom_utilisateur and socket_client != client_socket:
                client_socket.sendall('NOPE 13\n'.encode('utf-8'))  # Nom déjà pris par un autre client
                break  
        else:  
            client_socket.sendall('NOPE 11\n'.encode('utf-8'))  # Le client c'est s'est deja loggé 
    elif ' ' in nom_utilisateur or len(nom_utilisateur) < 1 or len(nom_utilisateur) > 25:
        client_socket.sendall('NOPE 12\n'.encode('utf-8'))  # Renvoie une erreur  car pseudo pas bon
    else:  
        clients[client_socket] = nom_utilisateur  
        pseudos_utilises.append(nom_utilisateur)
        
        # Insérer le pseudo dans la table pseudos_utilises
        sql_insert = "INSERT INTO pseudos_utilises (pseudo) VALUES (%s)"
        curseur.execute(sql_insert, (nom_utilisateur,))
        connexion.commit()  # Valider la transaction
        
        client_socket.sendall(f'HELO {nom_utilisateur}\n'.encode('utf-8'))

#Lister la liste des clients
def lst_clients(client_socket):   
    if client_socket in clients:  # On vérifie si le client est identifié
        if len(pseudos_utilises) == 0: # si y'a personne de connecté
            client_socket.sendall('NOPE 0\n'.encode('utf-8'))    
        else:
            #  Faire liste des pseudos des clients connectés
            pseudos_connectes = '\n'.join(pseudos_utilises)   
        
            # Envoi de la liste des pseudos au client
            client_socket.sendall(f'LIST {len(pseudos_utilises)}\n{pseudos_connectes}\n'.encode('utf-8'))
    else:
        client_socket.sendall('NOPE 10\n'.encode('utf-8'))    

#Lister la liste des groupes
def liste_grp(client_socket):      
    if client_socket in clients:  # Vérifier si le client est identifié
        if len(groupes) == 0:  
            client_socket.sendall('NOPE 17\n'.encode('utf-8'))  
        else:             
            # Faire liste des noms de groupes existants
            noms_groupes = '\n'.join(groupes.keys())
        
            # Envoyer de la liste des groupes à notre client
            client_socket.sendall(f'GRPL {len(groupes)}\n{noms_groupes}\n'.encode('utf-8'))
    else:
        client_socket.sendall('NOPE 10\n'.encode('utf-8'))            
  
# Créer un groupe
def creer_groupe(taille_groupe, nom_groupe, client_socket):
    # Vérifier si le nom du groupe existe déjà dans la base de données
    sql_check_group = "SELECT * FROM groupes WHERE nom = %s"
    curseur.execute(sql_check_group, (nom_groupe,))
    result = curseur.fetchone()

    if result:  
        client_socket.sendall('NOPE 0\n'.encode('utf-8')) 
    elif int(taille_groupe) <= 0:
        client_socket.sendall('NOPE 17\n'.encode('utf-8')) 
    else:  
        # Insérer le nom du groupe dans la table 'groupes' 
        sql_insert_group = "INSERT INTO groupes (nom) VALUES (%s)"
        curseur.execute(sql_insert_group, (nom_groupe,)) 
        connexion.commit()  # Valider la transaction

        # Ajouter le groupe à la variable 'groupes' en mémoire
        groupes[nom_groupe] = {'taille': int(taille_groupe), 'membres': [clients[client_socket]]}
        
        # Envoyer une réponse au client pour indiquer la création réussie du groupe
        client_socket.sendall(f'INTO {nom_groupe} 1\n{clients[client_socket]}\n'.encode('utf-8'))
 
  
# Rejoindre un groupe
def rejoindre_groupe(nom_groupe, client_socket):
    if nom_groupe not in groupes:   
        client_socket.sendall('NOPE 14\n'.encode('utf-8')) 
    elif clients[client_socket] in groupes[nom_groupe]['membres']:
        client_socket.sendall('NOPE 0\n'.encode('utf-8'))
    else:  
        if len(groupes[nom_groupe]['membres']) < groupes[nom_groupe]['taille']:
            groupes[nom_groupe]['membres'].append(clients[client_socket]) 
            membres = '\n'.join(groupes[nom_groupe]['membres'])  
            client_socket.sendall(f'INTO {nom_groupe} {len(groupes[nom_groupe]["membres"])}\n{membres}\n'.encode('utf-8'))
            for membre in groupes[nom_groupe]['membres']:   
                membre_socket = [sock for sock, pseudo in clients.items() if pseudo == membre][0]
                membre_socket.sendall(f'ANEW {clients[client_socket]}\n'.encode('utf-8'))
        else:
            client_socket.sendall('NOPE 16\n'.encode('utf-8'))

#Deconnextion du client
def gerer_deco(client_socket):
    if client_socket in clients:   
        pseudo_deconnecte = clients[client_socket]  
        del clients[client_socket]  # Retirer le client de la liste avant de fermer sa connexion
        message = f'EXIT {pseudo_deconnecte}\n'.encode('utf-8')
        for sock in clients:   
            sock.sendall(message)   
        client_socket.close()   
        
        # Supprimer le pseudo de la liste des pseudos use
        if pseudo_deconnecte in pseudos_utilises:
            pseudos_utilises.remove(pseudo_deconnecte)  

        # Supprimer le pseudo de la bdd 
        sql_delete = "DELETE FROM pseudos_utilises WHERE pseudo = %s"
        curseur.execute(sql_delete, (pseudo_deconnecte,))
        connexion.commit()  # valider bdd

    else:  
        client_socket.sendall('NOPE 10\n'.encode('utf-8'))


# Fonction pour quitter un groupe  
def quitter_groupe(nom_groupe, client_socket): 
    if client_socket in clients:    
        if nom_groupe not in groupes:    
            client_socket.sendall('NOPE 14\n'.encode('utf-8'))    
        elif clients[client_socket] not in groupes[nom_groupe]['membres']:  
            client_socket.sendall('NOPE 18\n'.encode('utf-8'))  
                
        else:
            pseudo_quittant = clients[client_socket]      
            groupes[nom_groupe]['membres'].remove(pseudo_quittant)   
            for membre in groupes[nom_groupe]['membres']:    
                membre_socket = [sock for sock, pseudo in clients.items() if pseudo == membre]
                if membre_socket:  # Vérifier si le socket du membre est toujours actif 
                    membre_socket[0].sendall(f'QUIT {pseudo_quittant}\n'.encode('utf-8'))  
            if len(groupes[nom_groupe]['membres']) == 0:   
                del groupes[nom_groupe]  # Supprimer le groupe s'il est vide 
            client_socket.sendall('LEFT\n'.encode('utf-8'))  
               
    else:
        client_socket.sendall('NOPE 10\n'.encode('utf-8'))

# Fonction pour envoyer un message à un groupe
def envoyer_mess_grp(nom_groupe, message, client_socket):
    if nom_groupe not in groupes:  
        client_socket.sendall('NOPE 14\n'.encode('utf-8'))  
    elif clients[client_socket] not in groupes[nom_groupe]['membres']:  
        client_socket.sendall('NOPE 18\n'.encode('utf-8'))  
    else:
        for membre in groupes[nom_groupe]['membres']:   
            membre_socket = [sock for sock, pseudo in clients.items() if pseudo == membre][0]  
            membre_socket.sendall(f'MESS {nom_groupe} {clients[client_socket]} {message}\n'.encode('utf-8'))  

# Envoyer un message privé à un client
def envoyer_mess_pv(destinataire, message, emetteur, emetteur_socket):  
    if destinataire not in pseudos_utilises:   
        emetteur_socket.sendall('NOPE 15\n'.encode('utf-8'))    
    else:  
        destinataire_socket = [sock for sock, pseudo in clients.items() if pseudo == destinataire][0]  
        destinataire_socket.sendall(f'PRIV {emetteur} {message}\n'.encode('utf-8'))  
        emetteur_socket.sendall(f'PRIV {emetteur} {message}\n'.encode('utf-8'))  # Envoyer également le message à l'émetteur

# Lister les membres d'un groupe
def lst_membres_grp(nom_groupe, client_socket):  
    if nom_groupe not in groupes: 
        client_socket.sendall('NOPE 14\n'.encode('utf-8')) 
    else:  
        membres = '\n'.join(groupes[nom_groupe]['membres']) 
        client_socket.sendall(f'INTO {nom_groupe} {len(groupes[nom_groupe]["membres"])}\n{membres}\n'.encode('utf-8'))


# Supprimer un client  
def supp_client(adresse_client):  
    for sock, nom_utilisateur in clients.items():
        if sock.getpeername() == adresse_client: 
            del clients[sock] 
            break  
  
# Démarrage de notre serveur
def demarrer_serveur():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server_socket.bind((HOTE, PORT))    
    server_socket.listen(CLIENTS_MAX)  
    print("Succès ! Le serveur est désormait en écoute.")  
    print(f"Ecoute sur :{HOTE}:{PORT}")
    
    while True:
        client_socket, adresse_client = server_socket.accept()  
        print(f"Connexion de {adresse_client}")  
        thread_client = threading.Thread(target=gestion_client, args=(client_socket, adresse_client))
        thread_client.start()
  
demarrer_serveur()
