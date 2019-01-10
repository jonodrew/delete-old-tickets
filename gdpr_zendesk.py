import requests, csv
from datetime import timedelta, datetime
from urllib.parse import urlencode

def get_next_page(url, user, pwd):
    response = requests.get(url, auth=(user, pwd))
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()
    else:
        return response.json()

def delete_ticket(ticket, user, pwd):
    id = ticket['id']
    ticketurl = ticket['url']
    updated = ticket['updated_at']
    print("ticket id: {}".format(id))
    print("Ticket last updated: {}".format(updated))

    #delete the ticket from Zendesk
    requests.delete(ticketurl, auth=(user, pwd))

def delete_all(user, pwd, soft_delete=True):
    """
    This function deletes all the old tickets. The soft_delete argument is a
    boolean, so you pass it a True or False. It defaults to True, so if you
    forget to set it it only soft deletes the tickets.
    """
    if soft_delete:
        fourth_column = "deleted"
        filename = "oldtickets"
        date_ago = datetime.now() - timedelta(days=1095)  # 1095 is three years
        # put date into "YYYY-MM-DD" format
        date=(date_ago.strftime("%Y-%m-%d"))
        params = {'query': 'type:ticket solved<{}'.format(date)}
        url = "https://cabinetoffice.zendesk.com/api/v2/search.json?query={}".format(urlencode(params))
    else:
        fourth_column = "hard-deleted"
        filename = "hard_delete"
        url = "https://cabinetoffice.zendesk.com/api/v2/deleted_tickets.json"
    data = get_next_page(url, user,pwd)
    while data['next_page'] != "null":
        for ticket in data['results']:
            delete_ticket(ticket, user, pwd)
            #write ticket ids and dates to csv for records
            row = [id, ticketurl, updated, fourth_column]
            with open(f'{filename}{datetime.now()}.csv', 'a') as output_file:
                writer = csv.writer(output_file)
                writer.writerow(row)

        #find the next url to pull tickets from
        url=data['next_page']
        data = get_next_page(url, user, pwd)
