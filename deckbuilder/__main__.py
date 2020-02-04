
import click

from deckbuilder.Gloss import Gloss
from deckbuilder.CardGenerator import CardGenerator
from deckbuilder.DeckBuilder import DeckBuilder


@click.command()
@click.argument('filepath')
@click.option('-output', default='deck', help='output filename')
@click.option('-deckid', default=-1, help='an integer than should be unique (i.e. no other deck has the same one). If '
                                          'you don\'t specify, a random one will be generated with no guarantee of '
                                          'uniqueness')
@click.option('-jlpt', default=5, help='filters out cards below the given JLPT level from the main gloss field. e.g. '
                                       '"2" will filter out words from the N3, N4, and N5 sets')
@click.option('-threshold', default=100, help='filters out cards that occur more times than this in the document from '
                                              'the main gloss field')
@click.option('-furiganadelim', default='《》', help='the two characters that indicate furigana in the text. All '
                                                   'instances of these characters and everything inside them will be '
                                                   'deleted')
def create_cards(filepath, output, deckid, jlpt, threshold, furiganadelim):
    cardGen = CardGenerator(output, deckid)
    glosser = Gloss()

    deckBuilder = DeckBuilder(glosser)
    sentences = deckBuilder.get_sentences_from_file(filepath, jlpt, threshold, furiganadelim)
    deckBuilder.process_sentences(sentences, cardGen)

    cardGen.output_deck(output+".apkg")


if __name__ == '__main__':
    create_cards()