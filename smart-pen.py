from flask import Flask, g, jsonify, request, send_from_directory, redirect, url_for, render_template, render_template_string
from flask_cors import CORS
from random import randint, randrange
import sqlite3
import datetime
from time import gmtime, time, strftime
app = Flask('smartpen')
CORS(app)

PACKAGE_CREATED = 'PACKAGE_CREATED'
MEASUREMENT = 'MEASUREMENT'
COUNTERFEIT_DETECTED = 'COUNTERFEIT_DETECTED'
INJECTION = 'INJECTION'
SPOILED = 'SPOILED'
EVENT_TYPES=[PACKAGE_CREATED, MEASUREMENT, COUNTERFEIT_DETECTED, INJECTION, SPOILED]

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/create_fake/<int:count>", methods=['GET'])
def create_fake(count):
    txt = ""
    base_utc = time() - (60*60*24 * randrange(30,90))
    for i in range(count):
        id = "abbv%04d" % randint(2000,9000)
        for j in range(0,10):
            event_type = MEASUREMENT
            time_utc = base_utc + 60*60*j
            lat = randrange(34.0,42.0)
            lng = randrange(-120.0,-76.0)
            temp = randrange(0,120)
            light = randint(0,110)
            record_measurement(id,time_utc=time_utc, event_type=event_type, lat=lat, lng=lng, temp=temp, light=light)
        txt += id
    get_db().commit()
    return txt


@app.route("/measurements/<string:id>", methods=["GET"])
def get_measurements(id):
    rslt = []
    cur = get_db().cursor()
    for row in cur.execute("select * from measurements where id = ?", (id,)):
        rslt.append(dict_from_row(row))
    return jsonify(rslt)


@app.route("/measurements", methods=["PUT"])
def set_measurements():
    data = request.json.get('data', [])
    print
    for row in data:
        print(row['id'])
        record_measurement(id=row['id'], time_utc=row['time_utc'], event_type=row['event_type'], lat=row['lat'], lng=row['lng'], temp=row['temp'], light=row['light'])
    return "OK"


@app.route("/ids", methods=["GET"])
def get_ids():
    rslt = []
    cur = get_db().cursor()
    for row in cur.execute("select distinct id from measurements"):
        rslt.append(dict_from_row(row))
    return jsonify(rslt)


@app.route("/show_history/<string:id>", methods=['GET'])
def show_history(id):
    cur = get_db().cursor()
    events = cur.execute("select * from measurements where id = ?", (id,))
    return render_template('show_history.html', events=events)


@app.route("/measuremnts", methods=['DELETE'])
def delete_measurements():
    get_db().execute("delete from measurements where id > 'abbv2000'")


def dict_from_row(row):
    return dict(zip(row.keys(), row))


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
        g.sqlite_db.row_factory = sqlite3.Row
    return g.sqlite_db



@app.template_filter('sec_to_ts')
def sec_to_ts(sec):
    return strftime("%Y-%m-%d %H:%M", gmtime(sec))


@app.template_filter('status_to_color')
def status_to_color(status):
    stats = {
        PACKAGE_CREATED : "info",
        MEASUREMENT : "",
        INJECTION : "success",
        SPOILED : "danger",
        COUNTERFEIT_DETECTED : "danger"
    }
    return stats[status]
