import nltk
# nltk.download()

from nltk.corpus import wordnet 

print("Started ....")

synonyms = []
for syn in wordnet.synsets("car"):
    for l in syn.lemmas():
        synonyms.append(l.name())

print(synonyms)
