from flask import Flask, render_template, request, redirect, url_for
from flask import redirect, jsonify

import psycopg2
import sys

from scrapping.main import *

app = Flask(__name__)


@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/resultat', methods=['GET'])
def envoie_email():
     
    print('************* entra page resultat *************')
    # il faut qui execute l envoie d'email
    email = request.args.get('email')
    # email = request.form['email']
    
    #print(request.args.get('email'))
    print(email)
    print('envoyer le message à '+str(email))
    #obj_email = main(email)
    #reponse = "Envoye Reussie" if obj_email else "Email PAS Envoyé - Pas des nouveau messages"

    return 'VAMOS!!!' #reponse 


# @app.route('/apivideo', methods=['GET'])
# def api_video():
#     dict_videos = []
#     cursor = mybdd.cursor(dictionary=True)
#     print('Curseur --->', cursor)
#     sql = 'select * from videos'
#     cursor.execute(sql)

#     for i in cursor:
#         dict_videos.append(i)

#     resp = jsonify(dict_videos)
#     return resp


if __name__ == '__main__':
    print('VAMOS !!!', file=sys.stderr)
    app.run(host='0.0.0.0', port=4000, debug=True)
