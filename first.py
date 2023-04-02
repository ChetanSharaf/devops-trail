from flask import Flask, g
import sqlite3
my_var = 0
app = Flask(__name__)
app.config['Database'] = 'myvar.db'


@app.before_first_request
def setup():
    global my_var
    conn = sqlite3.connect(app.config['Database'])
    c = conn.cursor()
    print(app.config['Database'])
    c.execute('SELECT var FROM mytable')
    var = c.fetchall()
    my_var = var[0][0]
    print(my_var)
    conn.close() 


@app.route('/api/hello', methods=['GET'])
def hello():
    global my_var
    my_var += 1
    return f"Hello World {my_var}"

@app.teardown_appcontext
def close_connection(exception):
    conn = sqlite3.connect(app.config['Database'])
    c = conn.cursor()
    c.execute('UPDATE mytable SET var = '+ str(my_var) + ' WHERE id = 1')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run()