# Make-Rainbow-Table
A simple rainbow table generator supporting MD5, SHA224, SHA256, SHA384, and SHA512, written in **Python 2**.

## Usage

    $ python make-rainbow-table.py [-h] [-d DATABASE] [-w WORDLIST] [-t HASHTYPE]
    
**Arguments:** 

    -h, --help                                                  show this help message and exit
  
    -d DB_NAME, --db=DB_NAME, --database=DB_NAME                Database to fill with hashes. (default='rainbow.db')
                        
    -w WORD_LIST_NAME, --wordlist=WORD_LIST_NAME                Wordlist to read from and hash. (default='linux.words')
                        
    -t md5|sha224|sha256|sha384|sha512|all, --type=HASHTYPE     Type of hash to use. (default='all')


## Examples

By default, the program will create a database called rainbow.db and use its local wordlist 'linux.words.' It will hash each word using all hash-types included in this program.
    
    $ python make-rainbow-table.py

You can specify what you feel necessary, however.
    
    $ python make-rainbow-table.py -d rainbow.db -w linux.words -t all
    
    $ python make-rainbow-table.py -t md5
    
    $ python make-rainbow-table.py -d rbdatabase.db -w mycustom.list -t sha256

If the specified database does not exist, then it will be created for you.
