# Installation

## Windows WSL

```
sudo apt update
sudo apt upgrade
sudo apt install nginx
sudo service nginx start
```

### configuration Nginx

L'utilisation de Nginx sur WSL (Windows Subsystem for Linux) peut fonctionner correctement, mais il y a quelques points
à considérer pour s'assurer que tout fonctionne comme prévu. Voici les étapes pour configurer et exécuter Nginx sur WSL
et assurer que votre application FastAPI soit accessible à distance.

### Étapes pour Configurer Nginx sur WSL

1. **Ouvrez un Terminal WSL**

   Assurez-vous que votre distribution Linux est à jour :

   ```sh
   sudo apt update
   sudo apt upgrade
   ```

2. **Installez Nginx**

   ```sh
   sudo apt install nginx
   ```

3. **Démarrez Nginx**

   ```sh
   sudo service nginx start
   ```

#### 2. Configurer Nginx pour l'api FastAPI

1. **Récuperer l'address IP de wsl**

dans un terminal powershell :

```powershell
wsl hostname -I
```

2. **Créer un Fichier de Configuration**

   Créez un fichier de configuration pour votre application FastAPI dans `/etc/nginx/sites-available/` :
    ```sh
   sudo nano /etc/nginx/sites-available/fastapi
   ```
   Ajoutez la configuration suivante (modifiez `ip_récupéré via wsl hostname -I` avec votre domaine ou adresse IP
   publique) :

   ```nginx
   server {
       listen 80;
       server_name `your_domain_or_ip via whatismyip`;

       location / {
           proxy_pass http://{via wsl hostname -I }:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

2. **Activer la Configuration du Site**

   Créez un lien symbolique dans le répertoire `sites-enabled` :

   ```sh
   sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
   ```

3. **Tester la Configuration Nginx**

   Assurez-vous que votre configuration est correcte :

   ```sh
   sudo nginx -t
   ```

4. **Redémarrer Nginx**

   Redémarrez Nginx pour appliquer les modifications :

   ```sh
   sudo service nginx restart
   ```

#### 3. Configurer WSL pour Autoriser l'Accès Externe

1. **Trouver l'Adresse IP de WSL**

   Exécutez `ip addr` ou `ifconfig` dans votre terminal WSL pour trouver l'adresse IP de l'interface réseau WSL. Cela
   ressemble souvent à `172.x.x.x`.

2. **Configurer la Redirection de Port sur Windows**

   Vous devez configurer Windows pour rediriger les requêtes vers votre instance WSL. Ouvrez une fenêtre de commande
   PowerShell en tant qu'administrateur et exécutez la commande suivante :

   ```powershell
   netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=<adresse IP machine Linux>
      ```

   Remplacez `<WSL_IP>` par l'adresse IP de votre interface WSL trouvée précédemment.

3. **Configurer le Pare-feu Windows**

   Ouvrez les ports nécessaires dans le pare-feu Windows :

   ```powershell
   New-NetFireWallRule -DisplayName 'WSL 2' -Direction Outbound -LocalPort "8000" -Action Allow -Protocol TCP
   New-NetFireWallRule -DisplayName 'WSL 2' -Direction Inbound -LocalPort "8000" -Action Allow -Protocol TCP
   ```

#### 4. Tester l'Accès Externe

Accédez à votre application en utilisant votre adresse IP publique (ou le nom de domaine si vous en avez configuré un)
depuis un navigateur web :

```
http://your_domain_or_ip:8000/classify/
```

# Executer le serveur
## installer uvicorn
`pip install uvicorn`
## Executer : 
verifier que le fichier `deep_woke\ml\ml_core\data\embedding_data\cc.fr.300.bin` (ou autre embedding data) est bien
présent

`./run.sh`


# Requête : 
envoyer une requête via une methode post :
```http request
POST http://{outside_ip}:8000/classify/
accept: application/json
Content-Type: application/json

{
"text": "cette femme est une méchante"
}
```

