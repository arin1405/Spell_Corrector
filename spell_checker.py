import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    #"Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    #"Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    #"Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    #"The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    #"All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    #"All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
    
def get_spell_check(input_text):
    input_text = input_text.lower()

    sent = ' '.join(correction(word) for word in re.split('[^a-zA-Z]', input_text) if len(word) > 0)
    remove_words = []
    split_words = []
    final_output = []
    for word in sent.split():
        if word not in WORDS:
            for i in range(1,len(word) + 1):
                #print((word[:i], word[i:]))
                if (word[:i] in WORDS) and (word[i:] in WORDS):
                    split_words.append(word[:i])
                    split_words.append(word[i:])
                    remove_words.append(word)
                    break

    if len(remove_words) > 0:
        for word in sent.split():
            if word not in remove_words:
                final_output.append(word)
            else:
                final_output.append(split_words.pop(0))
                final_output.append(split_words.pop(0))

        final_output_sent = ' '.join(word for word in final_output)
        return final_output_sent
    else:
        return sent