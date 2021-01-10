from flask import Flask

from reddit import client as rc
from os import environ
from yahoo import client as yc

import config
import time

import json

app = Flask(__name__)
app.config.from_object(config.DevConfig)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/stonks')
def stonks():
    r = rc.Reddit('dev', environ.get('REDDIT_ID'), environ.get('REDDIT_SECRET'), environ.get('REDDIT_AGENT'))
    stonks = r.get_stonks()
    
    y = yc.Yahoo()
    stonks, missed_stonks = y.fetch_prices(stonks)
    #stonks = [(v, k) for k, v in stonks.items()]
    stonks = json.dumps(stonks)
    print('--------\nokieeeeee----\n')
    print(stonks)
    return stonks
    #return { 'stonks': stonks }
    #print(stonks)
    #print('----')
    #print(missed_stonks)

if __name__=='__main__':
    app.run()
