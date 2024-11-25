import os
from requests import Session
from requests_ip_rotator import ApiGateway, ALL_REGIONS
from dotenv import load_dotenv

load_dotenv()


class Downloader(object):

    def __init__(self, domain):

        self.gateway = ApiGateway(
            domain,
            access_key_id=os.getenv("ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ACCESS_KEY_SECRET"),
            regions=ALL_REGIONS,
        )
        print("Starting the gateway")
        self.gateway.shutdown()
        self.gateway.start()

        self.s = Session()
        self.s.mount(domain, self.gateway)

    def shutdown_gateway(self):
        print("Shutting down the gateway")
        self.gateway.shutdown()

    def fetch(self, url, params):
        return self.s.get(url, params=params)
