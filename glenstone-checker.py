import requests, json, pprint, os, time
from requests.structures import CaseInsensitiveDict

pp = pprint.PrettyPrinter(indent=4)

DATE_WANTED = "2021-12-04"

def get_glen(method="calendar"):

    url = "https://visit.glenstone.org/api"

    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0"
    headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
    headers["Referer"] = "https://visit.glenstone.org/events/8c42a85b-0f1b-eee0-a921-8464481a74f6?tg=6d574b40-caf4-a7eb-899b-b805098ed106"
    headers["Content-Type"] = "application/json"
    headers["X-Requested-With"] = "XMLHttpRequest"
    headers["Origin"] = "https://visit.glenstone.org"
    headers["Connection"] = "keep-alive"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Site"] = "same-origin"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"
    headers["TE"] = "trailers"

    data = '{"method":"GET","uri":"events/8c42a85b-0f1b-eee0-a921-8464481a74f6/' + method + '"}'

    resp = requests.post(url, headers=headers, data=data)
    return resp.text


while True:
    calendar_raw = get_glen("calendar")

    calendar = json.loads(calendar_raw)["calendar"]
    if DATE_WANTED in calendar:
        avail = calendar[DATE_WANTED]
        print(f"Availability for {DATE_WANTED} is {avail}")
        if avail != 'sold_out':
            session_data = json.loads(get_glen('sessions?_ondate=' + DATE_WANTED))
            for sesh in session_data['event_session']['_data']:
                if (not sesh['sold_out']) or (not sesh['oversold_out']):
                    print(f"Theres's a session at {sesh['start_datetime']}")
                    try:
                        os.system(f"say We have a ticket for {sesh['start_datetime']}")
                    except:
                        print("Guess you're not on a mac")
            print(f"total available is {session_data['_total']}")
    time.sleep(30)