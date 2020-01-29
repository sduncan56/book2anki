import re
from japana.word_count import word_count
import click

from Gloss import Gloss

from CardGenerator import CardGenerator



class DeckBuilder:
    glosser = Gloss()

    def get_sentences_from_file(self, path):
        file = open(path, "r")
        string = file.read()

        string = re.sub(r'《.+?》', '', string)
        sentences = re.split('\n|。', string)

        words = word_count(string, True, False, False)
        self.glosser.populate_ignore_set(words)

        return sentences

    def process_sentences(self, sentences, cardGenerator):

        for sentence in sentences:
            if sentence.isspace():
                continue

            sentence = sentence.strip()

            glosses = self.glosser.fetchGlosses(sentence)

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
def create_cards(filepath, output):
    cardGen = CardGenerator("星界の紋章")

    deckBuilder = DeckBuilder()
    sentences = deckBuilder.get_sentences_from_file(filepath)
    deckBuilder.process_sentences(sentences, cardGen)

    cardGen.output_deck(output+".apkg")


if __name__ == '__main__':
    create_cards()