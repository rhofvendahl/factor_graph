from flask import Flask, render_template
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'

from flask_socketio import SocketIO, emit
socketio = SocketIO(app)

import os
import dialogflow_v2 as dialogflow

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keys/service_account_key.json'
session_client = dialogflow.SessionsClient()
PROJECT_ID = 'factor-graph-713c9'

import spacy
from spacy import displacy

print('loading en_core_web_md...')
nlp = spacy.load('en_core_web_sm')
print('done')

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('msg_user', namespace='/chat')
def test_message(msg):
    content = msg['content']
    session = session_client.session_path(PROJECT_ID, msg['session_id'])
    text_input = dialogflow.types.TextInput(text=msg['content'], language_code='en')
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    emit('msg_agent', {'content': response.query_result.fulfillment_text})

    doc = nlp(content)

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

    emit('msg_agent', {
        'content': content + content + content,
        'parse': displacy.parse_deps(doc)
    })

if __name__ == "__main__":
    socketio.run(app)
    # app.run()
