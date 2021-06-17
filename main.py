import requests
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup as bs
import json
import time

def sistema_orario(orario):
    """returna l'orario in formato corretto
    """
    orario = orario.replace(' ', '')
    return orario

def quando(orari, preferenza='primo'):
    """seleziona il primo o l'ultimo orario disponibile
       in base alla preferenza indicata.
    """
    if preferenza == 'primo':
        return orari[0]
    else:
        return orari[-1]

def fixa_path(d, o):
    """genera il path utilizzato per effettuare la prenotazione, il formato è: 20210617150000
                                                                               YYYYmmddhhMM00
    """
    data = ''.join(d.split('-'))
    orario = o.split('-')[0].replace(':', '')
    return f'{data}{orario}00'

with open('first_pay_load.txt') as first, open('last_pay_load.txt') as second, open('ultima_data.txt') as x, open('sedi.txt') as y:
    pay_load = json.load(first)
    confirm_pay_load = json.load(second)
    last = x.readline()
    sedi = json.load(y)

#genera date da oggi all'ultima data indicata come disponibile

last = datetime.strptime(last, '%Y-%m-%d')

today = datetime.now()
delta = timedelta(days = 1)

dates = []

while today <= last:
    dates.append(today.strftime('%Y-%m-%d'))
    today += delta

url = 'https://vaccinicovid.regione.veneto.it/ulss2/azione'


#Mantieni la sessione aperta

with requests.Session() as s:

    #Inserisci codice_fiscale e numero_tessera
    post1 = s.post(f'{url}/controllocf', pay_load)
    print('STEP 1: Codice fiscale e numero di tessera inseriti con successo...')

    #Seleziona il servizio under_50
    post2 = s.post(f'{url}/sceglisede/servizio/704')
    print('STEP2: Selezionato il servizio under_50')

    data_and_sede = False

    while not data_and_sede:

        for sede in sedi:
            post3 = s.post(f'{url}{sedi[sede]}')

            #se la sede non dà errore, ci sono posti disponibili in quella sede
            if not 'alert alert-danger' in post3.text:

                # bruteforce date --> a volte, alcune date segnalate come occupate, in realtà non lo sono.
                # tramite bruteforce troviamo anche quelle.


                today = datetime.now()
                delta = timedelta(days = 1)

                for data in dates:
                    post4 = s.post(f"{url}/getfasce/idata/{data}")
                    time.sleep(0.2) #diamo un po' di respiro al sito
                    if not 'alert alert-danger' in post4.text:
                        data_and_sede = True
                        break
            if data_and_sede:
                break

        print(f'STEP 3: Trovata una data: {data} e una sede: {sede}...')


        #prendiamo l'orario in base alla preferenza indicata (primo/ultimo disponibile)
        #atm non è configurabile, prende solo il primo disponibile

        soup = bs(post4.text, 'html.parser')
        link = soup.find_all(class_='btn btn-primary btn-full')
        orari_disponibili = [sistema_orario(l.text) for l in link]

        orario = quando(orari_disponibili)

        res = fixa_path(data, orario)

        #adda ad ultimo payload
        confirm_pay_load['data'] = res

    #POST di orario
    post5 = s.post(f'{url}/riepilogo/fascia/{orario}')

    #POST di conferma prenotazione e invio dati: path data, nome, cognome, email, cellulare
    post6 = s.post(f'{url}/faiprenotazione', confirm_pay_load)

    #per debug: salva testo della pagina dopo la prenotazione e lo salva
    with open('risultato.txt', encoding = 'utf-8') as f:
        f.write(post6.text)

    del confirm_pay_load['data']

    print(f'Effettuata una prenotazione:\n\nSEDE: {sede.capitalize()}\nGIORNO: {data}\nORARIO: {orario}\n\ncon i seguenti dati:{confirm_pay_load}\n')
    print(f'Per conferma della prenotazione attendi una mail da noreply.vaccinicovid@regione.veneto.it')