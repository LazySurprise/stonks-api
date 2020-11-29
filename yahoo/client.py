from datetime import datetime, timedelta

import yfinance as yf

class Yahoo:

    def fetch_prices(self, stonks):
        _stonks = dict()
        missed_stonks = dict()
        for _stonk in stonks :
            stonk_symbol = _stonk[0]
            prices, missed_stonk = self.fetch_price(_stonk)
            if ( missed_stonk != '' ) :
                missed_stonks[stonk_symbol] = missed_stonk
            else :
                _stonks[stonk_symbol] = prices
        return _stonks, missed_stonks

    # expects upper case stonk_symbol
    def fetch_price(self, stonk):
        stonk_symbol = stonk[0]
        _datetime = stonk[1]
        
        stonk = yf.Ticker(stonk_symbol)
        
        start_date, end_date = self.__build_dates(_datetime, num_days = 2)
        if (start_date == '' and end_date == ''):
            error = 'failed to retrieve prices for {0}. Incorrect date format.\nExpected\tYYYY-mm-dd HH:MM:SS\nReceived\t{1}'.format(stonk_symbol, _datetime)
            return [], error
        else:
            stonk = stonk.history(start = start_date, end = end_date).to_numpy()
            if (stonk.size != 14):
                error = 'prices not available for {0} from {1} - {2}'.format(stonk_symbol, start_date, end_date)
                return [], error
        stonk = self.__build_stonk_prices(stonk)
        return stonk, ''

    def __build_stonk_prices(self, stonk):
        prices = []
        for i in range(0, 2):
            price_fields = ['Date', 'Open', 'Low', 'Close', 'Volume']
            price_object = dict(zip(price_fields, stonk[i][0:5]))
            prices.append(price_object)
        return prices

    def __build_dates(self, start_date, num_days):
        if (not self.__proper_format(start_date)):
            return '', ''
        start = str(start_date)[:10]
        end = str(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=2))[:10] 
        return start, end 

    def __proper_format(self, _datetime ) :
        try:
            _datetime = datetime.strptime( _datetime , '%Y-%m-%d %H:%M:%S')
        except:
            return False

        return True
