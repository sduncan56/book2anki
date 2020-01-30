from urllib import (
    error,
    parse,
    request,
)
import re


class Gloss:
    mirrors = ['http://nihongo.monash.edu/cgi-bin/wwwjdic?9ZIH%s', 'http://wwwjdic.biz/cgi-bin/wwwjdic?9ZIH%s']

    junk_terms = ['(P);', '(P)', 'ED;', 'ED', 'KD', 'ES', 'ST', 'SP', 'MA', 'EV', '(n,adj-no)',
                  '(v5r,vi,aux-v)', '(n)', '(adv-no)', '(adj-no,n)', '(adj-no)',
                  '(v1)', '(vi)', '(v1,vi)', '( adj-i)', '(adj-na)', '(aux)',
                  '(aux-v)', '(uk)', '(n-t)', '(adj-no,adj-na,n)']

    ignore_set = set()

    def populate_ignore_set(self, frequency_list, jlpt, freq_threshold):
        for entry in frequency_list:
            allowWord = entry['frequency'] < freq_threshold

            level = entry['jlpt']
            if level is not None:
                if int(level[1]) > jlpt:
                    allowWord = False

            if not allowWord:
                continue

            self.ignore_set.add(entry['word'])

    def remember_word(self, gloss):
        wordIndex = gloss.find(' ')
        self.ignore_set.add(gloss[0:wordIndex])

    def send_request(self, url, term, tries):
        out = None
        try:
            url = url % parse.quote(term)
            out = request.urlopen(url).read()
        except error.HTTPError:
            if tries + 1 > len(self.mirrors):
                raise ConnectionError("Cannot connect to any mirror")
            return self.send_request(self.mirrors[tries + 1], term, tries + 1)
        return out

    def fetch_glosses(self, term):
        out = self.send_request(self.mirrors[0], term, 0)

        result = out.decode("utf8")
        ls = re.findall('<li>(.*?)</li>', result)
        return ls

    def clean_verb_stem(self, gloss):
        txt = '《verb stem》'
        verbSectIndex = gloss.find(txt)
        if verbSectIndex != -1:
            numSecStart = gloss[verbSectIndex::].find('(1)')
            if numSecStart != -1:
                return gloss[0:verbSectIndex] + gloss[verbSectIndex + numSecStart::]

            for counter, c in enumerate(gloss[verbSectIndex + len(txt)::]):
                charVal = ord(c)
                if (charVal >= 65 and charVal <= 90) or (charVal >= 97 and charVal <= 122):
                    return gloss[0:verbSectIndex] + gloss[verbSectIndex + len(txt) + counter::]

        return gloss

    def clean_front(self, gloss):
        gloss = gloss.strip()

        lineBreakIndex = gloss.find('<br>')
        if lineBreakIndex != -1:
            gloss = gloss[lineBreakIndex + 4::]

        firstSpaceIndex = gloss.find(' ')
        if gloss[firstSpaceIndex::].find('from') == 1:
            gloss = gloss[firstSpaceIndex + 6::]
            if gloss[0] == ":":
                gloss = gloss[1::]
            gloss = gloss.lstrip()

        tabIndex = gloss.find('\t')
        cutIndex = -1

        seenOpenBracket = False

        for i in range(len(gloss)):
            if i + tabIndex + 1 < len(gloss):
                character = gloss[i + tabIndex + 1]
                if character.isalpha() and not character.isspace() and not seenOpenBracket:
                    tabIndex = i + tabIndex
                    break

                if character == '(':
                    seenOpenBracket = True
                elif character == ')':
                    seenOpenBracket = False

        for i in range(len(gloss)):
            if gloss[i] == ' ' or gloss[i] == ':' or gloss[i] == ';':
                cutIndex = i
                break

        assert (cutIndex > 0)

        # if there is no convenient tab, use the first english character (or '{') instead.
        # argument could be made that we should do this anyway
        if tabIndex == -1:
            for i in range(cutIndex + 1, len(gloss)):
                c = gloss[i]
                charOrd = ord(gloss[i])
                if charOrd >= 65 and charOrd <= 90 or charOrd >= 97 and charOrd <= 123:
                    tabIndex = i - 1
                    break

        if gloss[tabIndex] == '{' or gloss[tabIndex] == '(':
            gloss = gloss[0:tabIndex] + ' ' + gloss[tabIndex::]

        return gloss[0:cutIndex] + ' - ' + gloss[tabIndex + 1::]

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
            curIndex = len(gloss) - i - 1

            if gloss[curIndex] == ';':
                semicolonIndex = curIndex
                break

        cleaned = gloss[0:semicolonIndex]
        return cleaned

    def get_text_before_reading(self, gloss, start):
        i = start
        seenOneSpace = False
        while i > 0:
            if gloss[i].isspace():
                if i - 2 >= 0 and gloss[i - 1] == ';' and not gloss[i - 2].isspace() and ord(gloss[i - 2]) < 128:
                    return gloss[i:start].lstrip()

                elif not seenOneSpace:
                    seenOneSpace = True
                elif i - 2 >= 0 and gloss[i - 1] == ';' and ord(gloss[i - 2]) > 128:
                    seenOneSpace = False
                else:
                    return gloss[i:start].lstrip()
            elif gloss[i] == ':':
                return gloss[i + 1:start].lstrip()
            i -= 1
        return gloss[i:start]

    def get_readings(self, gloss):
        readings = []
        for i, c in enumerate(gloss):
            if c == '【':
                prevText = self.get_text_before_reading(gloss, i)
                endIndex = gloss.find('】', i)
                readings.append(prevText + gloss[i:endIndex + 1])

        return readings

    def generate_alt_readings(self, readings):
        if len(readings) == 0:
            return ''

        altreadings = ''

        for reading in readings:
            altreadings = altreadings + ' | ' + reading
        return altreadings[3::] + '</br>'

    def remove_furigana(self, gloss):
        result = ''
        lastGoodIndex = 0
        for i, c in enumerate(gloss):
            if c == '【':
                endIndex = gloss.find('】', i)
                result += gloss[lastGoodIndex:i]
                lastGoodIndex = endIndex + 1
        result += gloss[lastGoodIndex::]

        return result

    def is_known_word(self, gloss):
        wordIndex = gloss.find(' ')
        return True if gloss[0:wordIndex] in self.ignore_set else False
