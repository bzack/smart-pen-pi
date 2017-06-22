from flask import Flask, g
from random import randint, randrange
import sqlite3
from time import gmtime, time
app = Flask(__name__)

EVENT_TYPES=['PACKAGE_CREATED', 'MEASUREMENT', 'COUNTERFEIT_DETECTED', 'INJECTION', 'SPOILED']


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/create_fake/<int:count>", methods=['GET'])
def create_fake(count):
    txt = ""
    base_utc = time() - (60*60*24 * randrange(30,90))
    for i in range(count):
        id = "abbv%04d" % randint(0,9999)
        for j in range(0,10):
            event_type = 'MEASUREMENT'
            time_utc = base_utc + 60*60*j
            lat = randrange(34.0,42.0)
            lng = randrange(-120.0,-76.0)
            temp = randrange(0,120)
            light = randint(0,110)
            record_measurement(id,time_utc=time_utc, event_type=event_type, lat=lat, lng=lng, temp=temp, light=light)
        txt += id
    get_db().commit()
    return txt


def record_measurement(id, time_utc, event_type, lat, lng, temp, light):
    comp_key = (id,time_utc,event_type)
    rows = get_db().execute("select count(*) from measurements where id=? and time_utc=? and event_type=?", comp_key)
    if rows.rowcount < 1:
        data = (id, time_utc, event_type, lat, lng, temp, light)
        get_db().execute("insert into measurements(id, time_utc, event_type, lat, lng, temp, light) values(?,?,?,?,?,?,?)", data)
        get_db().commit()


def connect_db():
    return sqlite3.connect('database.db')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db