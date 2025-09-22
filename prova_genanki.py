import genanki
import random

nome = "Capitali del mondo"

# --- PASSO 1: Definire il Modello ---
# Ogni modello ha un ID unico e un nome.
# L'ID deve essere un numero intero casuale.
# Si definiscono i campi ('fields') e i template delle carte ('templates').

my_model = genanki.Model(
  random.randrange(1 << 30, 1 << 31), # ID del modello
  'Modello Semplice', # Nome del modello
  fields=[
    {'name': 'Domanda'},
    {'name': 'Risposta'},
  ],
  templates=[
    {
      'name': 'Carta 1',
      'qfmt': '{{Domanda}}', # Formato del fronte della carta
      'afmt': '{{FrontSide}}<hr id="answer">{{Risposta}}', # Formato del retro
    },
  ])

# --- PASSO 2: Creare il Mazzo ---
# Ogni mazzo ha un ID unico e un nome.

my_deck = genanki.Deck(
  random.randrange(1 << 30, 1 << 31), # ID del mazzo
  nome) # Nome del mazzo




dati_carte = [
    ('Italia', 'Roma'),
    ('Francia', 'Parigi'),
    ('Giappone', 'Tokyo'),
    ('Spagna', 'Madrid'),
    ('Germania', 'Berlino') 
]

for domanda, risposta in dati_carte:
    my_note = genanki.Note(
        model=my_model,
        fields=[domanda, risposta]
    )
    my_deck.add_note(my_note)

genanki.Package(my_deck).write_to_file(f'{nome}.apkg')

print(f"Mazzo '{nome}.apkg' creato con successo!")