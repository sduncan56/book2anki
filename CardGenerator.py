
import genanki
from random import randint

class CardGenerator:
    def __init__(self, deckName, deckId):

        if deckId == -1:
            deckId = randint(0, 9999999999)

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
            deckId,
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