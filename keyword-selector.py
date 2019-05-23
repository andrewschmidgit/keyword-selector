from argparse import ArgumentParser
from collections import Counter

import re
import sys

# Setup argument parser
parser = ArgumentParser()
parser.add_argument("filename", help="must pass in filename")
parser.add_argument("-o", "--output", dest="outputFilename", default=None)
parser.add_argument("-n", "--number", dest="number", default=10, type=int)
args = parser.parse_args()

def readFile(filename):
    try:
        file = open(filename, "r")
        words = re.findall(r"\w+", file.read().lower())
        file.close()
        return words
    except:
        print("There was an error opening" + filename)
        return None

def wordIsValid(word, rx, bannedWords):
    if rx.search(word):
        return False
    
    for w in bannedWords:
        if w == word or w + 's' == word or w + 'ed' == word:
            return False
        elif w.endswith('e') and (w[:-1] + 'ing' == word or w + 'd' == word):
            return False

    return True

def formatWords(words):
    arr = []
    for word in words:
        arr.append(word[0])
    ret = ', '
    ret = ret.join(arr)
    return ret


# Read in the file
words = readFile(args.filename)

wordCount = Counter(words)

rx = re.compile(r'^([0-9]+|[a-zA-Z]{1,2})$')
bannedWords = readFile('banned-words.txt')

filteredWords = Counter({key: wordCount[key] for key in wordCount if wordIsValid(key, rx, bannedWords)}).most_common(args.number)

output = formatWords(filteredWords)

if args.outputFilename is None:
    print(output)
else:
    outFile = open(args.outputFilename, "w+")
    outFile.write(output)