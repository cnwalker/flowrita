import sys, random

import markovify
import requests

API_ROOT = 'https://api.datamuse.com/'

lyrics_data = open('lyric_data.txt', 'r')
rap_model = markovify.NewlineText(lyrics_data.read())
lyrics_data.close()

def query_datamuse(word, endpoint, mode):
    response = requests.get(API_ROOT + endpoint + '?' + mode + '=' + word).json()
    return response

def get_rhyme(word):
    rhymed_words = query_datamuse(word, 'words', 'rel_rhy')
    similar_words = filter(lambda x: word != x.get('word'), rhymed_words)
    return random.choice(similar_words[:3]).get('word')

def generate_stanza(note):
    stanza = rap_model.make_short_sentence(140, tries=100)
    stanza = stanza.split()
    stanza[-1] = get_rhyme(note.split()[-1])
    return ' '.join(stanza)

if __name__ == '__main__':
    output_song = []
    input_notes = open(sys.argv[1], 'r')
    output = open('fun_notes.txt', 'w+')

    all_notes = input_notes.readlines()
    for note in all_notes:
        output_song.append(note)
        output_song.append(generate_stanza(note) + '\n')
    output.write(''.join(output_song))
