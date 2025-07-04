Istruzioni per l'utilizzo

Il sistema prevede 4 livelli di accesso differenti, ognuno con la relativa vista: commesso, magazziniere, responsabile commerciale e amministratore.
Avviando il programma dal file main.py si aprirà una finestra di login dove è possibile accedere ad uno di questi 4 livelli, digitando il codice utente collegato all'account utente.
Se non si dispone di un account utente è possibile registrasti cliccando "Registrati", dove nell'apposita finestra è necessario inserire il proprio nome e cognome e ruolo di registrazione.
Cliccando il bottone registrati verrà creato l'account utente e verrà anche fornito il codice utente utile per il login al sistema.
In ogni vista è possibile eseguire il logut cliccando nel menù in alto a sinistra dove oltre alle informazioni dell'account è presente il bottone "Logout"


Le attività che un utente loggato come "COMMESSO" può eseguire, sono quelle di inserimento di una nuova vendita e modifica di una vendita già presente all'interno del db.
Per inserire una nuova vendita è necessario digitare nell'apposito form lo SKU, che deve essere valido e presente all'interno del db articoli, la quantità della vendita, e il paese di vendita dall'apposito menù. Qualora uno di questi campi non soddisfi i requisiti viene mostrato un alert di errore. (es: 687YP, 15, Italia)
Per modificare una vendita è necessario digitare nell'apposito form l'ID della vendita, che deve essere valido per una vendita e presente all'interno del db operazioni, lo SKU, la quantità, e il paese. Se non è necessario modificare tutti i campi basterà lasciarli vuoti, qualora uno di questi campi non soddisfi i requisiti viene mostrato un alert di errore. (es: 2, 734NX, 15, Italia) (es 2: 3, *CAMPO SKU VUOTO, 20, **CAMPO PAESE VUOTO*)


Le attività che un utente loggato come "MAGAZZINIERE" può eseguire, sono quelle di inserimento di una nuova giacenza e modifica di una giacenza già presente all'interno del db.
Per inserire una nuova giacenza è necessario digitare nell'apposito form lo SKU, che deve essere valido e presente all'interno del db articoli e la quantità della giacenza. Qualora uno di questi campi non soddisfi i requisiti viene mostrato un alert di errore. (es: 687YP, 15)
Per modificare una giacenza è necessario digitare nell'apposito form l'ID della giacenza, che deve essere valido per una giacenza e presente all'interno del db operazioni, lo SKU e la quantità. Se non è necessario modificare tutti i campi basterà lasciarli vuoti, qualora uno di questi campi non soddisfi i requisiti viene mostrato un alert di errore. (es: 1, 734NX, 15) (es 2: 91, *CAMPO SKU VUOTO*, 20)

Le attività che un utente loggato come "RESPONSABILE COMMERCIALE" può eseguire, sono quelle di visualizzazione del grafico con vendite mensili totali, giacenza media mensile e indice di rotazione mensile. Inoltre su questi dati mostrati possono essere applicati dei filtri per Genere, Tipologia, Sku, e Paese, che si trovano nella bara sopra al grafico. Per visualizzare i dati filtrati è sufficiente cliccare il bottone "Applica Filtri"

Infine le attività che un utente "AMMINISTRATORE" può eseguire, oltre a tutte quelle elencate fino ad ora per gli altri livelli di accesso sono quelle di inserimento, modifica ed eliminazione di articolo all'interno del db articoli.
Per inserire o modificare un nuovo articolo è necessario inserire nell'apposito form lo SKU, il genere dell'articolo, e la tipologia con le stesse modalità precedentemente descritte.
Per l'eliminazione invece è sufficiente digitare nell'apposito form lo SKU, che deve essere presente all'intero del db articoli.
