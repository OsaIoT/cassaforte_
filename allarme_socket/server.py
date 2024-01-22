import socket
import pickle

# Creazione di un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Indirizzo e porta del server
server_socket.listen(1)  # Numero massimo di connessioni in attesa

print("In attesa di connessioni...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connessione accettata da {client_address}")

        try:
            data = client_socket.recv(4096)
            if not data:
                break  # Se non ci sono dati, la connessione è stata chiusa dal client

            dati_utente = pickle.loads(data)
            print(f"Dati ricevuti dal client: {dati_utente}")

        except pickle.UnpicklingError as e:
            print(f"Errore durante il deserializzazione dei dati: {e}")

        finally:
            client_socket.close()

except KeyboardInterrupt:
    print("Server interrotto manualmente.")

finally:
    server_socket.close()
