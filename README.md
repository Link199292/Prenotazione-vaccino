# Prenotazione-vaccino

## Disclaimer

*Non mi assumo alcuna responsabilità per l'uso improprio dello script qui pubblicato, né per eventuali esiti infausti causati da un suo utilizzo improprio.*

*controllate 1000 volte i dati inseriti nei files*, in particolar modo la mail: una volta che la prenotazione è andata a buon fine, non c'è più nulla da fare, se malauguratamente la mail inserita è sbagliata e per una qualsiasi ragione avete intenzione di spostare la prenotazione, non avete più modo di cancellarla, se non chiamando il numero verde.
Altre informazioni errate non causano problemi, semplicemente lo script non funzionerà come dovrebbe.

## Scopo

Questo script permette di effettuare una prenotazione per il vaccino, in maniera automatica.
E' stato programmato per funzionare solo per l'**aulss2** e solo per gli **under_50**.

## Files

- **first_pay_load.txt**: su cod_fiscale va inserito il codice fiscale, su num_tessera le ultime 6 cifre del numero di identificazione della tessera.
- **last_pay_load.txt**: qui vanno inserite le informazioni personali, tramite cui verrà generata la prenotazione (Cognome, Nome, Email, Cellulare).
Mi ripeto: *controllate 1000 volte la mail inserita* e in generale i dati inseriti.
- **sedi.txt**: contiene le informazioni necessarie per trovare le sedi disponibili. Eliminando una (o più) coppia di chiave e valori è possibile restringere il campo di ricerca per le sedi disponibili, così da cercare una prenotazione per le sole sedi desiderate.
Ad esempio:
{
    "VILLORBA" : "/sceglidata/sede/52"
}

un file impostato in questo modo cercherà date disponibili solo per la sede di Villorba.

- **ultima_data.txt**: inserendo, nella prima linea, una data nel formato 'YYYY-MM-DD' sarà possibile selezionare una soglia per le date ricercate (e.g. inserendo '2021-8-31, cercherà date disponibili a partire da oggi, fino al 31 agosto, incluso).
