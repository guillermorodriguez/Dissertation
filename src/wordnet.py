
from nltk.corpus import wordnet 

query = "car"
_keywords = []
for _synonyms in wordnet.synsets(query):
    for _s in _synonyms.lemmas():
        _s = _s.name().replace('_', ' ')
        if _s not in _keywords:
            _keywords.append(_s)
if len(_keywords) == 0:
    _keywords.append(query)
    
print(_keywords)