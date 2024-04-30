from typing import Any
import os
from openai import OpenAI
from flask import Flask, jsonify, request
from flask import Blueprint, make_response, Response
from cheroot.wsgi import Server
from cheroot.ssl.builtin import BuiltinSSLAdapter

main = Blueprint(__name__, 'main')

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()
serverPort = 8080

THREADS = 512
CONNECTION_LIMIT = 1024

@main.route('/')
def renderHome():
  return "hey"

def craft_response(data: Any, ok: bool = True):
  response = {"ok": ok, "data": data}
  print("Replying with: {}.".format(response))
  return attach_access_control_headers(jsonify(response))

@staticmethod
def build_cors_preflight_response():
  response = make_response()
  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add('Access-Control-Allow-Headers', "*")
  response.headers.add('Access-Control-Allow-Methods', "*")
  return response

@staticmethod
def attach_access_control_headers(response):
  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Methods", "*")
  return response

def generateResponse(message):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Sei un simpatico assistente di matematica per bambini, il tuo nome é Grillo, dai solo spiegazioni semplici e ami far battute sull'argomento, rispondi solo a domande sulla matematica, se non riguardano la matematica ammetti di non sapere la risposta e cerchi di riportare il discorso sulla matematica."},
      {"role": "user", "content": message}
    ]
  )
  return completion.choices[0].message.content
    
@main.route('/question', methods=['OPTIONS','POST'])
def do_GET():

  response = Response()
  raw_ResponseData = request.get_json()

  resp = generateResponse(raw_ResponseData['content'])

  #response.headers['message'] = json.dumps(dictresp)
  if request.method == "OPTIONS":
    return build_cors_preflight_response()
  
  return craft_response(resp)
  
  
app = Flask(__name__)
app.register_blueprint(main, url_prefix="/")

def start_and_run(host: str = "0.0.0.0", port: int = 5000) -> None:  
  global app
  app = Server(
      (host, port), 
      app, 
      numthreads=THREADS, 
      request_queue_size=CONNECTION_LIMIT
  )

  abs_path = os.path.dirname(os.path.abspath(__file__))
  ssl_cert = os.path.join(abs_path, "fullchain.pem")
  ssl_key = os.path.join(abs_path, "privkey.pem")
  app.ssl_adapter = BuiltinSSLAdapter(ssl_cert, ssl_key, None)

  try:
      app.start()
  except KeyboardInterrupt:
      app.stop()


if __name__ == '__main__':
  start_and_run()
