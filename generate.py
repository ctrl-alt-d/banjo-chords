# -*- coding: UTF-8 -*-.
import itertools

#SIMBOLS
NOTES      = [ 'A', 'bB', 'B', 'C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G' ]
NOTES_UP   = [ 'A', '#A', 'B', 'C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G' ]
NOTES_DOWN = [ 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab' ]
STRINGS = [ 'D', 'B', 'G', 'C' ]
TOTAL_FRETS = 22

NUM_SEMITONES = 12
ROOT = 0 # at 0 semitones
MINOR_THIRD = 3 # 3 semitones
MAJOR_THIRD = 4 # 4 semitones
PERFECT_FIFTH = 7

CHORDS_TYPES = [ {'Name': 'Major', 'Simbol': '', 'Intervals': [ ROOT, MAJOR_THIRD, PERFECT_FIFTH ] },
                 {'Name': 'Menor', 'Simbol': 'm', 'Intervals': [ ROOT, MINOR_THIRD, PERFECT_FIFTH ] }
                ]

MAX_FRETS = 4

#notes de cada corda
STRING_NOTES = []

n_string = 0
for n_string in range( 0 , len( STRINGS ) ):
    base_note = STRINGS[ n_string ]
    base_note_index = NOTES.index( base_note )
    STRING_NOTES.append( [] )
    for f in range( 0, TOTAL_FRETS ):
        STRING_NOTES[n_string].append( NOTES[  ( base_note_index + f ) % NUM_SEMITONES  ] )

#per cada acord:

all_solucions = []  #[ { 'Root': '#C', 'Chord': 'm', 'Solutions': [  ( (0,C) ,(0,G), (1,C) ,(2,E) ), ( ( .... ] }    ]

for root_note in NOTES:
    root_note_index = NOTES.index( root_note )
    #per cada tipus d'acord ....
    for acord in CHORDS_TYPES:
        solucions = []  #   ( (0,C) ,(0,G), (1,C) ,(2,E) ), ( ( ....

        needed_notes = set()
        #calcular notes les notes que calen
        for needed_note in acord['Intervals']:
            needed_notes.add( NOTES[  ( root_note_index + needed_note ) % NUM_SEMITONES  ]    )
        #print ( 'Per fer ', root_note, acord['Name'], ' calen', needed_notes )

        #des del traste 0 fins al darrer
        for f in range( 0, TOTAL_FRETS - MAX_FRETS ):
            #buscar fins a MAX_FRETS
            notes_per_corda = [ [] for _ in STRINGS ]  # [ [ (0, 'G'), (3,'B') ],  [ .... ]  ]
            for delta_corda in range( 0, MAX_FRETS ):
                for corda in range( 0, len( STRINGS) ):
                    if STRING_NOTES[corda][f+delta_corda] in needed_notes:
                        notes_per_corda[corda].append( ( f+delta_corda,
                                                         STRING_NOTES[corda][f+delta_corda]
                                                        ) )

            #buscar solucions:
            if all( notes_per_corda ):
                for possible_solucio in itertools.product(*notes_per_corda):
                    #agafo les notes:
                    notes_de_la_possible_solucio = set( [ x[1] for x in possible_solucio ]  )
                    if not ( needed_notes - notes_de_la_possible_solucio ):
                        l =  list( [ (x[0],x[1]) for x in possible_solucio ]  )
                        l.reverse()
                        if l not in solucions:
                            solucions.append( l )

        all_solucions.append( {  'Root': root_note,
                                 'Chord': acord['Simbol'],
                                 'Chord Notes': needed_notes,
                                 'Solutions': solucions } )


#pintar totes les solucions (index)
for a_solution in all_solucions:
    text="{root}{chord} ({notes})".format(
                    chord=a_solution['Chord'],
                    root=a_solution['Root'],
                    notes=' '.join( a_solution['Chord Notes'] )
                                            )
    print( "* [{0}](#{1})".format( text, text.replace(" ","-").replace("#","").replace("(","").replace(")","").lower() ) )


#pintar totes les solucions (acords)
for a_solution in all_solucions:
    text="{root}{chord} ({notes})".format(
                    chord=a_solution['Chord'],
                    root=a_solution['Root'],
                    notes=' '.join( a_solution['Chord Notes'] )
                                            )
    print( "### {0}".format( text ) )
    for s in a_solution['Solutions']:
        print( '    ' + ' '.join( [ "{0: >3}".format(x[0]) for x in s] ) )
        print( '    ' + ' '.join( [ "{0: >3}".format(x[1]) for x in s] ) )
        print('')
