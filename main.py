import genanki
import os
import re
import time

class CardGenerator:
    def __init__(self, deckName):
        self.model = genanki.Model(1878474794,
                                   'Japanese book',
                                   fields=[
                                       {'name': 'Expression'},
                                       {'name': 'Reading'},
                                       {'name': 'Gloss'},
                                   ],
                                   templates=[
                                       {
                                           'name': 'Japanese Book',
                                           'qfmt': ' <p style="font-size:30px;text-align:center"><span class=jp>{{Expression}}</span></p>',
                                           'afmt': '<hr id="answer"><p style="font-size:30px;text-align:center"> {{furigana:Reading}}</p>{{Gloss}}',
                                       },
                                   ])
        self.deck = genanki.Deck(
            1465567420,
            deckName
        )

    def add_card(self, expression, reading, gloss):
        note = genanki.Note(
            model=self.model,
            fields=[expression, reading, gloss],
        )
        self.deck.add_note(note)

    def output_deck(self, path):
        self.deck.write_to_file(path)


file = open("帝国の王女.txt", "r")
string = file.read()

string = re.sub(r'《.+?》', '', string)
sentences = re.split('\n|。', string)

cardGen = CardGenerator("星界の紋章")


count = 0
for sentence in sentences:
    if sentence.isspace():
        continue

    sentence = sentence.strip()
    cardGen.add_card(sentence, "")


cardGen.output_deck("星界の紋章.apkg")