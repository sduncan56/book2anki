
from urllib import (
    error,
    parse,
    request,
)
import re

class Gloss:
    base_url = 'http://nihongo.monash.edu/cgi-bin/wwwjdic?9ZIH%s'

    junk_terms = ['(P);', 'ED;', 'ED', 'KD', 'ES', 'ST', 'SP', 'MA', 'EV', '(n,adj-no)',
                  '(n)', '(adv-no)', '(adj-no,n)', '(adj-no)',
                  '(v1)', '(vi)', '(v1,vi)', '( adj-i)', '(adj-na)', '(aux)',
                  '(aux-v)']

    def fetchGlosses(self, term):
        url = self.base_url%parse.quote(term)
        out = request.urlopen(url).read()
        result = out.decode("utf8")
        ls = re.findall('<li>(.*?)</li>', result)
        return ls

    def clean_verb_stem(self, gloss):
        txt = '《verb stem》'
        verbSectIndex = gloss.find(txt)
        if verbSectIndex != -1:
            numSecStart = gloss[verbSectIndex::].find('(1)')
            if numSecStart != -1:
                return gloss[0:verbSectIndex] + gloss[verbSectIndex+numSecStart::]


            for counter, c in enumerate(gloss[verbSectIndex+len(txt)::]):
                charVal = ord(c)
                if (charVal >= 65 and charVal <= 90) or (charVal >= 97 and charVal <= 122):
                    return gloss[0:verbSectIndex] + gloss[verbSectIndex+len(txt)+counter::]

        return gloss


    def clean_front(self, gloss):
        gloss = gloss.strip()
        tabIndex = gloss.find('\t')
        cutIndex = -1

        seenOpenBracket = False
        for i in range(len(gloss)):
            character = gloss[i+tabIndex+1]
            if character.isalpha() and not character.isspace() and not seenOpenBracket:
                tabIndex = i+tabIndex
                break
            if character == '(':
                seenOpenBracket = True
            elif character == ')':
                seenOpenBracket = False

        for i in range(len(gloss)):
            if gloss[i] == ' ' or gloss[i] == ':':
                cutIndex = i
                break

        assert(cutIndex > 0)

        cleaned = gloss[0:cutIndex] + ' - ' + gloss[tabIndex + 1::]
        return cleaned

    def remove_dict_annotations(self, gloss):
        for term in self.junk_terms:
            index = 0

            while index != -1:
                index = gloss.find(term)
                if index != -1:
                    gloss = gloss[0:index] + gloss[index + len(term)::]

        return gloss

    def clean_back(self, gloss):
        semicolonIndex = -1
        for i in range(len(gloss)):
            curIndex = len(gloss)-i-1

            if gloss[curIndex] == ';':
                semicolonIndex = curIndex
                break

        cleaned = gloss[0:semicolonIndex]
        return cleaned



