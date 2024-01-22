# il database cassaforte.db contriene 2 table : 
# - credentials(name[pk], password) 
# - access_list(date_time[pk], user_name [che è una chiave esterna])


#codice che sceglie quanti utenti ci sono, a ognuno assegna una password diversa e lo assegna alla cassaforte, se si apre, tiene conto di chi lha aperta
import random
import sqlite3
import datetime
import hashlib
import time

db_path = 'cassaforte_fissa.db'
tentativi_errati = 0
tentativi_massimi = 3
tempo_blocco = 10 #secondi

def access_writer(password):
    try:
        #connessionme al database
        conn = sqlite3.connect(db_path)
        # Creazione di un cursore per eseguire le operazioni SQL
        cursor = conn.cursor()
        #selezione dal database il nome dell'utente corrispondente alla password
        cursor.execute('SELECT name FROM credentials WHERE password = ?', (password,))
        username = cursor.fetchone()
        username = username[0]
        
        data_ora_correnti = datetime.datetime.now()
        data_ora_formattate = data_ora_correnti.strftime("%Y-%m-%d %H:%M:%S")
        data_ora_formattate = str(data_ora_formattate)

        # aggiungo l'accesso nella tabella access_list
        cursor.execute('INSERT INTO access_list (date_time, user_name) VALUES (?,?)',(data_ora_formattate,username))

        # Commit delle modifiche
        conn.commit()

        # Chiusura del cursore e della connessione al database
        cursor.close()
        conn.close()

    except sqlite3.Error as e:
        print(f"Errore durante la scrittura nel database: {e}")


def enter_password():
 
    password = str(input("Inserisci password: "))

    hash = password.encode('utf-8')
    hash = hashlib.sha256(hash).hexdigest()[:16]

    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()

    # Esempio di query di selezione per verificare la presenza della variabile nella colonna hash
    cursor.execute('SELECT name FROM credentials WHERE hash = ?', (hash,))

    # Recupero della prima riga restituita dalla query
    riga = cursor.fetchone()

    # Chiusura del cursore e della connessione al database
    conn.commit()
    cursor.close()
    conn.close()

    # Verifica se la variabile è presente nella colonna1
    if riga:               
        print("🟢")
        access_writer(password)
        tentativi_errati = 0
    else:
        print("🔴")
        tentativi_errati += 1
        if tentativi_errati >= tentativi_massimi :
            tentativi_errati = 0
            allarme()
        



def add_user():# QUESTA FX SERVE AD AGGUNGERE NUOVI UTENTI A CUI ASSEGNARE UNA PSK FISSA

    while True:
        try:
            nuovo_personale = int(input("Inserire il numero di utenti alla quale assegnare password fissa: "))
            print(f"Aggiunta di {nuovo_personale} utenti...")
            break
        except ValueError:
            print("inserire un numero!")

        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _ in range(nuovo_personale):  # Utilizziamo range() per iterare per il numero specificato di credenziali

        while True:
            username = input("Inserire nome: ")
            username = username.upper()
            cursor.execute('SELECT name FROM credentials')
            usernames = cursor.fetchone()
            if usernames is None or username not in usernames:
                break
            else:
                print("ID utente già esistente ")

        #generazione di codici unici NON RIPETIBILI
        while True:
            random_code = [random.randint(0, 9) for _ in range(6)]
            password = ''.join(map(str, random_code))
            hash = password.encode('utf-8')
            hash = hashlib.sha256(hash).hexdigest()[:16]
            
            cursor.execute('SELECT password FROM credentials')
            passwords = cursor.fetchone()
            if passwords is None or password not in passwords:
                # inserisci in dizionario password
                break
        
        print(f" nome : {username} \n password : {password} \n hash : {hash}")
        try:
            cursor.execute('INSERT INTO credentials(name,hash, password) VALUES(?,?,?)',(username, hash, password ))
            conn.commit()
        except sqlite3.IntegrityError as e:
            # Gestisci l'eccezione per la violazione di unicità
            if "UNIQUE constraint failed: credentials.name" in str(e):
                print(f"Errore: Il nome utente '{username}' è già presente nel database.")
            else:
                print(f"Errore durante l'inserimento dell'utente: {e}")

    cursor.close()
    conn.close()
    


def delete_user():
    delete = input("inserisci il nome utente che desideri rimuovere: ")
    delete = delete.upper()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Esegui la query e ottieni i risultati
    cursor.execute('SELECT name FROM credentials WHERE name = ?', (delete,))
    result = cursor.fetchone()

    if result:
        # Se il nome utente esiste, esegui la cancellazione
        cursor.execute('DELETE FROM credentials WHERE name = ?', (delete,))
        print(f'Il nome utente {delete} è stato rimosso con successo.')
    else:
        print('Il nome utente inserito non esiste.')

    conn.commit()
    cursor.close()
    conn.close()
    

def allarme():
    #mandare avviso alla reception
    print("allarme")
    #blocco tot secondi
    print(f"Troppi tentativi errati. Attendi {tempo_blocco} secondi.")
    time.sleep(tempo_blocco)
    print("Blocco terminato. Ritenta l'accesso.")



while True:

    # if cassaforte aperta:
    #     print("chiudere sportello")
    # else:

    scelta= input("""
        DI QUALE FUNZIONE HAI BISOGNO
          1. Accesso alla cassaforte
          2. Aggiunta di utenti
          3. Rimozione di utenti
        
        """)
    if scelta == "1":
        enter_password()
    elif scelta == "2":
        add_user()
    elif scelta == "3":
        delete_user()
    else:
        print("scelta non valida")
