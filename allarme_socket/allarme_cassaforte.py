import socket
import pickle

try:
    # Creazione di un socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connessione al server
        server_address = ('172.17.2.27', 12345)  # Sostituisci con l'indirizzo e la porta del tuo server
        client_socket.connect(server_address)

        # Dati da inviare al server
        allarme = True

        # Invio dei dati al server
        data = pickle.dumps(allarme)
        client_socket.sendall(data)

except Exception as e:
    print(f"Errore durante la connessione o l'invio dei dati: {e}")
