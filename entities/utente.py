from entities.enums import RuoloUtente
from abc import abstractmethod, ABC
from typing import List, Dict, Any


def letturaDatabaseUtenti(nome_file: str)-> List[Dict[str, str]]:
    """metodo per la lettura del database degli utenti"""

    lista_utenti=[]

    try:
        with open(nome_file, 'r') as file:
            n = 0
            for riga in file :
                riga = riga.strip()
                if not riga:
                    continue

                campi=[campo.strip() for campo in riga.split(',')]
                if len(campi)!=4:
                    continue

                lista_utenti.append({
                    'nome': campi[0],
                    'cognome': campi[1],
                    'ruoloUtente': campi[2],
                    'id': campi[3]
                })
    except ValueError as e:
        print(f"Errore conversione dati nella linea {riga}: {e}")
    except Exception as e:
        print(f"Errore durante la lettura del file articoli: {e}")

    return lista_utenti

def get_utente_by_id(id: str, lista_utenti: List[Dict[str, Any]]) -> dict[str, Any] | None:
    """metodo che restituisce tutte le informazioni dell'utente in base al suo id"""

    for utente in lista_utenti:
        if utente['id'] == id:
            return utente
    return None

# class Utente(ABC):
#     def __init__(self,
#                  nome: str,
#                  cognome: str,
#                  codiceDipendente: str,
#                  livelloAccesso: RuoloUtente
#                  ):
#         self.nome = nome
#         self.cognome = cognome
#         self.codiceDipendente = codiceDipendente
#         self.livelloAccesso = livelloAccesso
#
# class Admin(Utente):
#     def __init__(self,
#                  nome: str,
#                  cognome: str,
#                  codiceDipendente : str
#     ):
#         super().__init__(nome, cognome, codiceDipendente, RuoloUtente.ADMIN)
#
#
# class ResponsabileCommerciale(Utente):
#     def __init__(self,
#                  nome:str,
#                  cognome:str,
#                  codiceDipendente:str
#                  ):
#         super().__init__(nome, cognome, codiceDipendente, RuoloUtente.RESPONSABILE_COMMERCIALE)
#
# class Commesso(Utente):
#     def __init__(self,
#                  nome:str,
#                  cognome:str,
#                  codiceDipendente:str
#                  ):
#         super().__init__(nome, cognome, codiceDipendente, RuoloUtente.COMMESSO)
#
# class Magazziniere(Utente):
#     def __init__(self,
#                  nome:str,
#                  cognome:str,
#                  codiceDipendente:str
#                  ):
#         super().__init__(nome, cognome, codiceDipendente, RuoloUtente.MAGAZZINIERE)

