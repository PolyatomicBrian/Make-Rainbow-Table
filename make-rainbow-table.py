#!/usr/bin/env python

'''make-rainbow-table.py: Creates a rainbow table of desired hashes
                          of a wordlist using MD5, SHA224, SHA256,
                          SHA384, SHA512, or all.'''

__author__ = 'Brian Jopling'
__copyright__ = 'Copyright 2017'
__credits__ = ['Brian Jopling']
__license__ = 'MIT'
__version__ = '1.0'
__status__ = 'Development'

''' USAGE '''
# Ensure this file resides in the same directory as your wordlist.
# Run with:
''' $python make-rainbow-table.py -w WORDLIST -t HASHTYPE '''
# The following are valid hashtypes:
# md5, sha224, sha256, sha384, sha512, all

''' IMPORTS '''
# Used for database modification:
import sqlite3
# Used for hashing:
import hashlib
# Used for getting options/args:
from optparse import OptionParser

''' OPTIONS / ARGS '''
parser = OptionParser()
parser.add_option('-d', '--db', '--database', dest='db_name',
                    action='store', default='rainbow.db',
                    help='Database to fill with hashes.')
parser.add_option('-w', '--wordlist', dest='word_list_name',
                    action='store', default='linux.words',
                    help='Wordlist to read from and hash.')
parser.add_option('-t', '--type', dest='hash_type',
                    action='store', default='all',
                    metavar='md5|sha224|sha256|sha384|sha512|all')
(options, args) = parser.parse_args()


''' FUNCTIONS '''

def create_rainbow_table(db_rainbow):
    '''Creates a table \'rainbow\' in database with two fields,
       one for hash, one for word.'''
    try:
        db_rainbow.execute('CREATE TABLE rainbow (hash VARCHAR(32) \
                            PRIMARY KEY, word VARCHAR(255));')
    except sqlite3.OperationalError:
        print 'Table \'rainbow\' already exists!'

def append_to_table(db_rainbow, word_hashed, word):
    '''Inserts a word and its hash into the \'rainbow\' table of our db.'''
    sql_values = (word_hashed, word)
    try:
        db_rainbow.execute('INSERT INTO rainbow \
                            (hash, word) VALUES (?, ?);',
                            sql_values)
    except sqlite3.IntegrityError:
        print '%s is already in the database as hash %s' % (word, word_hashed)

def hash_word(word, hash_type):
    '''Returns hashed word of specified hash type.'''
    if hash_type == 'md5':
        return hashlib.md5(word).hexdigest()
    elif hash_type == 'sha224':
        return hashlib.sha224(word).hexdigest()
    elif hash_type == 'sha256':
        return hashlib.sha256(word).hexdigest()
    elif hash_type == 'sha384':
        return hashlib.sha384(word).hexdigest()
    elif hash_type == 'sha512':
        return hashlib.sha512(word).hexdigest()
    else:
        return None

def iterate_wordlist(word_list_name, db_rainbow):
    hash_types = ['md5', 'sha224', 'sha256', 'sha384', 'sha512']
    hash_type = options.hash_type
    file_word_list = open(word_list_name, 'r')
    for word in file_word_list:
        if hash_type == 'all':
            for t in hash_types:
                word_hashed = hash_word(word, t)
                append_to_table(db_rainbow, word_hashed, word)
        else:
            word_hashed = hash_word(word, hash_type)
            append_to_table(db_rainbow, word_hashed, word)
    file_word_list.close()

def save_and_close_db(db_connect):
    # Save our changes:
    db_connect.commit()
    # Close the db:
    db_connect.close()

def __main__():
    # Get options.
    db_name = options.db_name
    word_list_name = options.word_list_name
    # Connect to db.
    db_connect = sqlite3.connect(db_name)
    db_rainbow = db_connect.cursor()
    # Modify db.
    create_rainbow_table(db_rainbow)
    iterate_wordlist(word_list_name, db_rainbow)
    save_and_close_db(db_connect)

''' PROCESS '''
__main__()
