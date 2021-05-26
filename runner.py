import csv
import time
from datetime import datetime
import json
import requests
import asyncio

with open('credentials.json') as result:
    credentials = json.load(result)
    username = credentials["username"]
    password = credentials["password"]
    api_key = credentials["api_key"]
    min_cities = credentials["min_cities"]
    target_alliance = credentials["target_alliance"]
    subject = credentials["subject"]

with open("message.txt") as result:
    message = result.read()

def log(log):
    print(log)
    with open('recruiter_logs.txt', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([log])


async def recruiter_run():
    while True:
        day = datetime.today()

        thisday = day.strftime("%m/%d/%Y")
        thistime = day.strftime("%H:%M:%S")
        start_time = time.process_time()

        log('Recruiter Script commenced, Date: ' + str(thisday) + ', Time: ' + str(thistime))

        nations_api = 'https://politicsandwar.com/api/nations/?key='+ api_key
        nations_data = requests.get(nations_api).json()
        nations = nations_data["nations"]

        log('Nations API loaded, Elapsed Time: ' + str(time.process_time() - start_time))

        reqs = 0
        for nation in nations:
            with open('recruiter_tracker.json', 'r+') as sent:
                sent_to = json.load(sent)
                log('Nation ID Tracker file opened, Elapsed Time: ' + str(time.process_time() - start_time))

            if nation['cities'] >= min_cities and nation['alliance'] == target_alliance and int(nation['minutessinceactive']) < 241440 and int(nation['nationid']) not in sent_to and int(nation['nationid']) != 6:
                reqs += 1
                login_url = "https://politicsandwar.com/login/"
                message_url = "https://politicsandwar.com/inbox/message"
                login_data = {
                    "email": username,
                    "password": password,
                    "loginform": "Login"
                    }
                with requests.Session() as s:
                    s.post(login_url, data=login_data)
                    receiver = nation['leader']
                    message_data = {
                        "newconversation": "true",
                        "receiver": receiver,
                        "carboncopy": "",
                        "subject": subject,
                        "body": message,
                        "sndmsg": "Send Message"
                        }

                    s.post(message_url, data=message_data)
                log(f'Message #{reqs} Sent to: {nation["leader"]} Nation ID: {nation["nationid"]} Elapsed Time: {time.process_time() - start_time}')
                sent_to.append(int(nation["nationid"]))
            else:
                pass
            with open('recruiter_tracker.json', 'w') as sent:
                json.dump(sent_to, sent)

        log('Recruiter Script completed. Messages Sent: ' + str(reqs) + ', Elapsed Time: ' + str(time.process_time() - start_time))

        await asyncio.sleep(900)

loop = asyncio.get_event_loop()
loop.run_until_complete(recruiter_run())
