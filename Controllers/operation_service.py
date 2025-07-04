from typing import List, Dict, Any


def calcolaVenditeTotali(lista_operazioni: List[Dict[str, any]]) -> List[int]:
    """Calcola le vendite totali per ogni mese dell'anno"""

    vendite_totali = [0] * 12

    for op in lista_operazioni:
        if op['vendita'] > 0:
            mese = op['data'].month - 1
            vendita = op['vendita']
            vendite_totali[mese] += vendita

    return vendite_totali

def ordinamentoOperazioni(lista_operazioni: List[Dict[str, any]], mese_set):
    """Le operazioni vengono ordinate in base alla data"""

    if mese_set == 2:
        giorni_mese = 28
    elif mese_set in {1, 3, 5, 7, 8, 10, 12}:
        giorni_mese = 31
    else:
        giorni_mese = 30

    operazioni_ordinate = [0] * giorni_mese

    for op in lista_operazioni:
        data_op = op['data']

        mese_op = int(data_op.strftime("%m"))
        giorno_op = int(data_op.strftime("%d"))

        if mese_op != mese_set:
            continue

        if giorno_op < 1 or giorno_op > giorni_mese:
            continue

        operazioni_ordinate[giorno_op - 1] += op['giacenza']

    return operazioni_ordinate

def giacenzaMediaMensile(operazioni_ordinate, mese_set) -> List[int]:
    """metodo per il calcolo della giacenza media mensile"""

    totale=0
    somma_corrente=0
    media_round=0

    if mese_set == 2:
        giorni_mese = 28
    elif mese_set in {1, 3, 5, 7, 8, 10, 12}:
        giorni_mese = 31
    else:
        giorni_mese = 30

    for i in range(giorni_mese):
        elemento_corrente = operazioni_ordinate[i]
        if elemento_corrente != 0:
            ultimo_valore = elemento_corrente
            somma_corrente+=ultimo_valore
        totale+=somma_corrente

        media=totale/giorni_mese
        media_round=round(media,2)
    return media_round

def indiceRotazione(vendite_totali, media_round):
    """metodo per il calcolo del'indice di rotazione mensile'"""
    indice_rotazione_round=[0]*12

    for i in range(12):
        indice_rotazione=vendite_totali[i]/media_round[i]
        indice_rotazione_round[i]=round(indice_rotazione, 2)
    return indice_rotazione_round

def filtroSKU(lista_operazioni: List[Dict[str, any]], sku_list: List[str]) -> list[dict[str, Any]]:
    """metodo per filtrare le operazioni tramite sku"""

    if not sku_list:
        return lista_operazioni

    sku_set = set(sku_list)
    return[op for op in lista_operazioni if op['sku'] in sku_set]

def filtroGenere(lista_operazioni: List[Dict[str, any]], lista_articoli: List[Dict[str, any]], generi: List[str]) -> List[Dict[str, any]]:
    """metodo per filtrare le operazioni per genere"""

    if not generi:
        return lista_operazioni

    test = []

    for art in lista_articoli:
        if art['genere'] in generi:
            test.append(art['sku'])

    return [op for op in lista_operazioni if op['sku'] in test]

def filtroTipologia(lista_operazioni: List[Dict[str, any]], lista_articoli: List[Dict[str, any]], tipologie: List[str]) -> List[Dict[str, any]]:
    """metodo per filtrare le operazioni per tipologia"""

    if not tipologie:
        return lista_operazioni

    test = []

    for art in lista_articoli:
        if art['tipologia'] in tipologie:
            test.append(art['sku'])

    return [op for op in lista_operazioni if op['sku'] in test]

def filtroZona(lista_operazioni: List[Dict[str, any]], zone: List[str]) -> list[dict[str, Any]]:
    """metodo per filtrare le operazioni per zona"""


    if not zone:
        return lista_operazioni

    zone_set = set(zone)
    return[op for op in lista_operazioni if op['paese'] in zone_set or op['paese'] == "Brancadoro"]

def filtraOperazioni(lista_operazioni: List[Dict[str, any]],
                     lista_articoli: List[Dict[str, Any]],
                     sku: List[str] = None,
                     generi: List[str] = None,
                     tipologie: List[str] = None,
                     zone: List[str] = None
                     ) -> List[Dict[str, any]]:
    """metodo utilizzato per scegliere quali dati filtrati visualizzare nel grafico"""
    filtrate = lista_operazioni

    if sku != ['']:
        filtrate = filtroSKU(filtrate, sku)
    if generi != [' ']:
        filtrate = filtroGenere(filtrate, lista_articoli, generi)
    if tipologie != [' ']:
        filtrate = filtroTipologia(filtrate, lista_articoli, tipologie)
    if zone != [' ']:
        filtrate = filtroZona(filtrate, zone)

    return filtrate
