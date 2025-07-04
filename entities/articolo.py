from entities.operazione import letturaDatabaseArticoli
from entities.enums import TipologiaArticolo, GenereArticolo


class Articolo:
    def __init__(self,
                 sku = None,
                 tipologia = TipologiaArticolo,
                 genere = GenereArticolo
                 ):
        self.sku = sku
        self.tipologia = tipologia
        self.genere = genere

    def aggiungiArticolo(self):
        """metodo per l'aggiunta di un nuovo articolo nel database articoli"""

        lista_articoli=letturaDatabaseArticoli("Model/databaseArticoli.txt")

        controllo_sku=False

        for riga in lista_articoli:
            if self.sku in riga['sku']:
                controllo_sku=True
            else:
                controllo_sku=False

        if controllo_sku is False:
            with open("Model/databaseArticoli.txt", "a") as file:
                file.write(f"\n{self.sku}, {self.genere}, {self.tipologia}")
            print("Articolo aggiunto")
        else:
            print("errore articolo gia esistente")

    def modificaArticolo(self, sku_set, genere, tipologia):
        """metodo per la modifica di un articolo presente all'interno del database articoli"""

        lista_articoli = letturaDatabaseArticoli("Model/databaseArticoli.txt")
        articolo_trovato = False

        for art in lista_articoli:
            if art['sku'] == sku_set:

                articolo_trovato = True

                if genere is not None:
                    art['genere'] = genere

                if tipologia is not None:
                    art['tipologia'] = tipologia

            lines=[]
            for art1 in lista_articoli:
                line = (
                    f"{art1['sku']}, "
                    f"{art1['genere']}, "
                    f"{art1['tipologia']}"
                )
                lines.append(line)

            try:
                with open("Model/databaseArticoli.txt", 'w') as file:
                    file.write("\n".join(lines))
            except Exception as e:
                raise RuntimeError(f"Errore salvataggio database: {str(e)}")

        if not articolo_trovato:
            raise ValueError(f"SKU articolo {sku_set} non trovato")

    def eliminaArticolo(self, sku_set):
        """metodo per l'eliminazione di un articolo presente all'interno del database articoli"""

        lista_articoli=letturaDatabaseArticoli("Model/databaseArticoli.txt")

        lista_articoli_new=[]
        for art in lista_articoli:
            if art['sku'] == sku_set:
                lista_articoli_new = [riga for riga in lista_articoli if sku_set not in riga['sku']]

            lines=[]
            for art1 in lista_articoli_new:
                line=(
                    f"{art1['sku']}, "
                    f"{art1['genere']}, "
                    f"{art1['tipologia']}"
                )
                lines.append(line)

            try:
                with open("Model/databaseArticoli.txt", 'w') as file:
                    file.write("\n".join(lines))
            except Exception as e:
                raise RuntimeError(f"Errore salvataggio database: {str(e)}")
