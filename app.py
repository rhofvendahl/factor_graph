from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# import os
# import dialogflow_v2 as dialogflow

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
#
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keys/service_account_key.json'
# session_client = dialogflow.SessionsClient()
# PROJECT_ID = 'loopy-nl-agent-1-0'
#
# @app.route('/loopy')
# def loopy():
#     return render_template('loopy.html')

@app.route('/')
def index():
    return render_template('index.html')


# @socketio.on('msg_user', namespace='/chat')
# def test_message(msg):
#     session = session_client.session_path(PROJECT_ID, msg['session_id'])
#     text_input = dialogflow.types.TextInput(text=msg['content'], language_code='en')
#     query_input = dialogflow.types.QueryInput(text=text_input)
#     response = session_client.detect_intent(session=session, query_input=query_input)
#
#     emit('msg_agent', {'content': response.query_result.fulfillment_text})

if __name__ == "__main__":
    # socketio.run(app)
    app.run()
