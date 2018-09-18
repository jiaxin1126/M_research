class Note:
    def __init__(self):
        self.step = None
        self.octave = None
        self.alter = None
        self.voice = None
        self.duration = None
        self.measure = None

    def note_print(self):
        return self.__dict__

if __name__ == '__main__':
    note = Note()
    note.step = 'c'
    note.octave = 4
    note.voice = 1
    note.duration = 4
    note.measure = 1

    print note.note_print()
