import os
import sys
import ssl
import urllib.request

def initAnagramMaker(word, corpus_path):
  word_letters = sorted(set(word))
  word_file = open(corpus_path + 'corpus.txt')
  words = list(word_file.read().splitlines())
  
  words_dict = {}

  for letter in word_letters:
    words_dict.setdefault(letter, [])
    
    for entry in words:
      if entry[0] == letter:
        words_dict[letter].append(entry)
  

  return words_dict


def findAnagrams(word, corpus_path='./'):
  sorted_word = "".join(sorted(word))
  
  try:
    word_path = os.path.join(corpus_path, 'corpusDB/', str(sorted_word[0]), sorted_word)
    word_file = open(word_path)
    words = word_file.read().splitlines()
    word_anagrams = '\n'.join(item for item in words if item!=word)
     
    print('The anagrams for "' + word + '" are: \n' + word_anagrams)
  
  except:
    print(word + ' was not found in this corpus.')


def makeCorpusDB(corpus_path, corpus_url, download_corpus=True):  
  db_dict = {}
  
  if download_corpus is True:
    ssl._create_default_https_context = ssl._create_unverified_context
    corpus_raw = urllib.request.urlopen(corpus_url).read().decode('utf-8')
  
    if not(os.path.exists(corpus_path) and os.path.isdir(corpus_path)):
      os.makedirs(corpus_path) 

    open(corpus_path + 'corpus.txt', 'w').write(corpus_raw)
    
    corpus_text = open(corpus_path + 'corpus.txt').read().splitlines()

    for word in corpus_text:
      if word.isalpha() == True:

        # Sort the word
        sorted_word = "".join(sorted(word.lower()))

        # Set database directory string
        db_path = os.path.join(corpus_path, 'corpusDB', str(sorted_word[0].lower()))

        # Append found word to list with anagrams
        db_dict.setdefault(sorted_word, []).append(word + '\n')
        os.makedirs(db_path, exist_ok=True)
      
        try:
          word_file = open(os.path.join(db_path, sorted_word), 'w')
          word_file.writelines(db_dict.get(sorted_word))
          word_file.close()

        except NotADirectoryError:
          print(word + 'was not created.')
      
        except FileNotFoundError:
          print(word + 'could not be found')
  
  

if __name__ == '__main__':
  argument = sys.argv[1]

  if argument == 'init':
    print('initializing...')
    corpus_path = './'
    corpus_url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
    makeCorpusDB(corpus_path, corpus_url)

  elif argument == 'search':
    findAnagrams(sys.argv[2])

