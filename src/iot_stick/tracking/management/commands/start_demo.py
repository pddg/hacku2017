from datetime import datetime, timedelta
from logging import getLogger, basicConfig, DEBUG
from time import sleep
import requests

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Post demo json"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.wait_for_init = True

    def handle(self, *args, **options):
        logger = getLogger("PostDemoData")
        basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        date_info = datetime.now()
        logger.debug("Start demo at: {}".format(date_info.strftime(date_format)))
        demo_data_list = [
            [35.048990, 135.779964, 0.0],
            [35.049118, 135.780159, 0.0],
            [35.049182, 135.780852, 0.0],
            [35.049662, 135.780857, 0.0],
            [35.049664, 135.781580, 0.0],
            [35.049719, 135.782315, 0.0],
            [35.049730, 135.782299, 0.0],
            [35.050257, 135.782263, 0.0],
            [35.051101, 135.782251, 0.0],
            [35.051633, 135.782412, 0.0],
            [35.051513, 135.782960, 0.0]
        ]
        for demo_data in demo_data_list:
            date_info = date_info + timedelta(seconds=10)
            json_template = {
                "datetime": date_info.strftime(date_format),
                "type": "channels",
                "module": "demo_module",
                "payload": {
                    "channels": []
                }
            }
            for i, value in enumerate(demo_data):
                json_template["payload"]["channels"].append({
                    "channel": i,
                    "datetime": date_info.strftime(date_format),
                    "type": "f" if i != 2 else "I",
                    "value": value
                })
            logger.debug("POST {}".format(json_template))
            response = requests.post(
                url="https://hacku2017.poyo.info/api/postlogs/",
                json=json_template,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code not in [i for i in range(200, 209)]:
                logger.warning("{} {}".format(str(response.status_code), response.text))
            else:
                logger.info("{} {}".format(str(response.status_code), demo_data))
            if self.wait_for_init:
                sleep(90)
                self.wait_for_init = False
            else:
                sleep(10)




