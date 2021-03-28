from bs4 import BeautifulSoup
import re
import requests
import unittest

# Task 1: Get the URL that links to the Pokemon Charmander's webpage.
# HINT: You will have to add https://pokemondb.net to the URL retrieved using BeautifulSoup
def getCharmanderLink(soup):
    tags =  soup.find('div', {'class':'infocard-list infocard-list-pkmn-lg'})
    x = tags.find_all ('a', {'class': 'ent-name'})[3]
    return 'https://pokemondb.net' + x['href']

# Task 2: Get the details from the box below "Egg moves". Get all the move names and store
#         them into a list. The function should return that list of moves.
def getEggMoves(pokemon):
    lst = []
    url = 'https://pokemondb.net/pokedex/'+pokemon
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('table', {'class': 'data-table'})[2]
    x = tags.find_all('td', {'class':'cell-name'})

    for item in x:
        k = item.find('a', {'class': 'ent-name'}).text.strip()
        lst.append(k)
    return lst
    

# Task 3: Create a regex expression that will find all the times that have these formats: @2pm @5 pm @10am
# Return a list of these times without the '@' symbol. E.g. ['2pm', '5 pm', '10am']
def findLetters(sentences):
    # initialize an empty list
    lst = []

    # define the regular expression
    x = '@(\d{1,2}\s?[ap]m)'

    # loop through each sentence or phrase in sentences
    for sentence in sentences:

    # find all the words that match the regular expression in each sentence
        k = re.findall(x, sentence)

    # loop through the found words and add the words to your empty list
        for i in k:
            lst.append(i)

    #return the list of the last letter of all words that begin or end with a capital letter
    return lst


def main():
    url = 'https://pokemondb.net/pokedex/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    getCharmanderLink(soup)
    getEggMoves('scizor')

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://pokemondb.net/pokedex/national').text, 'html.parser')

    def test_link_Charmander(self):
        self.assertEqual(getCharmanderLink(self.soup), 'https://pokemondb.net/pokedex/charmander')

    def test_egg_moves(self):
        self.assertEqual(getEggMoves('scizor'), ['Counter', 'Defog', 'Feint', 'Night Slash', 'Quick Guard'])

    def test_findLetters(self):
        self.assertEqual(findLetters(['Come eat lunch at 12','there"s a party @2pm', 'practice @7am','nothing']), ['2pm', '7am'])
        self.assertEqual(findLetters(['There is show @12pm if you want to join','I will be there @ 2pm', 'come at @3 pm will be better']), ['12pm', '3 pm'])

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)