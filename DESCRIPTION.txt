# Japanese Deck Builder

Reads a text file and turns it into Anki cards. Automatically retrieves glosses from wwwjdic and reformats them in a cleaner way, plus moves definitions of words that have already been encountered, or are below a given JLPT level or occur extremely frequent in the document, to a different field.

Can be installed through Pypi with:

`pip install Japanese-Deck-Builder`

Usage:

`deckbuilder FILENAME`

Options:
```
  -output TEXT         output filename
  -deckid INTEGER      an integer than should be unique (i.e. no other deck
                       has the same one). If you don't specify, a random one
                       will be generated with no guarantee of uniqueness
  -jlpt INTEGER        filters out cards below the given JLPT level from the
                       main gloss field. e.g. "2" will filter out words from
                       the N3, N4, and N5 sets
  -threshold INTEGER   filters out cards that occur more times than this in
                       the document from the main gloss field
  -furiganadelim TEXT  the two characters that indicate furigana in the text.
                       All instances of these characters and everything inside
                       them will be deleted
```

Note that there is currently a bug in Genanki which causes cards to not be in order. This might matter if you're processing a large amount of text (say, a novel) - things will be mostly in-order, but some chunks will not. If this matters to you, code to fix this can be found in this pull request: https://github.com/kerrickstaley/genanki/pull/35

If you don't care about ordering at all, consider MorphMan: https://ankiweb.net/shared/info/900801631


This is intended to be used with the Japanese Support Anki addon:

https://ankiweb.net/shared/info/3918629684

If you are new to Japanese, you should use subs2srs instead:

http://subs2srs.sourceforge.net/