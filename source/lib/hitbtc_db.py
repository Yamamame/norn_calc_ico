#!/usr/bin/python
#coding: utf-8
#hitbtc_db.py => class HITBTCDB
import MySQLdb

class HITBTCDB(object):
    def __init__(self):
        self.db_host     = 'localhost'
        self.db_port     = 3306
        self.db_user     = 'yama'
        self.db_pass     = 'sYr6nukU'
        self.db_name     = 'altcoins'
        self.open_conn()

    def open_conn(self):
        """Get symbol."""
        self.conn = MySQLdb.connect(
          host   = self.db_host,
          port   = self.db_port,
          user   = self.db_user,
          passwd = self.db_pass,
          db     = self.db_name,
        )
        self.cursor = self.conn.cursor()

    def regist_dict(self,data_dict):
        for data_row in data_dict :
            # 現在存在するかどうかチェック
            current_sql  = ' SELECT instrument,quantity,price,volume,fee,rebate,total FROM t_trades'
            current_sql += ' WHERE id=%s '
            placehold = (
                data_row['id'],
            )
            self.cursor.execute(current_sql,placehold)
            data_one = self.cursor.fetchall()
            print len(data_one)
            print('data row : "%s"' % data_row)
            if len(data_one) == 0:
                placehold = (
                    data_row['timestamp'],data_row['symbol'],data_row['id'],
                    data_row['orderId'],data_row['side'],data_row['quantity'],data_row['price'],
                    data_row['fee'],
                )
                current_sql  = ' INSERT INTO t_trades '
                current_sql += ' (exec_date,instrument,id'
                current_sql += ' ,order_id,side,quantity,price'
                # current_sql += ' ,volume,fee,rebate,total,uptime)'
                current_sql += ' ,fee,uptime)'
                # current_sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),%s,%s'
                current_sql += ',%s,%s,%s,%s,%s,now())'
                self.cursor.execute(current_sql,placehold)
                print('INSERT OK %d' , data_row['id'])
            else :
                placehold = (
                    data_row['timestamp'],data_row['symbol'],
                    data_row['orderId'],data_row['side'],data_row['quantity'],data_row['price'],
                    data_row['fee'],
                    data_row['id'],
                )
                current_sql  = ' UPDATE t_trades SET '
                current_sql += ' exec_date = CONVERT_TZ(%s,"+00:00","+09:00"),instrument=%s'
                current_sql += ' ,order_id=%s,side=%s,quantity=%s,price=%s'
                # current_sql += ' ,volume=%s,fee=%s,rebate=%s,total=%s,uptime=now()'
                current_sql += ' ,fee=%s,uptime=now()'
                current_sql += ' WHERE id=%s '
                self.cursor.execute(current_sql,placehold)
                print('UPDATE OK %d' , data_row['id'])
        print('finish and commit ')
        self.conn.commit()

    def regist_balance_now_dict(self,account_data_dict,trading_data_dict):
        for data_row in account_data_dict :
            if float(data_row['available']) > 0 :
                print('account balance: "%s"' % data_row)
        for data_row in trading_data_dict :
            if float(data_row['available']) > 0 :
                print('trading balance: "%s"' % data_row)

    def regist_transactions_dict(self,data_dict):
        for data_row in data_dict :
            print('transactions balance: "%s"' % data_row)
