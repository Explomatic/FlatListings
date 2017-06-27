from bs4 import BeautifulSoup
from urllib import request
import smtplib
from email.mime.text import MIMEText
import sys
import re
import quickstart as qs
import pdb

def fetch_all_listings(url):
    webReq = request.urlopen(url)
    soup = BeautifulSoup(webReq, 'lxml')
    return(soup)

def find_flat_information(soup):
    tags = soup.find_all('td')

    flat_information=[]
    list_title = []
    list_address = []
    list_rooms = []
    list_size = []
    list_rent = []
    list_utility = []
    list_date = []

    itr = 0
    for tag in tags:
        try:
            if tag.a['class'][0] == "advertLink":
                tagCenter = 0
                tagRight = 0
                list_title += [str(tag.a['title'])]
                list_address += [extract_address(tag)]
        except Exception as e:
            pass

        try:
            if "center" in tag['style'] and tagCenter < 2:
                if tagCenter == 0:
                    list_rooms += [extract_rooms(tag)]
                else:
                    list_size += [extract_size(tag)]

                tagCenter += 1
        except Exception as e:
            pass

        try:
            if "right" in tag['style'] and tagRight < 2:
                if tagRight == 0:
                    rent, utility = extract_rent_and_utility(tag)
                    #pdb.set_trace()
                    list_rent += [rent]
                    list_utility += [utility]
                else:
                    list_date += [extract_availability_date(tag)]
                    #list_date += [available_from]

                tagRight += 1
        except Exception as e:
            pass


#        if itr >= 35:
#            break

#        itr += 1

    #pdb.set_trace()
    #var = 2
    return flat_information

def extract_address(tag):
    match = re.search(r"<b>([\w\s,.-]+?)<\/b><br\/>([\w\s,.-]+?)<\/a><\/td>", str(tag))
    address = ""

    if match:
        address = str(match.group(1)) + ", " + str(match.group(2))

    return address

def extract_rooms(tag):
    match = re.search(r'>([0-9])<\/td>', str(tag))
    number_of_rooms = ""

    if match:
        number_of_rooms = str(match.group(1))

    return number_of_rooms

def extract_size(tag):
    match = re.search(r'>([0-9]{2,3})<\/td>', str(tag))
    size = ""

    if match:
        size = str(match.group(1))

    return size

def extract_rent_and_utility(tag):
    match = re.findall(r'>([\w.,]+\skr\.)', str(tag))
    rent = ""
    utility = ""

    if match:
        rent = match[0]
        utility = match[1]

    return (rent, utility)

def extract_availability_date(tag):
    match = re.search(r'>([\w-]+?)<\/td>', str(tag))
    date = ""

    if match:
        date = str(match.group(1))

    return date

def check_for_new_flats(list_of_flats):
    new_flats = []

    return new_flats

def send_mail(mail_content):
    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    credentials = qs.get_credentials(SCOPES)

    mail_content = "This is a test"

    msg = qs.create_message("morten.madsen.92@gmail.com", "morten.madsen.92@gmail.com", "Test mail", mail_content)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    service_id = qs.create_service(credentials)
    qs.send_message(service_id, "me", msg)

def main():
    url = 'https://www.findbolig.nu/ledigeboliger/liste.aspx?sa=83328&where=1000-2400,%202800,%202820,%202840,%202900,%202920&m2min=70&rentmax=15000&roomsmin=2&showrented=1&showyouth=0&showOpenDay=0&showlimitedperiod=0&showunlimitedperiod=1&page=1&pagesize=100'
    soup = fetch_all_listings(url)

    flat_information = find_flat_information(soup)

    new_flats = check_for_new_flats(flat_information)

    send_mail(new_flats)

if __name__ == "__main__":
    main()