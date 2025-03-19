import socket
import threading 
import tkinter as tk
import time

HOTE = '127.0.0.1'  
PORT = 12345 

def recevoir_message(client_socket, text_widget): 
    while True: 
        try:     
            message = client_socket.recv(1024).decode('utf-8')
            if not message: 
                break  
   
            if message.strip() == "PONG": 
                continue 
            elif message.strip().startswith("NOPE 0"): 
                text_widget.insert(tk.END, "Erreur de serveur\n")
            elif message.strip().startswith("NOPE 10"):
                text_widget.insert(tk.END, "Non identifié\n") 
            elif message.strip().startswith("NOPE 11"): 
                text_widget.insert(tk.END, "Client déjà identifié\n")
            elif message.strip().startswith("NOPE 12"):
                text_widget.insert(tk.END, "Nom invalide\n") 
            elif message.strip().startswith("NOPE 13"): 
                text_widget.insert(tk.END, "Nom déjà pris\n")
            elif message.strip().startswith("NOPE 14"):
                text_widget.insert(tk.END, "Nom inexistant \n")
            elif message.strip().startswith("NOPE 15"):
                text_widget.insert(tk.END, "Serveur plein\n") 
            elif message.strip().startswith("NOPE 16"):  
                text_widget.insert(tk.END, "Groupe plein\n")
            elif message.strip().startswith("NOPE 17"): 
                text_widget.insert(tk.END, "Taille incorrecte\n")
            elif message.strip().startswith("NOPE 18"):
                text_widget.insert(tk.END, "Client non membre du groupe\n")
            else:
                text_widget.insert(tk.END, message + '\n') 
             
        except Exception as e:
            text_widget.insert(tk.END, f"erreur message: {e}\n") 
            break

def send_message(client_socket, entry_message, text_chat):
    message = entry_message.get() 
    client_socket.sendall(message.encode('utf-8')) 
    entry_message.delete(0, tk.END)
    current_time = time.strftime('%H:%M:%S')
    text_chat.insert(tk.END, f"\n{current_time} - Client: {message}\n")

def fenetre(client_socket, adresse_client): 
    root = tk.Tk() 
    root.geometry("600x700") 
    root.title("Projet Tchat Systèmes et Réseaux - {}".format(client_socket.getsockname())) 
    root.configure(bg="red")    

    frame_chat = tk.Frame(root, bg="#222222", bd=2)   
    frame_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True) 

    text_chat = tk.Text(frame_chat, bg="#111111", fg="#FFFFFF", bd=0) 
    text_chat.pack(fill=tk.BOTH, expand=True) 

    # Afficher le message de connexion dans la zone de texte du chat
    text_chat.insert(tk.END, "Vous êtes bien connecté au serveur.\n")  
    text_chat.insert(tk.END, "IP : {}\n".format(adresse_client[0])) 
    text_chat.insert(tk.END, "Port du client : {}\n".format(adresse_client[1])) 
    text_chat.insert(tk.END, "\nCommencez par vous identifier :") 
    text_chat.insert(tk.END, "\nNAME <pseudo>\n")  

    frame_input = tk.Frame(root, bg="grey")
    frame_input.pack(padx=10, pady=10, fill=tk.X) 

    entry_message = tk.Entry(frame_input, bg="grey", fg="black", bd=0)
    entry_message.pack(side=tk.LEFT, fill=tk.X, expand=True)

    button_send = tk.Button(frame_input, text="Envoyer", bg="#555555", fg="#FFFFFF", bd=0, command=lambda: send_message(client_socket, entry_message, text_chat))
    button_send.pack(side=tk.RIGHT)

    def aff_info_fenetre(): 
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8') 
                if not message:
                    break
                text_chat.insert(tk.END, message + '\n')
            except Exception as e:
                print(f"Erreur lors de la réception du message: {e}")
                break 

    thread_receive = threading.Thread(target=recevoir_message, args=(client_socket, text_chat))
    thread_receive.start() 
 
    root.mainloop()

if __name__ == "__main__": 
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOTE, PORT))       
        adresse_client = client_socket.getsockname() 
        print("Vous êtes bien connecté au serveur.") 
        print("IP :",adresse_client[0]) 
        print("Port du client :",adresse_client[1]) 

        fenetre(client_socket, adresse_client) 

    except Exception as e: 
        print(f"Erreur: {e}")
        print("NOPE 0 : Vérifiez que le serveur est bien lancé !") 
    finally:
       client_socket.close() 