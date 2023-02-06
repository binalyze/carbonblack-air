import json
import sys
from cbapi.psc.defense import *
import time
import requests
import os

cb = CbDefenseAPI(profile='default')

air_webhook = os.environ["AIR_WEBHOOK_URL"]

cb_url = os.environ["CB_DEFENSE_SERVER"]  # https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/#:~:text=Path%20/%20Org%20Key-,The%20URL%20Parts,-Hostname
url_base = f'/{cb_url}alerts?s[dataGrouping]=NO_GROUP_RESULTS&s[highlight]=true&s[searchWindow]=ALL&s[maxRows]=20&s[fromRow]=1&s[sortDefinition][fieldName]=FIRST_ACTIVITY&s[sortDefinition][sortOrder]=DESC&s[c][THREAT_SCORE][0]=1&s[c][TARGET_PRIORITY][0]=LOW&s[c][TARGET_PRIORITY][1]=MEDIUM&s[c][TARGET_PRIORITY][2]=HIGH&s[c][TARGET_PRIORITY][3]=MISSION_CRITICAL&s[c][SEVERITY][0]=WARNING&s[c][SEVERITY][1]=NOTICE&s[c]'

headers = {
    'Content-Type': 'application/json'
}


def logs(log):
    with open("integration.log", "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {log}\n")


def main():
    while True:
        for notification in cb.notification_listener():
            try:
                with open('query.json', 'w+') as fp:
                    notify = (json.dumps(notification, indent=4, sort_keys=True))
                    fp.write('')
                    fp.write(notify)
                    fp.close()

                with open('query.json') as fp:
                    alert = json.load(fp)
                hostname = alert['deviceInfo']['deviceName']
                epoch = alert['eventTime']
                alert_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(str(epoch)[0:(len(str(epoch))-3)])))
                json_data = {
                    "result":
                        {
                            "host": hostname
                        }
                }
                webhook = requests.post(url=air_webhook, headers=headers, json=json_data)
                if webhook.status_code == 200:
                    print(f'An acquisiton request sent to {hostname} at {alert_time}.')
                    logs(f'Success: An acquisiton request sent to {hostname} at {alert_time}.')
                else:
                    print(f'Error: {webhook.text}')
                    logs(f'Error: {webhook.text}')
            except Exception as exc:
                print(f'Error: {exc}')


if __name__ == "__main__":
    try:
        print('Binalyze AIR & Carbon Black Integration is working... '
              'Once an acquisition has initiated you will be informed here: ')
        sys.exit(main())
    except KeyboardInterrupt:
        print('Script stopped working with a Keyboard interrupt..')