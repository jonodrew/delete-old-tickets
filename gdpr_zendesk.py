import requests, csv
from datetime import timedelta, datetime
from urllib.parse import urlencode


#work out date three years ago or 1095 days ago

Ndays = 1095
date_ago = datetime.now() - timedelta(days=Ndays)

print("The date today is {}".format(datetime.now()))

# put date into "YYYY-MM-DD" format
date=(date_ago.strftime("%Y-%m-%d"))
print("Gathering records from before: {}".format(date))

# Access API with search criteria

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

### this works below!
# The below code pulls ticket ids and the last updated dates of all tickets older than the date specified in the API search above
# and places in a csv file.
def soft_delete(user, pwd, date):
    """
    This function does a "soft delete". The ticket is marked as deleted, but
    still exists in Zendesk.
    """
    params = {'query': 'type:ticket solved<{}'.format(date)}
    url = "https://cabinetoffice.zendesk.com/api/v2/search.json?query={}".format(urlencode(params))
    data = get_next_page(url, user, pwd)
    #while loop to proceed through pages of tickets pulled from API
    while data['next_page'] != "null":
        for ticket in data['results']:
            delete_ticket(ticket, user, pwd)
            #write ticket ids and dates to csv for records
            row = [id, ticketurl, updated, "deleted"]
            with open('oldtickets {}.csv'.format(datetime.now()), 'a') as oldtickets:
                writer = csv.writer(oldtickets)
                writer.writerow(row)

        #find the next url to pull tickets from
        url=data['next_page']
        data = get_next_page(url, user, pwd)
    return True

#Permanently/hard delete tickets from the API

def hard_delete(user, pwd):
    durl = "https://cabinetoffice.zendesk.com/api/v2/deleted_tickets.json"

    ddata = get_next_page(durl, user, pwd)

    #while loop to proceed through pages of deleted tickets pulled from API
    while ddata['next_page'] != "null":
        for ticket in ddata['deleted_tickets']:
            delete_ticket(ticket, user, pwd)

             #write ticket ids and dates to csv for records
            row = [did, dticketurl, deleted, "hard-deleted"]
            with open('harddelete {}.csv'.format(datetime.now()), 'a') as harddelete:
                writer = csv.writer(harddelete)
                writer.writerow(row)

        #find the next url to pull tickets from
        durl=ddata['next_page']

        #Go to next page of tickets
        get_next_page(durl, user, pwd)
        #repeat - go back to begnning of loop for next page of tickets
