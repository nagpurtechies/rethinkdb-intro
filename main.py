import eventlet; eventlet.monkey_patch()
import rethinkdb as r
from flask import Flask, jsonify
import threading
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
conn = r.connect(host='localhost',
                 port=28015,
                 db='chatrethink')


def watch_db():
    conn = r.connect(host='localhost',
                     port=28015,
                     db='chatrethink')
    for x in r.table('messages').changes().run(conn):
        data = {'text': x['new_val']['text'], 'username': x['new_val']['by']}
        socketio.emit('broadcast event', data, namespace='/broadcast')
thread = threading.Thread(target=watch_db)
thread.daemon = True
thread.start()


@app.route("/")
def hello():
    return app.send_static_file('index.html')


@app.route('/_get_messages')
def get_messages():
    conn = r.connect(host='localhost',
                     port=28015,
                     db='chatrethink')
    messages = r.table('messages').order_by(r.desc('added')).limit(25).run(conn)
    messages = [{'text': message['text'], 'username': message['by']} for message in reversed(list(messages))]
    return jsonify({'messages': messages})


@socketio.on('new message', namespace='/broadcast')
def handle_json(json):
    data = {'text': json['text'], 'added': r.now(), 'by': json['username']}
    r.table('messages').insert(data).run(conn)


if __name__ == "__main__":
    socketio.run(app, debug=True)

