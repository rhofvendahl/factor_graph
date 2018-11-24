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

import clausiepy as clausie
clauses = clausie.clausie('Albert Einstein died in Princeton in 1955.')
print(clauses)
propositions = clausie.extract_propositions(clauses)
clausie.print_propositions(propositions)

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

    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.pos_)

    # nodes = []
    # for chunk in doc.noun_chunks:
    #     nodes += [{'id': chunk.text, 'label': chunk.text}]
    #     edges += [{'from': chunk.root.head.text, 'to': chunk.text, 'arrow'}]
    #     COUNTER += 1

    nodes = []
    edges = []
    for token in doc:
        if token.pos_ in ['PRON', 'NOUN']:
            color = 'pink'
        elif token.pos_ == 'VERB':
            color = 'lightblue'
        else:
            color = 'lightgrey'
        nodes += [{
            'id': token.idx,
            'label': token.text,
            'title': token.pos_,
            'color': color
        }]
        edges += [{
            'from': token.head.idx,
            'to': token.idx,
            'label': token.dep_,
            'arrows': 'to'
        }]

    clauses = clausie.clausie(content)
    for clause in clauses:
        print(clause)
    propositions = clausie.extract_propositions(clauses)
    print(type(propositions[0]['subject']))
    print('AAAAAAAAAAAAAAAAAAAAAAAAA')
    for proposition in propositions:
        print(proposition)
    clausie.print_propositions(propositions)

    emit('msg_agent', {
        'content': content + content + content,
        'parse': displacy.parse_deps(doc),
        'nodes': nodes,
        'edges': edges
    })

if __name__ == "__main__":
    socketio.run(app)
    # app.run()
