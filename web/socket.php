<!-- 
!!! Si vous souhaitez tester mon fichier, il faudra décommenter le socket dans votre php.ini de votre hebergeur
Car c'est avec ca que je verifie si le serveur est ON ou OFF

Dans ce fichier au départ je souhaite faire toute l'interface graphique en PHP, javascript et en CSS.

J'ai réussi à communiquer avec mon serveur en python on peut envoyer des messages en remplacant la variable $commande.

Mais apres je me suis rendu compte que pour chaque envoie il fallait que la page se recharge, et quand la page se recharge
socket change aussi et donc on ne pourra pas avoir de suivi, du coup j'ai dû faire une interface administrateur, car je voulais lier mon projet
au web car je suis plus alaise pour faire une interface graphique en web. Egalement, j'ai fait l'interface graphique en python avec tkinter.

-->

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
  
  <title>Document</title>
</head>
<body>
  <?php
  $host = '127.0.0.1';
  $port = '12345';

  $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

  if ($socket == false) {
    echo "Ca n'a pas marché" . socket_strerror(socket_last_error()) . "<br>";
  } else {
    echo "Succès !<br>";
  }

  if (!socket_bind($socket, $host, 0)) {
    echo "Failed to bind socket" . socket_strerror(socket_last_error()) . "<br>";
  } else {
    socket_getsockname($socket, $client_address, $client_port);
    echo "Client socket: $client_address<br>";
    echo "Client IP: " . explode(":", $client_address)[0] . "<br>";
    echo "Client port: $client_port<br>";
  }

  $result = socket_connect($socket, $host, $port);

  if ($result == false) {
    echo "Vérifiez que le serveur est ouvert, et que vous soyez sur la bonne IP / port" . socket_strerror(socket_last_error()) . "<br>";
  } else {
    echo "Vous etes bien connecté :)<br>";
  }

  // Envoi de la commande NAME suivie du nom d'utilisateur
  $message = "NAME bademba\n"; // envoie pseudo bademba
 
  ?>
  <div class="bas">
    <div class="lechat">
      <?php 
       socket_write($socket, $message, strlen($message));
       $reponse = socket_read($socket, 1024);
     
      echo "<p>Serveur: " . $reponse . "<br>"; ?>
    </div>
    <br>
    <label for="">Tchat :</label>
    <input placeholder="Exemple: NAME bademba" type="text">
  </div>
</body>
</html>
