import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('tracks_assign.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER);
''')

fname = input("Enter the file name: ")
if len(fname) < 1: fname = 'Library.xml'

def lookup(dict,key):
    found = False
    for child in dict:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

stuff = ET.parse(fname)
dicts = stuff.findall('dict/dict/dict')
print('Dictionary Len', len(dicts))

for val in dicts:
    if val is None: continue
    Name =  lookup(val,'Name')
    Artist = lookup(val,'Artist')
    Album = lookup(val,'Album')
    Genre = lookup(val,'Genre')
    Length = lookup(val,'Total Time')
    Count = lookup(val,'Play Count')
    Rating = lookup(val,'Rating')
    if Name is None or Album is None or Artist is None or Genre is None:
        continue
    print(Name,Album,Artist,Genre)
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)',(Artist,))
    cur.execute('SELECT id FROM Artist WHERE name = (?)', (Artist,))
    artist_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)',(Genre,))
    cur.execute('SELECT id FROM Genre WHERE name = (?)', (Genre,))
    genre_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Album(artist_id,title) VALUES (?,?)'
                ,(artist_id,Album))
    cur.execute('SELECT id FROM Album WHERE title = (?)',(Album,))
    album_id = cur.fetchone()[0]
    cur.execute('''INSERT OR REPLACE INTO Track
                (title, album_id, genre_id, len, rating, count)
                VALUES (?,?,?,?,?,?)''',
                (Name,album_id,genre_id,Length,Rating,Count))
    conn.commit()
