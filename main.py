import re
from japana.word_count import word_count
import click

from Gloss import Gloss

from CardGenerator import CardGenerator



class DeckBuilder:

    def __init__(self, glosser):
        self.glosser = glosser

    def get_sentences_from_file(self, path, jlpt, threshold, furiganadelim):
        file = open(path, "r")
        string = file.read()

        if len(furiganadelim) != 0 and len(furiganadelim) != 2:
            raise Exception("Must be 0 or 2 characters for furigana delimiters")

        if furiganadelim:
            reg = (furiganadelim[0], '.+?', furiganadelim[1])
            string = re.sub(''.join(reg), '', string)
        sentences = re.split('\n|。', string)

        words = word_count(string, True, False, False)
        self.glosser.populate_ignore_set(words, jlpt, threshold)

        return sentences

    def process_sentences(self, sentences, cardGenerator):

        for sentence in sentences:
            if sentence.isspace():
                continue

            sentence = sentence.strip()

            glosses = self.glosser.fetch_glosses(sentence)

            definitions = altreadings = knowndefs = ''
            altreadings, definitions, knowndefs = self.process_glosses(altreadings, definitions, glosses, knowndefs)

            definitions = definitions[10::]
            knowndefs = knowndefs[10::]


            cardGenerator.add_card(sentence, "", definitions, altreadings, knowndefs)
            # count = count+1
            # if count > 200:
            #     break

    def process_glosses(self, altreadings, definitions, glosses, knowndefs):
        for gloss in glosses:
            try:
                gloss = self.glosser.remove_dict_annotations(gloss)

                readings = self.glosser.get_readings(gloss)
                altreadings += self.glosser.generate_alt_readings(readings)

                gloss = self.glosser.clean_front(gloss)

                gloss = self.glosser.clean_verb_stem(gloss)
                gloss = self.glosser.clean_back(gloss)
                gloss = self.glosser.remove_furigana(gloss)
            except Exception as e:
                print("Error with term: " + gloss)
                raise e

            if self.glosser.is_known_word(gloss):
                knowndefs += '</br></br>' + gloss
            else:
                definitions += '</br></br>' + gloss
                self.glosser.remember_word(gloss)
        return altreadings, definitions, knowndefs



@click.command()
@click.argument('filepath')
@click.option('-output', default='deck', help='output filename')
@click.option('-jlpt', default=5, help='filters out cards below the given JLPT level from the main gloss field. e.g. '
                                       '"2" will filter out words from the N3, N4, and N5 sets')
@click.option('-threshold', default=100, help='filters out cards that occur more times than this in the document from '
                                              'the main gloss field')
@click.option('-furiganadelim', default='《》', help='the two characters that indicate furigana in the text. All '
                                                   'instances of these characters and everything inside them will be '
                                                   'deleted')
def create_cards(filepath, output, jlpt, threshold, furiganadelim):
    cardGen = CardGenerator(output)
    glosser = Gloss()

    deckBuilder = DeckBuilder(glosser)
    sentences = deckBuilder.get_sentences_from_file(filepath, jlpt, threshold, furiganadelim)
    deckBuilder.process_sentences(sentences, cardGen)

    cardGen.output_deck(output+".apkg")


if __name__ == '__main__':
    create_cards()