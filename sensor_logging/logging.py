import sqlite3

db = sqlite3.connect('./data/db')

# def setup():
#     cursor = db.cursor('''
#     CREATE TABLE info(time )
#     ''')


db.close()
