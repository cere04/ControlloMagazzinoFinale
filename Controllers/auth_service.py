from entities.utente import get_utente_by_id, letturaDatabaseUtenti

class AuthService:

    def loginUtente(self, id) -> dict:
        """Esegue il login con il codice dipendente e restituisce un dizionario con i dati utente"""
        lista_utenti = letturaDatabaseUtenti("Model/databaseUtenti.txt")
        utente = get_utente_by_id(id, lista_utenti)

        if utente:
            return utente
        else:
            return None

    def aggiungiUtenti(self, nome, cognome, ruolo) -> str:
        """Aggiunge un nuovo utente al sistema e restituisce il codice utente generato"""
        if nome == '' or cognome == '':
            return None
        else:
            with open("Model/databaseUtenti.txt", "r") as file1:
                lines = file1.readlines()
                n = len(lines) + 1  # Numero progressivo basato sul numero di righe

            cu = f"{nome[0]}.{cognome}{n}{ruolo[0]}"
            with open("Model/databaseUtenti.txt", "a") as file:
                file.write(f"\n{nome}, {cognome}, {ruolo}, {cu}")
            return cu