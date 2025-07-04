from enum import Enum

class TipologiaArticolo(Enum):
    CALZATURE = "Calzature"
    BORSE = "Borse"
    ABBIGLIAMENTO = "abbigliamento"

class GenereArticolo(Enum):
    UOMO = "Uomo"
    DONNA = "Donna"
    UNISEX = "Unisex"

class UnitaMisura(Enum):
    PEZZI = "Pezzi"
    PAIA = "Paia"

class RuoloUtente(Enum):
    COMMESSO = "Commesso"
    MAGAZZINIERE = "Magazziniere"
    ADMIN = "Amministratore"
    RESPONSABILE_COMMERCIALE = "Responsabile Commerciale"
    OPERATORE= "Operatore"

class TipoOperazione(Enum):
    VENDITA = "Vendita"
    GIACENZA = "Giacenza"

class Zone(Enum):
    ITALIA = "Italia"
    SPAGNA = "Spagna"
    GERMANIA = "Germania"
    FRANCIA = "Francia"
