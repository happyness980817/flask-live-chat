from flask import Flask, render_template, request, session, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkeyname"
socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code # generates new codes (not in rooms) with length of "length" parameter.

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        name = request.form.get("name") # dictionary 에서 key 가 "name" 인 애를 가져옴
        code = request.form.get("code")
        join = request.form.get("join", False) 
        # if "join" doesn't exist in the dictionary, it returns 'False' instead of 'None'.
        create = request.form.get("create", False) # join and create don't have a value(key).
        
        if not name: # this means the user didn't give a name or empty.
            return render_template("home.html",error="Please enter a name.")
        
        if join != False and not code: # when user attempts to join but doesn't enter a code
            return render_template("home.html",error="Please enter a room code.")
    
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members":0, "messages": []} # initializes rooms dictionary
        elif code not in rooms:
            return render_template("home.html",error="Room does not exist.")

    return render_template("home.html")

if __name__ == "__main__":
    # socketio.run(app, debug=True) # automatically refreshes
    socketio.run(host='0.0.0.0') # deployment