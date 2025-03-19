<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
  <title>Projet tchat - Systèmes et réseaux</title>
</head>
<body>
  <div class="top">
    <h1>Interface administrateur - Tchat</h1>
    <p>Ici on pourra accéder à certains éléments de façon plus simple.</p>
  </div>

  <div class="sec">
    <div class="gauche">
       <div class="box">
        <h2>Commandes disponibles client</h2>
         <table border="1" cellspacing="0">
          <thead>
            <tr>
              <th>Commande</th>
            </tr>
          </thead>
          <tbody>
             <tr>
              <td>NAME &lt;pseudo&gt;</td>
            </tr>
            <tr>
              <td>HELO &lt;pseudo&gt;</td>
            </tr>
            <tr>
              <td>CRGP &lt;N&gt; &lt;groupe&gt;</td>
            </tr>
            <tr>
              <td>JOIN &lt;groupe&gt;</td>
             </tr>
            <tr>
              <td>QUIT &lt;groupe&gt;</td>
            </tr>
            <tr>
              <td>LEFT</td>
            </tr>
            <tr>
              <td>MESS &lt;groupe&gt; &lt;message&gt;</td>
            </tr>
            <tr>
              <td>PRIV &lt;pseudo&gt; &lt;message&gt;</td>
            </tr>
            <tr>
              <td>LIST</td>
            </tr>
             <tr>
              <td>GRPL</td> 
            </tr>
            <tr>
              <td>MEMB &lt;groupe&gt;</td>
            </tr>
            <tr>
              <td>EXIT</td>
            </tr>
            <tr>
               <td>PING</td>
            </tr>
            <tr>
              <td>PONG</td>
            </tr>
          </tbody>
        </table>
      </div> 
      <div class="box">
        <h2>Code d'erreur serveur</h2> 
        <table>
          <tr>
            <th>Code</th>
            <th>Signification</th>
          </tr>
          <tr>
            <td>0*</td>
            <td>erreur serveur</td>
          </tr>
          <tr> 
            <td>10</td>
            <td>client non identifié</td>
          </tr>
          <tr>
            <td>11</td>
            <td>client déjà identifié</td>
          </tr> 
          <tr>
            <td>12</td>
            <td>nom invalide</td>
          </tr>
          <tr>
            <td>13</td>
            <td>nom déjà pris</td> 
          </tr>
          <tr>
            <td>14</td>
            <td>nom inexistant</td>
          </tr>
          <tr> 
            <td>15</td>
            <td>serveur plein</td>
          </tr>
          <tr>
            <td>16</td>
            <td>groupe plein</td>
          </tr>
          <tr>
            <td>17</td> 
            <td>taille incorrecte</td>
          </tr>
          <tr>
            <td>18</td>
            <td>client non membre du groupe</td>
          </tr> 
        </table>
      </div>
    </div>
    <div class="infos">
      <div class="noms">
        <div>
          <p><strong>Liste des membres connectés :</strong></p>
          <?php 
          $connexion = new mysqli("localhost", "root", "", "tchat");
          if ($connexion->connect_error) {
            die("Connection failed: " . $connexion->connect_error); 
          }
          $requete_noms = "SELECT pseudo FROM pseudos_utilises";
          $resultat_noms = $connexion->query($requete_noms);
          if ($resultat_noms->num_rows > 0) {
            while($row = $resultat_noms->fetch_assoc()) {
              echo "<p>" . $row["pseudo"] . "</p>";
            }
          } else {
            echo "<p>Tous les utilisateurs sont déconnectés.</p>";
          }
          $connexion->close(); 
          ?>
        </div>
      </div>
      <div class="nbco">
        <?php
        $connexion = new mysqli("localhost", "root", "", "tchat");
        if ($connexion->connect_error) { 
          die("Connection failed: " . $connexion->connect_error);
        }
        $requete_nb_co = "SELECT COUNT(*) as total FROM pseudos_utilises";
        $resultat_nb_co = $connexion->query($requete_nb_co);
        $row_nb_co = $resultat_nb_co->fetch_assoc();
        echo "<p>" . $row_nb_co["total"] . " personnes connectée(s)</p>";
        $connexion->close();
        ?>
      </div> 
      <div class="groupes">
        <p>Listes des groupes</p>
        <?php 
        $connexion = new mysqli("localhost", "root", "", "tchat");
        if ($connexion->connect_error) {
          die("Erreur: " . $connexion->connect_error);
        }
        $requete_grp = "SELECT nom FROM groupes";
        $resultat_grp = $connexion->query($requete_grp);
        if ($resultat_grp->num_rows > 0) {
          while($row = $resultat_grp->fetch_assoc()) {
            echo "<p>" . $row["nom"] . "</p>";
          }
        } else {
          echo "<p>Aucun groupe pour le moment.</p>";
        }

        ?>
      </div>
      <div class ="grpco">
        <?php
        $requete_nb_groupes = "SELECT COUNT(*) as total FROM groupes";
        $resultat_nb_groupes = $connexion->query($requete_nb_groupes);
        $row_nb_groupes = $resultat_nb_groupes->fetch_assoc();
        echo "<p>Nombre de groupes : " . $row_nb_groupes["total"] . "</p>";
        $connexion->close();
        ?>
      </div>
      <div class="text">

      <strong>!!! Si vous souhaitez tester mon fichier, il faudra décommenter le socket dans votre php.ini de votre hebergeur</strong>
      <p>
      
        Car c'est avec ca que je verifie si le serveur est ON ou OFF

        Dans ce fichier au départ je souhaite faire toute l'interface graphique en PHP, javascript et en CSS.

        J'ai réussi à communiquer avec mon serveur en python on peut envoyer des messages en remplacant la variable $commande.

        Mais apres je me suis rendu compte que pour chaque envoie il fallait que la page se recharge, et quand la page se recharge
        socket change aussi et donc on ne pourra pas avoir de suivi, du coup j'ai dû faire une interface administrateur, car je voulais lier mon projet
        au web car je suis plus alaise pour faire une interface graphique en web. Egalement, j'ai fait l'interface graphique en python avec tkinter.
      </p>
      <a href="socket.php">Tester mon tchat version socket (pas complet, et bien ajouter l'option socket dans votre php.ini)</a>
      </div>

    </div>
      <?php
        $host = '127.0.0.1';
        $port = '12345';

        $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

        $result = socket_connect($socket, $host, $port);

        if ($result == false) {
          echo "<div style='background-color: red'><p>SERVEUR OFF :/<br>Vérifiez que le serveur est ouvert, et que vous soyez sur la bonne IP / port<br>" . socket_strerror(socket_last_error()) . "</p></div>";
        } else {
          echo "<div style='background-color: green'><p>Le serveur est ON ! :)</p></div>";
        }
      ?>
  </div>
</body>
</html>
