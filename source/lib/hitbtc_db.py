#!/usr/bin/python
#coding: utf-8
#hitbtc_db.py => class HITBTCDB
import MySQLdb
import datetime

class HITBTCDB(object):
    def __init__(self,host='localhost',port=3306,user='yama',password='sYr6nukU',db_name='altcoins',mode='hitbtc'):
        self.mode        = mode
        self.db_host     = host
        self.db_port     = port
        self.db_user     = user
        self.db_pass     = password
        self.db_name     = db_name
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
    """
    wrapperとなる関数 名前がずれているがデフォルトはhitbtcとする
    """
    def regist_candles(self, set_symbols, data_dict, debug=0):
        if self.mode == 'bittrex':
            self.regist_candles_bittrex(set_symbols, data_dict, debug)
        else:
            self.regist_candles_hitbtc(set_symbols, data_dict, debug)

    """
    bittrex用に作成した関数 共通化できるものは共通化したい
    """

    def regist_candles_bittrex(self, set_symbols, data_dict, debug=0):
        """ bittrexのAPIはwindowを動かしながら24時間の範囲を取得できる """
        print("--------------------------------------------------- ")
        if debug != 0 :
            print("--------------------------------------------------- ")
            print("symbol      {0} ".format(data_dict['MarketName']))
            print("min         {0} ".format(data_dict['Low']))
            print("max         {0} ".format(data_dict['High']))
            print("open        {0} ".format(data_dict['PrevDay']))
            print("close       {0} ".format(data_dict['Last']))
            print("volume      {0} ".format(data_dict['BaseVolume']))
            print("volumequote {0} ".format(data_dict['Volume']))
            print("TimeStamp   {0} ".format(data_dict['TimeStamp']))
        print("--------------------------------------------------- ")
        placehold = (
            data_dict['TimeStamp'].translate(
                {ord(u'T'): u' ', ord(u'Z'): u' ', }
            ), set_symbols, data_dict['Low'],
            data_dict['High'], data_dict['PrevDay'], data_dict['Last'],
            data_dict['BaseVolume'], data_dict['Volume'],
        )
        current_sql = ' INSERT INTO trade_candles '
        current_sql += ' (timestamp,symbols,min'
        current_sql += ' ,max,open,close'
        current_sql += ' ,volume,volumequote,uptime)'
        current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),%s,%s'
        current_sql += ',%s,%s,%s,%s,%s,now())'
        self.cursor.execute(current_sql, placehold)
        # result = self.cursor.fetchall()
        if debug != 0:
            print('this INSERT OK {0} {1}'.format(data_dict['MarketName'], data_dict['TimeStamp']))
            print('finish and commit ')
        self.conn.commit()


    """
    hitbtc用に作成した関数 共通化できるものは共通化したい
    """
    def get_used_symbols(self,debug=0):
        # 現在までに売買履歴のあるsymbolを取得
        #select instrument,side,sum(total) from t_trades GROUP BY instrument,side;
        current_sql  = ' SELECT instrument FROM t_trades  GROUP BY instrument'
        self.cursor.execute(current_sql)
        data_one = self.cursor.fetchall()
        return data_one
    def regist_dict(self,data_dict,debug = 0):
        for data_row in data_dict :
            # 現在存在するかどうかチェック
            current_sql  = ' SELECT instrument,quantity,price,volume,fee,rebate,total FROM t_trades'
            current_sql += ' WHERE id=%s '
            placehold = (
                data_row['id'],
            )
            self.cursor.execute(current_sql,placehold)
            data_one = self.cursor.fetchall()
            data_row['volume'] = str(float(data_row['quantity']) * float(data_row['price']))
            if 'buy' in data_row['side'] :
                data_row['total']  = str((float(data_row['volume']) * -1) - float(data_row['fee']))
            else :
                data_row['total']  = str((float(data_row['volume']) * 1) - float(data_row['fee']))
            if debug != 0 :
                print (len(data_one))
                print('data row : "%s"' % data_row)
            if len(data_one) == 0:
                placehold = (
                    data_row['timestamp'].translate(
                    {ord(u'T'): u' ',ord(u'Z'): u' ',}
                    ),data_row['symbol'],data_row['id'],
                    data_row['orderId'],data_row['side'],data_row['quantity'],data_row['price'],
                    data_row['volume'],data_row['fee'],data_row['total'],
                )
                current_sql  = ' INSERT INTO t_trades '
                current_sql += ' (exec_date,instrument,id'
                current_sql += ' ,order_id,side,quantity,price'
                # current_sql += ' ,volume,fee,rebate,total,uptime)'
                current_sql += ' ,volume,fee,total,uptime)'
                # current_sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),%s,%s'
                current_sql += ',%s,%s,%s,%s,%s,%s,%s,now())'
                self.cursor.execute(current_sql,placehold)
                self.cursor.fetchall()
                if debug != 0 :
                    print('this INSERT OK %d' , data_row['id'])
            else :
                placehold = (
                    data_row['timestamp'].translate(
                    {ord(u'T'): u' ',ord(u'Z'): u' ',}
                    ),data_row['symbol'],
                    data_row['orderId'],data_row['side'],data_row['quantity'],data_row['price'],
                    data_row['volume'],data_row['fee'],data_row['total'],
                    data_row['id'],
                )
                current_sql  = ' UPDATE t_trades SET '
                current_sql += ' exec_date = CONVERT_TZ(%s,"+00:00","+09:00"),instrument=%s'
                current_sql += ' ,order_id=%s,side=%s,quantity=%s,price=%s'
                # current_sql += ' ,volume=%s,fee=%s,rebate=%s,total=%s,uptime=now()'
                current_sql += ' ,volume=%s,fee=%s,total=%s,uptime=now()'
                current_sql += ' WHERE id=%s '
                self.cursor.execute(current_sql,placehold)
                self.cursor.fetchall()
                # print('sUPDATE OK : "%s"' % result)
                if debug != 0 :
                    print('this UPDATE OK %d' , data_row['id'])
            if debug != 0 :
                print('finish and commit ')
        self.conn.commit()

    def regist_balance_now_dict(self,account_data_dict,trading_data_dict):
        for data_row in account_data_dict :
            if float(data_row['available']) > 0 :
                print('account balance: "%s"' % data_row)
        for data_row in trading_data_dict :
            if float(data_row['available']) > 0 :
                print('trading balance: "%s"' % data_row)

    def regist_candles_hitbtc(self,set_symbols,data_dict,debug=0):
        for data_row in data_dict :
            # 現在存在するかどうかチェック
            if not isinstance(data_row, dict) and data_row in 'error':
                print("symbols:{0} error : {1}".format(set_symbols, data_dict))
                continue
            current_sql  = ' SELECT symbols FROM trade_candles'
            current_sql += ' WHERE symbols=%s AND timestamp=CONVERT_TZ(%s,"+00:00","+09:00") ;'
            placehold = (
                set_symbols,
                data_row['timestamp'].translate({ord(u'T'): u' ',ord(u'Z'): u' ',}),
            )
            self.cursor.execute(current_sql,placehold)
            data_one = self.cursor.fetchall()
            if len(data_one) == 0:
                placehold = (
                    data_row['timestamp'].translate(
                    {ord(u'T'): u' ',ord(u'Z'): u' ',}
                    ),set_symbols,data_row['min'],
                    data_row['max'],data_row['open'],data_row['close'],
                    data_row['volume'],data_row['volumeQuote'],
                )
                current_sql  = ' INSERT INTO trade_candles '
                current_sql += ' (timestamp,symbols,min'
                current_sql += ' ,max,open,close'
                current_sql += ' ,volume,volumequote,uptime)'
                current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),%s,%s'
                current_sql += ',%s,%s,%s,%s,%s,now())'
                self.cursor.execute(current_sql,placehold)
                # result = self.cursor.fetchall()
                if debug != 0 :
                    print('this INSERT OK %d' , data_row['id'])
            if debug != 0 :
                print('finish and commit {0},{1},{2}'.format(
                    current_sql, set_symbols, data_row['timestamp']))
        self.conn.commit()

    def trading_balance_and_average(self,trading_data_dict):
        for data_row in trading_data_dict :
            if float(data_row['available']) > 0 :
                # print('trading balance: "%s"' % data_row)
                print('trading balance: "%s"' % data_row['currency'])
                print('      available: "%s"' % data_row['available'])
                average_value = self.calculate_current_price(data_row['currency'])
                print('        average: "%s"' % average_value)
                print(' ')
    """
    入力された範囲で月をずらしてnヶ月分を取得する
    (デフォルトは3ヶ月前から今日まで)
    """
    def get_recent_period(self, instrument='ETHBTC', span_end=0, span_start=3):
        instrument = '%' + instrument + '%'
        # 今日の分を含めるため予め+1しておく
        nowdate   = datetime.date.today() + datetime.timedelta(days=1)
        startdate = nowdate - datetime.timedelta(days= int(30 * span_start))
        enddate   = nowdate - datetime.timedelta(days= int(30 * span_end))
        current_sql  = ' select symbols,timestamp ,min,max,open,close,volume from trade_candles tca '
        current_sql += ' WHERE symbols like %s AND timestamp BETWEEN %s AND %s '
        current_sql += ' ORDER BY symbols,timestamp '
        placehold = (
            instrument,
            "{0:%Y-%m-%d}".format(startdate),
            "{0:%Y-%m-%d}".format(enddate),
        )
        # print (current_sql)
        # print (placehold)
        self.cursor.execute(current_sql,placehold)
        data_dict = self.cursor.fetchall()
        return data_dict
    """
    入力された範囲で月をずらしてnヶ月分を取得する
    (デフォルトは3ヶ月前から今日まで)
    """

    def get_recent_period_tith_datetime(self, instrument='ETHBTC', span_end=None, span_start=None):
        instrument = '%' + instrument + '%'
        # 今日の分を含めるため予め+1しておく
        nowdate = datetime.date.today() + datetime.timedelta(days=1)
        if span_end is None :
            span_end = nowdate - datetime.timedelta(days=int(30 * 0))
        if span_start is None :
            span_start = nowdate - datetime.timedelta(days=int(30 * 3))
            
        current_sql = ' select symbols,timestamp ,min,max,open,close,volume from trade_candles tca '
        current_sql += ' WHERE symbols like %s AND timestamp BETWEEN %s AND %s '
        current_sql += ' ORDER BY symbols,timestamp '
        placehold = (
            instrument,
            "{0:%Y-%m-%d}".format(span_start),
            "{0:%Y-%m-%d}".format(span_end),
        )
        # print (current_sql)
        # print (placehold)
        self.cursor.execute(current_sql, placehold)
        data_dict = self.cursor.fetchall()
        return data_dict
        
    def get_recently_price(self,instrument):
        instrument = '%' + instrument + '%'
        current_sql  = ' select tca.symbols,min,max,open,close,volume,tca.timestamp from trade_candles tca '
        current_sql += ' INNER JOIN ( '
        current_sql += '     select symbols,max(timestamp) as timestamp from trade_candles '
        current_sql += '     WHERE symbols like %s GROUP BY symbols '
        current_sql += ' ) tcb '
        current_sql += ' ON tca.symbols = tcb.symbols AND tca.timestamp = tcb.timestamp '
        placehold = (
            instrument,
        )
        # print (current_sql)
        self.cursor.execute(current_sql,placehold)
        data_dict = self.cursor.fetchall()
        return data_dict

    def calculate_current_price(self,instrument):
        #一つの銘柄の現在価格を計算
        average_value = 0.00
        instrument = '%' + instrument + '%'
        current_sql  = ' SELECT count(order_id),instrument FROM t_trades '
        current_sql += ' WHERE instrument like %s GROUP BY instrument ORDER BY count(order_id) DESC'

        ###これで平均値になるか? -> sellとbuyが区別できていない
        current_sql  = ' SELECT instrument,avg(price),avg(quantity) FROM t_trades '
        current_sql += ' WHERE exec_date > (now() - INTERVAL 1 month) AND  instrument like %s GROUP BY instrument;'
        # current_sql += ' WHERE uptime > (now() - INTERVAL 12 month)  '
        placehold = (
            instrument,
        )
        # print (current_sql)
        # print (instrument)
        self.cursor.execute(current_sql,placehold)
        # self.cursor.execute(current_sql)
        data_dict = self.cursor.fetchall()
        for data_row in data_dict :
            print('calc instrument: "{0:<10}" '.format(data_row[0]))
            print('calc      price: "{0:<10}" '.format(data_row[1]))
            print('calc   quantity: "{0: 4.10f}" '.format(data_row[2]))
        return average_value

    ###前回のトレードを取得
    def pre_trade_value(self,instrument='ETH',debug = 0):
        instrument = '%' + instrument + '%'
        current_sql = ' SELECT t_a.instrument,t_a.price,t_a.quantity,t_a.side,t_a.exec_date FROM t_trades as t_a '
        current_sql += ' WHERE id IN '
        current_sql += '     (SELECT id FROM t_trades '
        current_sql += '      WHERE (instrument,side,exec_date) IN '
        current_sql += '          ( SELECT instrument,side,max(exec_date) FROM t_trades GROUP BY instrument,side ) '
        current_sql += '      GROUP BY instrument,side'
        current_sql += '     ) '
        current_sql += ' AND instrument like %s; '
        placehold = (
            instrument,
        )
        # print (current_sql)
        # print (instrument)
        self.cursor.execute(current_sql,placehold)
        data_dict = self.cursor.fetchall()
        # for data_row in data_dict :
        #     print('calc    price: "%s" ' % str(data_row[0]))
        #     print('calc quantity: "%s" ' % str(data_row[1]))
        return data_dict

    def regist_transactions_dict(self,data_dict,debug = 0):
        for data_row in data_dict :
            # 現在存在するかどうかチェック
            current_sql  = ' SELECT t_hash FROM payment_history '
            current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
            current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
            placehold = (
                  data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                  data_row['id'].split("-")[3], data_row['id'].split("-")[4],
            )
            self.cursor.execute(current_sql,placehold)
            data_one = self.cursor.fetchall()
            if debug != 0 :
                print (len(data_one))
                print('transactions balance: "%s"' % data_row)
            if len(data_one) == 0:
                current_sql  = ' INSERT INTO payment_history '
                current_sql += ' (exec_date,operation_id_1,operation_id_2,operation_id_3'
                current_sql += ' ,operation_id_4,operation_id_5,type,amount'
                if 'hash' not in data_row :
                    # hashのkeyはないことがある
                    current_sql += ' ,currency,uptime)'
                    current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),'
                    current_sql += '%s,%s,%s,'
                    current_sql += '%s,%s,%s,%s,'
                    current_sql += '%s,now());'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ),
                      data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4], data_row['type'], data_row['amount'],
                      data_row['currency'],
                    )
                    self.cursor.execute(current_sql,placehold)
                else :
                    current_sql += ' ,t_hash,currency,uptime)'
                    current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),%s,%s,%s,%s,%s,%s,%s,%s,%s,now());'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ), data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4], data_row['type'], data_row['amount'],
                      data_row['hash'], data_row['currency'],
                    )
                    self.cursor.execute(current_sql,placehold)
                if debug != 0 :
                    print ('INSERT OK')
            else :
                current_sql  = ' UPDATE payment_history SET '
                current_sql += ' exec_date = CONVERT_TZ(%s,"+00:00","+09:00") '
                current_sql += ' ,type=%s,amount=%s'
                if 'hash' not in data_row :
                    # hashのkeyはないことがある
                    current_sql += ' ,currency=%s,uptime=now() '
                    current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
                    current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ),
                      data_row['type'],data_row['amount'],
                      data_row['currency'],
                      data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4]
                    )
                else:
                    current_sql += ' ,t_hash=%s,currency=%s,uptime=now() '
                    current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
                    current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ),
                      data_row['type'],data_row['amount'],
                      data_row['hash'],data_row['currency'],
                      data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4]
                    )

                self.cursor.execute(current_sql,placehold)
                if debug != 0 :
                    print ('UPDATE OK')
            self.conn.commit()
