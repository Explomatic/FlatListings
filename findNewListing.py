from bs4 import BeautifulSoup
from urllib import request
from email.mime.text import MIMEText
import quickstart as qs
import sys, os.path, re, jsonpickle, io, pdb

class Flat:
    pass

def fetch_all_listings(url):
    webReq = request.urlopen(url)
    soup = BeautifulSoup(webReq, 'lxml')
    return(soup)

def get_flat_information(soup):
    tags = soup.find_all('td')

    flats={}
    base_url = "http://findbolig.nu"
    all_flat_ids = extract_info(tags, 'flat ids')
    all_urls =  extract_info(tags, 'urls')
    all_titles =  extract_info(tags, 'titles')
    all_addresses =  extract_info(tags, 'addresses')
    all_rooms =  extract_info(tags, 'number of rooms')
    all_sizes =  extract_info(tags, 'sizes')
    all_rents_and_utilities =  extract_info(tags, 'rent and utilities')
    all_dates =  extract_info(tags, 'availability dates')
<<<<<<< HEAD

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
=======
    num_of_flats = len(all_flat_ids)
#   len_all = [len(all_flat_ids), len(all_urls), len(all_titles), len(all_addresses), len(all_rooms),
#               len(all_sizes), len(all_rents_and_utilities), len(all_dates)]
#    print(len_all)
    list_of_flat_objects = [Flat() for i in range(num_of_flats)]

    #pdb.set_trace()

    for idx, obj in enumerate(list_of_flat_objects):
        obj.flat_id = all_flat_ids[idx]
        obj.url = base_url + all_urls[idx]
        obj.title = all_titles[idx]
        obj.address = all_addresses[idx]
        obj.number_of_rooms = all_rooms[idx]
        obj.size = all_sizes[idx]
        obj.rent = all_rents_and_utilities[idx][0]
        obj.utility = all_rents_and_utilities[idx][1]
        obj.availability_date = all_dates[idx]
        flats[obj.flat_id] = obj
>>>>>>> b5fee32eeb0ca4df08bb2aa8a1671a30c0213959

    return flats


def extract_info(tags, inputstr):
    info = []

    if inputstr == 'flat ids':
<<<<<<< HEAD
        matches = re.findall(r"<b>([\w\s,.-]+?)<\/b><br\/>([\w\s,.-]+?)<\/a><\/td>", str(s))

=======
        matches = re.findall(r'aid=([\d]+?)\&amp;s=2\"\s', str(tags))
>>>>>>> b5fee32eeb0ca4df08bb2aa8a1671a30c0213959

        if matches:
            for match in matches:
                info += [int(match)]

    elif inputstr == 'urls':
        matches = re.findall(r'href=\"([\w.\?=\/]+?)\&amp;s=2\"\s', str(tags))

        if matches:
            for match in matches:
                info += [match]

    elif inputstr == 'titles':
        matches = re.findall(r'title=\"([\w\s,.\/-]+?)\"><b>', str(tags))

        if matches:
            for match in matches:
                info += [match]

    elif inputstr == 'addresses':
        matches = re.findall(r"<b>([\w\s,.-]+?)<\/b><br\/>([\w\s,.-]+?)<\/a><\/td>", str(tags))

        if matches:
            for match in matches:
                info += [str(match[0]) + ", " + str(match[1])]

    elif inputstr == 'number of rooms':
        matches = re.findall(r'>([0-9])<\/td>', str(tags))

        if matches:
            for match in matches:
                info += [int(match)]

    elif inputstr == 'sizes':
        matches = re.findall(r'>([0-9]{2,3})<\/td>', str(tags))

        if matches:
            for match in matches:
                info += [int(match)]

    elif inputstr == 'rent and utilities':
        matches = re.findall(r'>([\w.,]+\skr\.)<br\/>([\w.,]+\skr\.)<\/td>', str(tags))

        if matches:
            for match in matches:
                info += [[match[0], match[1]]]

    elif inputstr == 'availability dates':
        matches = re.findall(r'>(\d\d\-\d\d\-\d\d\d\d)<\/td>|>(Ledig nu)<\/td>', str(tags))

        if matches:
            for match in matches:
                if match[0]:
                    info += [match[0]]
                elif match[1]:
                    info += [match[1]]

    return info

def check_for_new_flats(found_flats):
    new_flats = {}
    filename = 'known_flats.txt'

    #pdb.set_trace()
    if os.path.isfile(filename):
        with io.open(filename, 'r', encoding="utf-8") as f:
            content = f.read()
            known_flats = jsonpickle.decode(content)
            known_flats = {int(k): v for k, v in known_flats.items()}
            first_time = False
    else:
        f = io.open('known_flats.txt', 'w', encoding="utf-8")
        first_time = True

    if first_time:
        new_flats = found_flats
    else:
        for key, value in found_flats.items():
            if key not in known_flats.keys():
                new_flats[key] = value

    jsonObj = jsonpickle.encode(found_flats)
    f.write(jsonObj)
    f.close()

    return new_flats


def generate_mail_content(list_of_flats):
    mail_content = ""

    for flat_id, flat in list_of_flats.items():
        mail_content += flat.url + "\n"
        mail_content += flat.title + "\n"
        mail_content += flat.address + "\n"
        mail_content += str(flat.size) + " m2, " + str(flat.number_of_rooms) + " værelser\n"
        mail_content += "Husleje " + flat.rent + " pr. mdr., acontoforbrug " + flat.utility + " pr. mdr.\n"
        mail_content += "Ledig fra: " + flat.availability_date + "\n\n"


    mail_content = mail_content[:-2]

    return mail_content

def send_mail(mail_content):

    with io.open('tmpfile.txt', 'w', encoding="utf-8") as f:
        f.write(mail_content)
        f.close()

    #print("Now we would normally send a mail!")
    #return 0

    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    credentials = qs.get_credentials(SCOPES)

    #mail_content = "This is a test"

    msg = qs.create_message("morten.madsen.92@gmail.com", "morten.madsen.92@gmail.com",
                            "New flats found!", mail_content)

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
        mail_content = generate_mail_content(new_flats)
        send_mail(mail_content)
    else:
        print("No new flats found!")

if __name__ == "__main__":
    main()