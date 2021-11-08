from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json

def get_free_ticket_sympla(event_url, first_name, last_name, email):

    session = HTMLSession()

    headers = {
        'authority': 'www.sympla.com.br',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    sympla = BeautifulSoup(session.get(event_url, headers=headers).text, 'html.parser')
    
    inscricao_url = sympla.find('form').get('action')
    
    for script_tag in sympla.find_all('script', {"type":"text/javascript"}):
        if script_tag.string and "lista-de-ingressos" in script_tag.string:
            event_details = script_tag.string

    available_tickets = event_details.split("_tracking_callback(")

    prices = []
    for i in range(1, len(available_tickets)):
        dict_elements = available_tickets[i].split(");")[0].splitlines()
        single_ticket = json.loads(''.join([el.replace(" ","") for el in dict_elements if el.replace(" ","")]).replace("'", '"'))

        prices.append({'id': single_ticket['ecommerce']['impressions'][0]['id'], 
                       'price': single_ticket['ecommerce']['impressions'][0]['price']})
        
    for p in prices:
        if p['price'] == '0.00':
            free_ticket_id = p['id']
            
    data = {
      f'ddlQuant_{free_ticket_id}': '1'
    }

    ticket = BeautifulSoup(session.post(inscricao_url, headers=headers, data=data).text, 'html.parser')
    
    data = {
      'YII_PAGE_STATE': ticket.find('input', {'name': 'YII_PAGE_STATE'}).get('value'),
      'customFormField_eid': ticket.find('input', {'name': 'customFormField_eid'}).get('value'),
      'customFormField_total': '1',
      'customFormField_firstName[0]': first_name,
      'customFormField_lastName[0]': last_name,
      'customFormField_Email[0]': email,
      'ddlCopyFrom': '0',
      'FreeOrder[FIRST_NAME]': first_name,
      'FreeOrder[LAST_NAME]': last_name,
      'FreeOrder[EMAIL]': email,
      'FreeOrder[confirmEmail]': email,
      'FreeOrder[step]': 'step1',
      'FreeOrder[createReservation]': '',
      'FreeOrder[reservationId]': ticket.find('input', {'name': 'FreeOrder[reservationId]'}).get('value'),
      'FreeOrder[paymentType]': ticket.find('input', {'name': 'FreeOrder[paymentType]'}).get('value'),
      'FreeOrder[IP_ADDRESS]': ticket.find('input', {'name': 'FreeOrder[IP_ADDRESS]'}).get('value'),
      'FreeOrder[DEVICE]': ticket.find('input', {'name': 'FreeOrder[DEVICE]'}).get('value'),
      'FreeOrder[DEVICE_BRAND]': ticket.find('input', {'name': 'FreeOrder[DEVICE_BRAND]'}).get('value')
    }

    response = session.post(inscricao_url, headers=headers, data=data, allow_redirects=False)
    success = session.get(response.headers['Location'])
    return None
