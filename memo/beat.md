## How Division
* For example: 2/2
* then in MusicXML file, an 'attribute' can be found
    * 'beat' && 'beat-type'
    * one 'beat-type' is a unit, then there are 'beat' units in one measure

* <code>
```
In the second meusure
    Calculate the whole length of time

# no necessary
strong_beat_points = `whole length of time` / beat -> how many?
for measure in measures[1: ]:
    strong_beats = []
    for note in notes:
        if note.onset % beat == 0:
            strong_beats.append(note)
        else:
            pass
```
* not very good (what about the first measure?)
    * how about check from the last note to the first one?