import genanki
import os
import re
import time
from Gloss import Gloss

class CardGenerator:
    def __init__(self, deckName):
        self.model = genanki.Model(1878474795,
                                   'Japanese book v2',
                                   fields=[
                                       {'name': 'Expression'},
                                       {'name': 'Reading'},
                                       {'name': 'Gloss'},
                                       {'name': 'AltReadings'}
                                   ],
                                   templates=[
                                       {
                                           'name': 'Japanese Book',
                                           'qfmt': ' <p style="font-size:30px;text-align:center"><span class=jp>{{Expression}}</span></p>',
                                           'afmt': '<hr id="answer"><p style="font-size:30px;text-align:center"> {{furigana:Reading}}</p><p style="font-size:20px">{{furigana:Gloss}}</p>',
                                       },
                                   ])
        self.deck = genanki.Deck(
            1465567420,
            deckName
        )

    def add_card(self, expression, reading, gloss, altreadings):
        note = genanki.Note(
            model=self.model,
            fields=[expression, reading, gloss, altreadings],
        )
        self.deck.add_note(note)

    def output_deck(self, path):
        self.deck.write_to_file(path)





file = open("帝国の王女.txt", "r")
string = file.read()

string = re.sub(r'《.+?》', '', string)
sentences = re.split('\n|。', string)

cardGen = CardGenerator("星界の紋章")

glosser = Gloss()

count = 0


for sentence in sentences:
    if sentence.isspace():
        continue

    sentence = sentence.strip()

    glosses = glosser.fetchGlosses(sentence)

    definitions = ''
    altreadings = ''

    for gloss in glosses:
        gloss = glosser.remove_dict_annotations(gloss)

        readings = glosser.get_readings(gloss)
        altreadings += glosser.generate_alt_readings(readings)

        gloss = glosser.clean_front(gloss)
        gloss = glosser.clean_verb_stem(gloss)
        gloss = glosser.clean_back(gloss)
        gloss = glosser.remove_furigana(gloss)

        definitions = definitions+'</br></br>'+gloss

    definitions = definitions[10::]


    cardGen.add_card(sentence, "", definitions, altreadings)
    count = count+1

    if count > 50:
        break




cardGen.output_deck("星界の紋章.apkg")