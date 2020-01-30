
import re
from japana.word_count import word_count
import click

class DeckBuilder:
    def __init__(self, glosser):
        self.glosser = glosser

    def get_sentences_from_file(self, path, jlpt, threshold, furiganadelim):
        click.echo('Reading file: '+path)
        file = open(path, "r")
        string = file.read()

        if len(furiganadelim) != 0 and len(furiganadelim) != 2:
            raise Exception("Must be 0 or 2 characters for furigana delimiters")

        if furiganadelim:
            reg = (furiganadelim[0], '.+?', furiganadelim[1])
            string = re.sub(''.join(reg), '', string)
        sentences = re.split('\n|。', string)

        click.echo('Analysing text for word frequency:')
        words = word_count(string, True, False, False)
        self.glosser.populate_ignore_set(words, jlpt, threshold)

        return sentences

    def process_sentences(self, sentences, cardGenerator):
        click.echo('Processing sentence definitions:')
        with click.progressbar(sentences) as bar:
            for sentence in bar:
                if sentence.isspace():
                    continue

                sentence = sentence.strip()

                glosses = self.glosser.fetch_glosses(sentence)

                definitions = altreadings = knowndefs = ''
                altreadings, definitions, knowndefs = self.process_glosses(altreadings, definitions, glosses, knowndefs)

                definitions = definitions[10::]
                knowndefs = knowndefs[10::]

                cardGenerator.add_card(sentence, "", definitions, altreadings, knowndefs)

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