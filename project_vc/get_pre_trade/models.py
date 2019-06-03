from django.db import models

# Create your models here.
#参照   : https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import requests
import datetime
import time


class HITBTClient(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)
        self.now = datetime.date.today()
