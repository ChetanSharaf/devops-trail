from flask import Flask, g
import pickle

my_var = 0
app = Flask(__name__)
app.config['Database'] = 'myvar.pickle'
   
@app.before_first_request
def setup():
    global my_var
    try:
        with open(app.config['Database'], 'rb') as f:
            my_var = pickle.load(f)
    
    except FileNotFoundError:
        with open(app.config['Database'], 'wb') as f:
            print("Creating a new pickle file...")
    print("Setting up the app...")

@app.route('/api/hello', methods=['GET'])
def hello():
    global my_var
    my_var += 1
    return f"Hello World {my_var}"

@app.teardown_appcontext
def close_connection(exception):
    with open(app.config['Database'], "wb") as f:
        pickle.dump(my_var, f)

if __name__ == '__main__':
    app.run()