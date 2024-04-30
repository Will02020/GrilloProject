from typing import Any
import openai
import dotenv
import os
from openai import OpenAI
from http.server import BaseHTTPRequestHandler, HTTPServer
from flask import Flask, jsonify, request
from flask import render_template, Blueprint, make_response, Response
import flask_cors

main = Blueprint(__name__, 'main')

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()
hostName = "localhost"
serverPort = 8080

@main.route('/')
def renderHome():
  return render_template('index.html')

@main.route('/primi')
def renderArgs():
  return render_template('primi.html')

@main.route('/insiemi')
def renderInsiemi():
  return render_template('insiemi.html')

@main.route('/diagramma')
def renderDiagramma():
  return render_template('diagramma.html')

@main.route('/naturali')
def renderNaturali():
  return render_template('naturali.html')

@main.route('/decimali')
def renderDecimali():
  return render_template('decimali.html')

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
  response.headers.add('Access-Control-Allow-Headers', "*")
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
@flask_cors.cross_origin()
def do_GET():

  response = Response()
  raw_ResponseData = request.get_json()

  resp = generateResponse(raw_ResponseData['content'])
  
  
  #response.headers['message'] = json.dumps(dictresp)
  
  return craft_response(resp)
  
  

