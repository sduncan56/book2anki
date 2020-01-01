
from urllib import (
    error,
    parse,
    request,
)
import re

class Gloss:
    base_url = 'http://nihongo.monash.edu/cgi-bin/wwwjdic?9ZIH%s'

    def fetchGlosses(self, term):
        url = self.base_url%parse.quote(term)
        out = request.urlopen(url).read()
        result = out.decode("utf8")
        ls = re.findall('<li>(.*?)</li>', result)
        return ls

    def clean_gloss_front(self, gloss):
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