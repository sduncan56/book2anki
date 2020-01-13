import genanki
import os
import re
import time
from Gloss import Gloss
from japana.word_count import word_count

class CardGenerator:
    def __init__(self, deckName):
        self.model = genanki.Model(1878474795,
                                   'Japanese book v2',
                                   fields=[
                                       {'name': 'Expression'},
                                       {'name': 'Reading'},
                                       {'name': 'Gloss'},
                                       {'name': 'AltReadings'},
                                       {'name': 'Known Definitions'}
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

    def add_card(self, expression, reading, gloss, altreadings, knowndefs):
        note = genanki.Note(
            model=self.model,
            fields=[expression, reading, gloss, altreadings, knowndefs],
        )
        self.deck.add_note(note)

    def output_deck(self, path):
        self.deck.write_to_file(path)





file = open("帝国の王女.txt", "r")
string = file.read()

string = re.sub(r'《.+?》', '', string)
sentences = re.split('\n|。', string)

words = word_count(string, True, False, False)


cardGen = CardGenerator("星界の紋章")

glosser = Gloss()

glosser.populate_ignore_set(words)

count = 0


for sentence in sentences:
    if sentence.isspace():
        continue

    sentence = sentence.strip()

    glosses = glosser.fetchGlosses(sentence)

    definitions = ''
    altreadings = ''
    knowndefs = ''

    for gloss in glosses:
        try:
            gloss = glosser.remove_dict_annotations(gloss)

            readings = glosser.get_readings(gloss)
            altreadings += glosser.generate_alt_readings(readings)

            gloss = glosser.clean_front(gloss)

            gloss = glosser.clean_verb_stem(gloss)
            gloss = glosser.clean_back(gloss)
            gloss = glosser.remove_furigana(gloss)
        except Exception as e:
            print("Error with term: " + gloss)
            raise e

        if glosser.is_known_word(gloss):
            knowndefs += '</br></br>' + gloss
        else:
            definitions += '</br></br>'+gloss
            glosser.remember_word(gloss)

    definitions = definitions[10::]
    knowndefs = knowndefs[10::]


    cardGen.add_card(sentence, "", definitions, altreadings, knowndefs)
    # count = count+1
    # if count > 200:
    #     break




cardGen.output_deck("星界の紋章.apkg")