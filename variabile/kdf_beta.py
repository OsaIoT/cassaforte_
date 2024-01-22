#script contenente crittografia e gestione password
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
file_path = "kdf.txt"
tentativi_errati=0

def generate_key(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  # Genera un salt casuale di 16 byte

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Lunghezza della chiave in byte
        salt=salt,
        iterations=100000,  # Numero di iterazioni
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt    

# Scrive le variabili in un file txt
def scrivi_su_file(file_path, *dati):
    with open(file_path, 'w') as file:
        for dato in dati:
            file.write(str(dato)+ '\n')


# Leggere variabili da un file txt e restituire una tupla
def leggi_da_file(file_path):
    with open(file_path, 'r') as file:
        contenuto = file.read().splitlines()

        return tuple(contenuto)


def verifica_password(password_inserita, saved_key, saved_salt):
    chiave_inserita, _ = generate_key(password_inserita, saved_salt)
    return chiave_inserita == saved_key

def kdf_chiusura():
    
    while True:
        # registrazione di un nuovo utente
        password_chiusura = input("Inserire una password di chiusura: ")
        if len(password_chiusura) <= 6 and len(password_chiusura)>=4:
            print("chiusura effettuata con successo")
            break
        else: 
            print("la password deve contenere dai 4 ai 6 caratteri")

    
    chiave_derivata, salt_generato = generate_key(password_chiusura)


    #Scrittura password crittografata e hash su file txt
    scrivi_su_file(file_path, chiave_derivata.decode(),base64.urlsafe_b64encode(salt_generato).decode())


def kdf_apertura():
    global tentativi_errati
    #prelievo password crittografata e hash da file txt
    # Leggere variabili da un file txt e restituire una tupla
    saved_key, saved_salt = leggi_da_file(file_path)



    # Converti la stringa in bytes utilizzando base64
    saved_key = saved_key.encode()
    saved_salt = base64.urlsafe_b64decode(saved_salt)

    # Simuliamo il processo di verifica dell'utente
    password_apertura = input("Inserisci la password per l'apertura: ")
    if verifica_password(password_apertura, saved_key, saved_salt):
        print("🟢Accesso consentito🟢")
        tentativi_errati = 0
        sportello = 0
        mod_apertura = "user"
        return tentativi_errati, sportello,mod_apertura
    else:
        print("🔴Accesso negato🔴")
        tentativi_errati +=1
        sportello = 1
        mod_apertura = "user"
        return tentativi_errati, sportello,mod_apertura


