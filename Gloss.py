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
                  '(aux-v)', '(uk)']


    def send_request(self, url, term, tries):
        out = None
        try:
            url = url % parse.quote(term)
            out = request.urlopen(url).read()
        except error.HTTPError:
            if tries+1 > len(self.mirrors):
                raise ConnectionError("Cannot connect to any mirror")
            return self.send_request(self.mirrors[tries+1], term, tries+1)
        return out

    def fetchGlosses(self, term):


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
            gloss = gloss[lineBreakIndex+4::]

        tabIndex = gloss.find('\t')
        cutIndex = -1

        seenOpenBracket = False


        for i in range(len(gloss)):
            character = gloss[i + tabIndex + 1]
            if character.isalpha() and not character.isspace() and not seenOpenBracket:
                tabIndex = i + tabIndex
                break

            if character == '(':
                seenOpenBracket = True
            elif character == ')':
                seenOpenBracket = False

        for i in range(len(gloss)):
            if gloss[i] == ' ' or gloss[i] == ':':
                cutIndex = i
                break

        assert (cutIndex > 0)

        if tabIndex > 0:
            return gloss[0:cutIndex] + ' - ' + gloss[tabIndex + 1::]
        return gloss[0:cutIndex] + ' - ' + gloss[cutIndex+1::]

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
            charVal = ord(gloss[i])

            if gloss[i].isspace():
                if i - 2 >= 0 and gloss[i - 1] == ';' and not gloss[i-2].isspace() and ord(gloss[i - 2]) < 128:
                    return gloss[i:start].lstrip()

                elif not seenOneSpace:
                    seenOneSpace = True
                elif i-2 >= 0 and gloss[i-1] == ';' and ord(gloss[i-2]) > 128:
                    seenOneSpace = False
                else:
                    return gloss[i:start].lstrip()
            elif gloss[i] == ':':
                return gloss[i+1:start].lstrip()
            i-=1
        return gloss[i:start]


        #     if not gloss[i].isspace() and charVal < 58 or (charVal > 59 and charVal < 128):
        #         return ""
        #     elif charVal == 58: #i.e. :
        #         return gloss[i+1:start].lstrip()
        #     i -= 1
        # return gloss[i:start]

    def get_readings(self, gloss):
        readings = []
        for i, c in enumerate(gloss):
            if c == '【':
                prevText = self.get_text_before_reading(gloss, i)
                endIndex = gloss.find('】', i)
                readings.append(prevText + gloss[i:endIndex + 1])

        return readings

    def generate_alt_readings(self, readings):
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
                tst = gloss[lastGoodIndex:i]
                result += gloss[lastGoodIndex:i]
                lastGoodIndex = endIndex+1
        result += gloss[lastGoodIndex::]

        return result
