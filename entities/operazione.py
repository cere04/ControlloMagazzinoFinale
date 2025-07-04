import os
from datetime import datetime
from typing import List, Dict


def letturaDatabaseArticoli(nome_file: str) -> List[Dict[str, str]]:
    """metodo per la lettura del database degli articoli"""

    lista_articoli = []

    try:
        with open(nome_file, 'r') as file:
            for linea in file:
                linea = linea.strip()
                if not linea:
                    continue

                campi = [campo.strip() for campo in linea.split(',')]
                if len(campi) != 3:
                    continue

                lista_articoli.append({
                    'sku': campi[0],
                    'genere': campi[1],
                    'tipologia': campi[2]
                })

    except ValueError as e:
        print(f"Errore conversione dati nella linea {linea}: {e}")
    except Exception as e:
        print(f"Errore durante la lettura del file articoli: {e}")

    return lista_articoli


def letturaDatabaseOperazioni(nome_file: str) -> List[Dict[str, any]]:
    """metodo per la lettura del database degli articoli"""

    lista_operazioni = []

    if not os.path.exists(nome_file):
        print(f"Errore: il file {nome_file} non esiste")
        return lista_operazioni

    try:
        with open(nome_file, 'r') as file:
            for linea in file:
                linea = linea.strip("\n")
                if not linea:
                    continue

                try:
                    campi = [campo.strip() for campo in linea.split(',')]

                    if len(campi) != 6:
                        print(f"Errore formato nella linea: {linea}")
                        continue

                    operazione = {
                        'sku': campi[0],
                        'vendita': int(campi[1]),
                        'giacenza': int(campi[2]),
                        'paese': campi[3],
                        'data': datetime.strptime(campi[4], '%d-%m-%Y').date(),
                        'idOperazione': int(campi[5])
                    }

                    lista_operazioni.append(operazione)

                except ValueError as e:
                    print(f"Errore conversione dati nella linea {linea}: {e}")
                    continue
                except Exception as e:
                    print(f"Errore processing linea {linea}: {e}")
                    continue

    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")

    return lista_operazioni

class Operazione:
    def __init__(self,
                 id= None,
                 tipo= None,
                 sku= None,
                 quantitaVendita = 0,
                 quantitaGiacenza = 0,
                 paese= None,
                 data = datetime.now(),
    ):

        try:
            self.quantitaVendita = int(quantitaVendita)
        except (ValueError, TypeError):
            self.quantitaVendita = 0

        try:
            self.quantitaGiacenza = int(quantitaGiacenza)
        except (ValueError, TypeError):
            self.quantitaGiacenza = 0

        self.id = id
        self.tipo = tipo
        self.sku = sku
        self.quantitaVendita = quantitaVendita
        self.quantitaGiacenza = quantitaGiacenza
        self.data = data
        self.paese = paese

    def aggiungiVendita(self, sku, quantitaVendita, paese):
        """metodo per l'aggiunta di una vendita al database operazioni"""

        lista_operazioni = letturaDatabaseOperazioni("Model/databaseOperazioni.txt")
        self.id_auto = max(op['idOperazione'] for op in lista_operazioni) + 1 if lista_operazioni else 1
        self.data_formatted = self.data.strftime("%d-%m-%Y")
        line = (
            f"\n{sku}, "
            f"{quantitaVendita}, "
            f"-{quantitaVendita}, "
            f"{paese}, "
            f"{self.data_formatted}, "
            f"{self.id_auto}"
        )
        with open("Model/databaseOperazioni.txt", 'a') as file:
            file.write(line)

    def aggiungiGiacenza(self, sku, quantitaGiacenza):
        """metodo per l'aggiunta di una giacenza al database operazioni"""

        lista_operazioni = letturaDatabaseOperazioni("Model/databaseOperazioni.txt")
        self.id_auto = max(op['idOperazione'] for op in lista_operazioni) + 1 if lista_operazioni else 1
        self.data_formatted = self.data.strftime("%d-%m-%Y")
        line=(
            f"\n{sku}, "
            f"{0}, "
            f"{quantitaGiacenza}, "
            f"Brancadoro, "
            f"{self.data_formatted}, "
            f"{self.id_auto}"
        )
        with open("Model/databaseOperazioni.txt", 'a') as file:
            file.write(line)

    def modificaGiacenza(self, id_set, sku_set, quantitaGiacenza, paese):
        """metodo per la modifica di una giacenza all'interno del database operazioni"""

        lista_operazioni = letturaDatabaseOperazioni("Model/databaseOperazioni.txt")
        operazione_giacenza_trovata= False
        errore_tipo_op = False
        try:
            int(quantitaGiacenza)
        except ValueError:
            quantitaGiacenza = 0

        for op in lista_operazioni:
            if op['idOperazione'] == id_set:
                operazione_giacenza_trovata = True
                if op['vendita'] == 0:
                    errore_tipo_op = True
                    if sku_set != '':
                        op['sku'] = sku_set
                    if quantitaGiacenza != 0:
                        op['giacenza'] = quantitaGiacenza
                    if paese is not None:
                        op['paese'] = paese
                    op['vendita']=0


            lines = []
            for op1 in lista_operazioni:
                data_formatted = op1['data'].strftime('%d-%m-%Y')
                line = (
                    f"{op1['sku']}, "
                    f"{op1['vendita']}, "
                    f"{op1['giacenza']}, "
                    f"{op1['paese']}, "
                    f"{data_formatted}, "
                    f"{op1['idOperazione']}"
                )
                lines.append(line)

            try:
                with open("Model/databaseOperazioni.txt", 'w') as file:
                    file.write("\n".join(lines))
            except Exception as e:
                raise RuntimeError(f"Errore salvataggio database: {str(e)}")

        if not operazione_giacenza_trovata:
            return 'Errore'
        if operazione_giacenza_trovata == True and errore_tipo_op == False:
            return True



    def modificaVendita(self, id_set, sku_set, quantitaVendita, paese):
        """metodo per la modifica di una vendita all'interno del database operazioni"""

        lista_operazioni = letturaDatabaseOperazioni("Model/databaseOperazioni.txt")
        operazione_trovata= False
        tipo_op = False

        try :
            int(quantitaVendita)
        except ValueError:
            quantitaVendita = 0

        sku_set:str
        paese:str

        for op in lista_operazioni:
            if op["idOperazione"] == id_set:
                operazione_trovata = True
                if op['vendita'] != 0:
                    tipo_op = True
                    if sku_set != '':
                        op['sku'] = sku_set
                    if quantitaVendita != 0:
                        op['vendita'] = quantitaVendita
                        op['giacenza'] = '-'+ str(quantitaVendita)
                    if paese != '':
                        op['paese'] = paese

        lines = []
        for op1 in lista_operazioni:
            data_formatted = op1['data'].strftime('%d-%m-%Y')
            line = (
                f"{op1['sku']}, "
                f"{op1['vendita']}, "
                f"{op1['giacenza']}, "
                f"{op1['paese']}, "
                f"{data_formatted}, "
                f"{op1['idOperazione']}"
            )
            lines.append(line)

            try:
                with open("Model/databaseOperazioni.txt", 'w') as file:
                    file.write("\n".join(lines))
            except Exception as e:
                raise RuntimeError(f"Errore salvataggio database: {str(e)}")

        if not operazione_trovata:
            return 'non trovato'
        if operazione_trovata == True and tipo_op == False :
            return True