#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

class Note:
    def __init__(self):
        self.step = None
        self.octave = None
        self.alter = None
        self.voice = None
        self.duration = None
        self.measure = None
        self.height = 0 # tsuika

    def note_print(self):
        return self.__dict__

if __name__ == '__main__':
    note = Note()
    note.step = 'c'
    note.octave = 4
    note.voice = 1
    note.duration = 4
    note.measure = 1
    note.height = 40

    print(note.note_print())
