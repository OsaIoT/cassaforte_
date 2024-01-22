
import sqlite3
import datetime
import time
import datetime
from kdf_beta import kdf_apertura, kdf_chiusura

tentativi_errati = 0
tentativi_massimi = 3
mod_apertura = "user"

#NEL DATABASE ACCESSI AGGIUNGI COLONNA PER MODALITA APERTURA = USER, KEY, RECEPTION

# per la comunicazione tra la web app e i Raspberry Pi. Puoi utilizzare richieste (HTTP o) WebSocket = WEBSOCKET  con pickle (utilizzata per convertire i dati dell'utente in un formato che può essere inviato attraverso il socket tra il client e il server).
# A WEBSOCKET DEVI GESTIRE GLI ERRORI: SE LA RETE è DOWN TUTTI I LOG VENGONO SALVATI IN LOCALE X POI INVIARLI ONLINE
#WEB APP HTTPS O TLS
#SERVER BACKEND SU RASPBERR X ACCETTARE LE RICHIESTE (con flask)
#REGISTRA ANCHE I TENTATIVI FALLITI
#TUTTI I DB DEVONON ESSERE ACCESSIBILI VIA WEBAPP

db_path = 'cassaforte_variabile.db'
tempo_blocco = 10 #secondi
safe_id = "000000"
sportello = 0# da cambiare con if rele chiuso allora = 1 , else 0

def access_writer(sportello):

    # Ottenere la data e l'ora correnti come oggetto datetime
    data_ora = datetime.datetime.now()
    # Estrarre la data e l'ora 
    data_ora_attuale = data_ora.strftime("%Y-%m-%d %H:%M:%S")
    print(data_ora_attuale)
    
    try:
        with sqlite3.connect(db_path) as conn:

            # Creazione di un cursore per eseguire le operazioni SQL
            cursor = conn.cursor()
            
            # aggiungo l'accesso nella tabella access_list
            cursor.execute('INSERT INTO safe_status_log (date_time, safe_id, status, opening_mode) VALUES (?,?,?,?)',(data_ora_attuale,safe_id, sportello, mod_apertura))#aggiungi colonna per tipo aprtura(chiave , reception, codice)

            # Commit delle modifiche
            conn.commit()

    except sqlite3.Error as e:
        print(f"Errore durante la scrittura nel database: {e}")



def allarme():
    #mandare avviso alla reception
    print("allarme")
    #blocco tot secondi 
    print(f"Troppi tentativi errati. Attendi {tempo_blocco} secondi.")
    time.sleep(tempo_blocco)
    print("Blocco terminato. Riprova più tardi.")



if __name__ == "__main__":

    while True:
        try:
            if sportello == 0:
                kdf_chiusura()
                #if rele chiusi:
                sportello = 1
                access_writer(sportello)

            else:
                while sportello == 1:
                    tentativi_errati, sportello, mod_apertura= kdf_apertura()
                    access_writer(sportello)
                    if tentativi_errati > tentativi_massimi:
                        allarme()
                    
        except ValueError as e:
            print(e)
            #if rele aperti



