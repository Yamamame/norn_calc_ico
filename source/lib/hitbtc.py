#!/usr/bin/python
#coding: utf-8
#hitbtc.py => class HITBTClient
#参照: https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import requests
import datetime
import time

class HITBTClient(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)
        self.now     = datetime.date.today()

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def get_address(self, currency_code):
        return self.session.get("%s/account/crypto/address/%s" % (self.url, currency_code)).json()

    def get_candles(self, symbols="ETHBTC"):
        print ("%s/public/candles/%s" % (self.url, symbols))
        print self.session.get("%s/public/candles/%s" % (self.url, symbols))
        return self.session.get("%s/public/candles/%s" % (self.url, symbols)).json()

    def get_history_trades(self):
        return self.session.get("%s/history/trades/" % (self.url)).json()

    def get_history_trades_by_a_month(self):
        month_ago = datetime.datetime.fromtimestamp(time.mktime((
          self.now.year, self.now.month - 1,self.now.day,0,0,0,0,0,0)))
        data = {'sort':"DESC", 'by':"timestamp", 'from':month_ago}
        return self.session.get("%s/history/trades/" % (self.url),params=data).json()

    def get_history_payment(self):
        return self.session.get("%s/history/trades/" % (self.url)).json()

    def get_account_balance(self):
        """Get main balance."""
        return self.session.get("%s/account/balance" % self.url).json()

    def get_trading_balance(self):
        """Get trading balance."""
        return self.session.get("%s/trading/balance" % self.url).json()

    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
                'currency': currency_code, 'amount': amount,
                'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
            }).json()

    def new_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order."""
        data = {'symbol': symbol_code, 'side': side, 'quantity': quantity}

        if price is not None:
            data['price'] = price

        return self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()

    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait': wait} if wait is not None else {}

        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def cancel_order(self, client_order_id):
        """Cancel order."""
        return self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()

    def withdraw(self, currency_code, amount, address, network_fee=None):
        """Withdraw."""
        data = {'currency': currency_code, 'amount': amount, 'address': address}

        if network_fee is not None:
            data['networkfee'] = network_fee

        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_transaction(self, transaction_id):
        """Get transaction info."""
        return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()

    def get_transaction_by_a_month(self):
        month_ago = datetime.datetime.fromtimestamp(time.mktime((
          self.now.year, self.now.month - 1,self.now.day,0,0,0,0,0,0)))
        data = {'sort':"DESC", 'by':"timestamp", 'from':month_ago}
        return self.session.get("%s/account/transactions/" % (self.url),params=data).json()
