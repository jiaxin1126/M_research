from note import *
from bs4 import BeautifulSoup

class Measure:
    def __init__(self, number=None):
        self.number = number

    def parse_measure(self):
        for n in self.find_all('note'):
            note = Note()
            note.step = n.pitch.step.string
            note.octave = int(n.pitch.octave.string)
            note.duration = int(n.duration.string)
            note.voice = int(n.voice.string)
            note.measure = self.number.string

            if not n.pitch.alter:
                note.alter = 0
            else:
                note.alter = int(n.pitch.alter.string)

    def pitch_height(self):
        '''Calculate pitch's height.'''
        pass

class Sheet:
    def __init__(self, xml=None):
        self.xml = xml
        self.soup = BeautifulSoup(open(self.xml), 'html.parser')

    def parse(self):
        pass

if __name__ == '__main__':
    crab = Sheet('/Users/jiaxin/Documents/M_research/test_file/Crab_Canon.xml')
    print crab.soup
