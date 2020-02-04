from setuptools import setup, find_packages

# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()

# specify requirements of your package here
REQUIREMENTS = ['genanki', 'click', 'japana']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'Topic :: Text Processing',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'Programming Language :: Python :: 3',
]

# calling the setup function
setup(name='Japanese-Deck-Builder',
      version='1.0.0',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'deckbuilder = deckbuilder.__main__:create_cards'
          ]
      },
      description='A tool for building Anki decks from Japanese text with well-formatted definitions',
      long_description=long_description,
      url='https://github.com/sduncan56/japanesedeckbuilder',
      author='Shane Duncan',
      author_email='shane.duncan56@gmail.com',
      license='CC0',
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='anki japanese'
      )
