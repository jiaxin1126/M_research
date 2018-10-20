#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from note import *
from bs4 import BeautifulSoup

import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

class Measure:
    def __init__(self, measure, number=None):
        self.measure = measure
        self.number = number
        self.note_array = []

    def parse_measure(self):
        '''
        Every note's info in each measure.
        '''
        note_array = []
        m = self.measure
        for n in m.find_all('note'):
            note = Note()
            if n.find('grace'): # grace
                break
            if n.find('cue'):
                break
            if n.find('rest'):
                note.step = '-'
                note.octave = 0
                note.alter = 0
                note.height = 0
            else: # normal notes
                note.step = n.pitch.step.string
                note.octave = int(n.pitch.octave.string)
                if not n.pitch.alter:
                    note.alter = 0
                else:
                    note.alter = int(n.pitch.alter.string)
                note.height = self.pitch_height(note.step, note.alter, note.octave)
            # for checking
            # print note.step
            note.duration = int(n.duration.string)
            note.voice = int(n.voice.string)
            note.measure = self.number

            note_array.append(note.note_print()) # became dictionary

            # special process: if member of chord
            if n.find('chord'):
                previous, candidate = note_array[-2], note_array[-1]
                previous_height, candidate_height = self.pitch_height(previous['step'], previous['alter'], previous['octave']), \
                                                    self.pitch_height(candidate['step'], candidate['alter'], candidate['octave'])
                if candidate_height > previous_height:
                    del note_array[-2]

        self.note_array = note_array

    def get_measure_notes(self):
        self.parse_measure()
        return self.note_array

    def pitch_height(self, step, alter, octave):
        '''
        Calculate pitch's height.
        May be not necessary.
        '''
            # A0 is 1
        height = 0
        if step == '-':
            height = 0
        if octave == 0:
            if step == 'A':
                height = 0 if alter == 0 else 1
            if step == 'B':
                if alter == 0:
                    height = 3
                else:
                    height = 2 if alter == -1 else 4
        else:
            d_note = {
                'C': 4,
                'D': 6,
                'E': 8,
                'F': 9,
                'G': 11,
                'A': 13,
                'B': 15
            }
            height = d_note[step] + (octave-1) * 12 + alter
        return height

class Sheet:
    def __init__(self, xml=None):
        self.xml = xml
        self.soup = BeautifulSoup(open(self.xml, encoding='utf-8'), 'lxml')
        self.measures = []

    def parse(self):
        s = self.soup
        measures = []
        for m in s.find_all('measure'):
            number = m['number']
            # print number
            measure = Measure(m, number)
            measures.append(measure.get_measure_notes())
        self.measures = measures

    def get_sheet_measures(self):
        self.parse()
        return self.measures

def treble_line(sheet):
    '''
    Sheet should be a list of measures' list, and measures should be a list of notes' dictionary.
    '''
    max_time, min_time = -1 * float('Inf'), float('Inf')
    treble_line = []
    for measures in sheet:
        treble = []
        for notes in measures:
            if notes['voice'] == 1:
                treble.append((notes['step'], notes['alter'], notes['octave'], notes['duration'], notes['height']))
                min_time = min(min_time, notes['duration'])
                max_time = max(max_time, notes['duration'])
        treble_line.append(treble)
    return max_time, min_time, treble_line

def split_into_unit_time(melody_line, unit_time):
    melody = []
    for measures in melody_line:
        line = [] # if some stupid questions come?
        for notes in measures:
            how_many = int(notes[3] / unit_time)
            line += [(notes[0], notes[1], notes[2], notes[-1])] * how_many
        melody.append(line)
    return melody

def dot_plot(melody):
    '''
    Input: list of dictionaries of notes
    eg. [(u'G', -1, 6, 70), (u'G', -1, 6, 70), (u'B', -1, 6, 74), (u'B', -1, 6, 74), (u'D', -1, 6, 65), ...
    '''
    # use pitch height
    all_sheet = []
    all_sheet_without_measures = []
    for measure in melody:
        measure_height = []
        for notes in measure:
            measure_height.append(notes[-1])
            all_sheet_without_measures.append(notes[-1])
        all_sheet.append(measure_height)

    time_seq = []
    for i in range(len(all_sheet_without_measures)):
        time_seq.append(i)
    plt.scatter(time_seq, all_sheet_without_measures)
    plt.show()

if __name__ == '__main__':
    # crab = Sheet('/Users/jiaxin/Documents/M_research/test_file/Crab_Canon.xml')
    # mazeppa = Sheet('/Users/jiaxin/Documents/M_research/test_file/mazeppa.xml')
    black = Sheet('/Users/jiaxin/Desktop/exp/black_key.xml')
    m = black.get_sheet_measures()
    max_time, min_time, treble_line = treble_line(m)
    # for checking
    count = 0
    # for i in treble_line:
    #     count += 1
    #     print count
    #     print i

    # for checking
    # f = open('/Users/jiaxin/Documents/M_research/test_file/m.txt', 'w')
    # for i in treble_line:
    #     f.write(str(i))
    #     f.write('\n')
    # f.close()

    unit_line = split_into_unit_time(treble_line, min_time)
    # print max_time, min_time
    # for i in unit_line:
    #     count += 1
    #     print count
    #     print i
    dot_plot(unit_line)
