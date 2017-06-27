from bs4 import BeautifulSoup
from urllib import request
from email.mime.text import MIMEText
import quickstart as qs
import sys, os.path, re, jsonpickle, io, pdb

class flat:
    pass

def fetch_all_listings(url):
    webReq = request.urlopen(url)
    soup = BeautifulSoup(webReq, 'lxml')
    return(soup)

def get_flat_information(soup):
    tags = soup.find_all('td')

    flats={}
    base_url = "http://findbolig.nu"
    all_flat_ids = extract_all_flat_ids(tags)
    all_urls = extract_all_urls(tags)
    all_titles = extract_all_titles(tags)
    all_addresses = extract_all_addresses(tags)
    all_rooms = extract_all_rooms(tags)
    all_sizes = extract_all_sizes(tags)
    all_rents, all_utilities = extract_all_rent_and_utilities(tags)
    all_dates = extract_all_availability_dates(tags)
    counter = 0
    for tag in tags:
        if "advertLink" in str(tag) and not tag.img:
            tmpFlat = flat()
            counter = 1
            tmpFlat.title = str(tag.a['title'])
            tmpFlat.address = extract_address(tag)
            tmpFlat.url = base_url + tag.a['href']
            tmpFlat.flat_id = extract_flat_id(tmpFlat.url)
            continue

        if counter == 1:
            tmpFlat.number_of_rooms = extract_rooms(tag)
            counter += 1
        elif counter == 2:
            tmpFlat.size = extract_size(tag)
            counter += 1
        elif counter == 3:
            tmpFlat.rent, tmpFlat.utility = extract_rent_and_utility(tag)
            counter += 1
        elif counter == 4:
            tmpFlat.date_available = extract_availability_date(tag)
            flats[tmpFlat.flat_id] = tmpFlat

    return flats


def extract_all_addresses(tags):
    match = re.search(r"<b>([\w\s,.-]+?)<\/b><br\/>([\w\s,.-]+?)<\/a><\/td>", str(s))
    address = ""

    if match:
        address = str(match.group(1)) + ", " + str(match.group(2))

    return address


def extract_all_rooms(tags):
    match = re.search(r'>([0-9])<\/td>', str(tags))
    number_of_rooms = ""

    if match:
        number_of_rooms = float(match.group(1))

    return number_of_rooms


def extract_all_sizes(tags):
    match = re.search(r'>([0-9]{2,3})<\/td>', str(tags))
    size = ""

    if match:
        size = float(match.group(1))

    return size


def extract_all_rent_and_utilities(tags):
    match = re.findall(r'>([\w.,]+\skr\.)', str(tags))
    rent = ""
    utility = ""

    if match:
        rent = match[0]
        utility = match[1]

    return (rent, utility)


def extract_all_availability_dates(tags):
    match = re.search(r'>([\w-]+?)<\/td>', str(tags))
    date = ""

    if match:
        date = str(match.group(1))

    return date


def extract_all_flat_ids(tags):
    match = re.search(r'aid=([\d]+?)\&amp', tags)
    flat_id = ""

    if match:
        flat_id = float(match.group(1))

    return flat_id


def extract_all_urls(tags):
    match = re.search(r'aid=([\d]+?)\&amp', tags)
    urls = ""

    if match:
        urls = float(match.group(1))

    return urls


def extract_all_titles(tags):
    match = re.search(r'aid=([\d]+?)\&amp', tags)
    titles = ""

    if match:
        titles = float(match.group(1))

    return titles


def check_for_new_flats(found_flats):
    new_flats = {}
    filename = 'known_flats.txt'

    if os.path.isfile(filename):
        with io.open(filename, 'r', encoding="utf-8") as f:
            content = fid.read()
            known_flats=jsonpickle.decode(content)
            first_time = False
    else:
        f = io.open('known_flats.txt', 'w', encoding="utf-8")
        first_time = True

    if first_time:
        jsonObj = jsonpickle.encode(found_flats)
        f.write(jsonObj)
        f.close()
        new_flats = found_flats
    else:
        for key, value in found_flats.items():
            if key not in known_flats.keys():
                new_flats[key] = value

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
    args = sys.argv[1:]
    # if not args:
    #     max_rent = 15000
    #     min_rooms = 2
    #     min_m2 = 70
    # else:
    #     if args[0] == '--todir':
    #         todir = args[1]
    #         del args[0:2]
    #
    #     tozip = ''
    #     if args[0] == '--tozip':
    #         tozip = args[1]
    #         del args[0:2]
    #
    #     if len(args) == 0:
    #         print
    #         "error: must specify one or more dirs"
    #         sys.exit(1)

    url = 'https://www.findbolig.nu/ledigeboliger/liste.aspx?sa=83328&where=1000-2400,%202800,%202820,%202840,%202900,%202920&m2min=70&rentmax=15000&roomsmin=2&showrented=1&showyouth=0&showOpenDay=0&showlimitedperiod=0&showunlimitedperiod=1&page=1&pagesize=100'

    soup = fetch_all_listings(url)

    flats = get_flat_information(soup)

    new_flats = check_for_new_flats(flats)

    if new_flats:
        #send_mail(new_flats)
        print("Now we would send a mail!")

if __name__ == "__main__":
    main()