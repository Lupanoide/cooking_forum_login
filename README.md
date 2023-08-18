Per testare il servizio:

# Creare l'immagine:

- `docker build -t "cooking_forum:1.0" .`

Per far girare l'applicazione. La mia applicazione si appoggia su un database postgres. Per una migliore integrazione ho deciso di deployare con docker-compose. Per tirare su l'istanza

- `docker-compose up`

E attendere il completamento della fase di creazione. Ora sarà possibile, in quanto i servizi sono sviluppati con FASTAPI, la documentazione in formato Open Api al seguente indirizzo:

- `http://localhost:8000/docs`

e

- `http://localhost:8000/docs`

**Sono stati creati 4 endpoint:**
 - `/signup` un servizio **POST** per la registrazione di nuovi utenti, in  cui è possibile abilitare l'autenticazione a due fattori
 - `/login` un servizio **POST** per il login degli utenti, è anche l'unico disponibile per coloro che non hanno abilitato l'autenticazione a due fattori. Restituisce un JWT
- `/generate_otp` un servizio **POST** con cui è possibile richiedere una one time password
- `/validate_otp` un servizio **POST** che permette la validazione della one time password generata dal servizio `/generate_otp`

# Chiamare gli endpoint

 Per chiamare gli endpoint è possibile usare la libreria `requests` di python. Aprire un interprete e importare la libreria:
 
 `import  requests`

**Creare un nuovo utente senza abilitare l'autenticazione a due fattori:**

`r = requests.post("http://localhost:8000/signup", json={"username": r"michele_lupo@gmail.it", "password": "pappappero", "name": "Michele", "surname": "Lupo"})`

**Fare il login  dell'utente appena creato**

`r = requests.post("http://localhost:8000/login", json={"username": r"michele_lupo@gmail.it", "password": "pappappero"})`

**Creare un nuovo utente, abilitando l'autenticazione a due fattori**

`r = requests.post("http://localhost:8000/signup", json={"username": r"lupanoide@yahoo.it", "password": "123456", "name": "Michele", "surname": "Lupo", "two_factors_login_enabled": True})`

**Richiedere una OTP per l'utente appena creato**

`r = requests.post("http://localhost:8000/generate_otp", json={"username": r"lupanoide@yahoo.it"})`

Ora occorre intercettare la otp nei log dell'applicazione. È necessario andare nella scheda del terminale con cui si è lanciato il docker compose e trovare una linea come questa:

`Your one time password is: znUag2T7. It will be active only for 5 minutes`

**Per validare la otp occorre inviarla all'endpoint `validate_otp`**

`r = requests.post("http://localhost:8000/validate_otp", json={"username": r"lupanoide@yahoo.it", "otp": "znUag2T7"})`

# Configurare l'ambiente di sviluppo in locale e lanciare i test 

 Chiudere l'applicazione. Per farlo andare nella  scheda del terminale in cui si è lanciato  il comando `docker-compose up` e tirarla giù con `Control+C`. A questo punto sarà possibile rimuovere i container creati dal compose:

`docker-compose down`

Ora è  consigliato creare un python virtual nvironment in cui saranno installate tutte le librerie necessarie. Per farlo creare un venv nella cartella `cooking_forum_login`:

`python -m venv myvenv`

Attivarlo:

`source myvenv/bin/activate`

Installare le dipendenze:

`pip install --upgrade -r requirements.txt`

È necessario cambiare il file di configurazione e inserire quello di test. Per farlo entrare nelle cartelle ./src/conf e aprire il file `config.py`. qui  nella classe config  occorre decommentare la linea 

- `name = os.path.abspath( os.path.join( __file__ , r"../../conf/properties_test.ini"))` 

e commentare la linea 

- `name = os.path.abspath( os.path.join( __file__ , r"../../conf/properties_prod.ini"))`

Ora si può lanciare  un container docker del tutto analogo a quello usato dal compose. Per farlo aprire un'altra scheda del terminale e lanciare: 

`docker run --name postgres --rm -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres  -p 5432:5432 postgres:15-alpine`

L'ambiente di sviluppo è ora pronto. Si possono lanciare i test dalla cartella iniziale del progetto `cooking_forum_login` con `pytest`

`pytest`

