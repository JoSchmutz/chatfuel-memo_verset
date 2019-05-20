# todo : parser un message texte qui contient une référence

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import flask_jsonpify

from App import *
# from versify.util.Dbt import Dbt
app = Flask(__name__)
api = Api(app)

# verse_sent = ''

class Verses(Resource):

    def get(self):
        # r est la chaîne que l'API bible nous a renvoyé

        # verset_brut =  remove_tags(htmlValue):
        # headers = {'api-key': '0fff648164b9a80b9b89b5ddce43c9e7',}
        # response = requests.get('https://api.scripture.api.bible/v1/bibles/2ef4ad5622cfd98b-01/'+, headers=headers)
        # utiliser le dbt de python versify de willy
        # resp = response.json()
        # htmlValue = resp['content']  def remove_tags(text):''.join(xml.etree.ElementTree.fromstring(text).itertext())
        # resp = r.json()
        # htmlValue = resp['content']  
        # def remove_tags(text): ''.join(xml.etree.ElementTree.fromstring(text).itertext())
        # verset_brut =  remove_tags(htmlValue):
        # print(dbt.find_verse("DBY", "1 Timothée", 2, 1))

        # txt = verse_sent
        # txt = "Hello world c'est MemoVerset sur Chatfuel"
        verse = str(Dbt.find_verse("DBY", "Jean", 3, 16))
        str_verse = verse[1:-1]
        new_vers = complexify_verse(2, str_verse)
        # print(new_vers)

        result =  {"messages": [{"text": new_vers},]}
        return jsonify(result)

class Verse_complexified(Resource):
    def get(self, livre, chapitre, verset, complexity):

        verse = str(Dbt.find_verse("DBY", str(livre), int(chapitre), int(verset)))
        str_verse = verse[1:-1]
        new_vers = complexify_verse(int(complexity), str_verse)
        print("new verse = ", new_vers)

        result =  {"set_attributes": {"verse_txt": str_verse},"messages": [{"text": new_vers}]}
        return jsonify(result)

class Texte_complexified(Resource):
    def get(self, texte):
        texte = texte
        complexity = 2
        # verse_final
        # complexified_verse = complexify_verse(complex, verse_final)
        # complexified_verse = complexify_verse(complexity, verse)
        # print("complexity = ", complexity)
        # verse = str(Dbt.find_verse("DBY", "Jean", 3, 16))
        # str_verse = verse[1:-1]
        new_vers = complexify_verse(int(complexity), texte)
        print("new verse = ", new_vers)

        result =  {"messages": [{"text": new_vers}]}
        return jsonify(result)


class Verse_ref(Resource):
    def get(self, livre, chapitre, verset):
        # verse_final
        # complexified_verse = complexify_verse(complex, verse_final)
        # complexified_verse = complexify_verse(complexity, verse)
        # verse_txt_from_verse_ref() #write function that get verse ref
        # verse = str(Dbt.find_verse("DBY", "Jean", 3, 16))
        verse = str(Dbt.find_verse("DBY", str(livre), int(chapitre), int(verset)))
        str_verse = verse[1:-1]
        print("verse_ref_sent = ", str_verse)

        # new_vers = complexify_verse(int(complexity), str_verse)
        # print("new verse = ", new_vers)

        result =  {"set_attributes": {"verse_txt": str_verse},"messages": [{"text": str_verse}]}
        return jsonify(result)

api.add_resource(Verses, '/verses')
api.add_resource(Verse_ref, '/save_verse_txt/<livre>/<chapitre>/<verset>') #cette route permet de sauvegarder dans un attribut le verset en question
api.add_resource(Verse_complexified, '/complexity/<livre>/<chapitre>/<verset>/<complexity>')



api.add_resource(Texte_complexified, '/text/<verse_txt>') #ici on doit renvoyer le texte complexifié


if __name__ == '__main__':
     app.run(port='5002')

# Dans l'url utiliser ?variable=value
