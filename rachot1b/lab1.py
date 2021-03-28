import matplotlib.pyplot as plt
import codecs

# ---1a---
voiceless = ['п', 'ф', 'т', 'с', 'ш', 'к','ч', 'щ', 'ц', 'х']
voiced = ['б', 'в', 'д', 'з', 'ж', 'г', 'л', 'м', 'н', 'р', 'й']
vowels = ['а', 'о', 'и', 'е', 'ё', 'э', 'ы', 'у', 'ю', 'я']
signs = ['ь', 'ъ']

def letterInfo(letter):
    s = ''
    if letter == '': return ''
    if letter in signs: return 's'
    if letter.isupper():
        s = 'u'
    else:
        s = 'l'
    letterL = letter.lower()
    if letterL in voiceless:
        s = s + 'cs'
    elif letterL in voiced:
        s = s + 'cd'
    elif letterL in vowels:
        s = s + 'v'
    return s

def piLetter(word,letter):
    return len([a for a in word if a.lower()==letter]) / len(word)

def piInfo(word,position,info):
    if position >= len(word): return 0
    if info != letterInfo(word[position]):
        return 0
    else:
        return 1 / len(word)

f = codecs.open('task_1_words.txt',encoding='utf-8')
n_exp = int(f.readline().split(': ')[1].split(', ')[1].split(' = ')[1])
f.readline()
infoList = []
for i in range(n_exp):
    dct = {}
    s = f.readline().split(': ')
    if len(s) == 2:
        dct['letter'] = s[1][1]
    else:
        dct['position'] = int(s[1]) - 1
        x = ''
        for item in s[2].rstrip().split(' '):
            if item == 'заглавная': x = 'u'
            if item == 'строчная': x = 'l'
            if item == 'гласная': x = x + 'v'
            if item == 'звонкая': x = x + 'cd'
            if item == 'глухая': x = x + 'cs'
        dct['info'] = x
    infoList.append(dct)
f.close()   

listOfWords = []
with open('names_all.txt', 'r', encoding = 'utf-8') as file:
    for line in file:
        listOfWords.append(line.rstrip())
        
probs = {}
for word in listOfWords:
    probs[word]= 1 / len(listOfWords)
    
possibleWords = [word for word in listOfWords]
step = 0
maxProb = max(probs.values())
for item in infoList:
    step += 1
    if 'letter' in item:
        for word in possibleWords:
            probs[word] *= piLetter(word, item['letter'])
    else:
        for word in possibleWords:
            probs[word] *= piInfo(word, item['position'], item['info'])
    s = sum(probs.values())
    
    for word in possibleWords:
        try:
            probs[word] /= s
        except:
            print("0")
                         
    possibleWords = [word for word in possibleWords if probs[word] != 0]
    
    if max(probs.values()) / maxProb > 1.5:
        print(step)
        plt.plot(list(probs.values()))
        plt.show()
        maxProb = max(probs.values())
        
    if len(possibleWords) == 1:
        break
        
# ---1b---
possibleWords = listOfWords
list_of_codes = []
best_words = {'':0}
for item in infoList:
    if 'letter' in item:
        for word in possibleWords:
            probs[word] = piLetter(word, item['letter'])
    else:
        for word in possibleWords:
            probs[word] = piInfo(word, item['position'], item['info'])
            
    s = sum(probs.values())
    for word in possibleWords:
        try:
            probs[word] /= s
        except:
            print("0")
                         
        
    possibleWords = [word for word in possibleWords if probs[word] != 0]
    word = max(probs, key = probs.get)
    
    if word in best_words:
        list_of_codes.append(best_words[word])
    else:
        best_words[word] = max(best_words.values()) + 1
        list_of_codes.append(best_words[word])
        
    if len(possibleWords) == 1: break
    
fig, ax = plt.subplots()
ax.set_yticks(range(len(best_words)))
ax.set_yticklabels([['$'+key+'$' for key, value in best_words.items() if value == i][0] for i in range(len(best_words))])
ax.plot(list_of_codes)
ax.set_title('Maximum probability hypothesis')
plt.show()

# ---1c---
possibleWords = listOfWords
list_of_nums = []
for item in infoList:
    if 'letter' in item:
        for word in possibleWords:
            probs[word] = piLetter(word, item['letter'])
    else:
        for word in possibleWords:
            probs[word] = piInfo(word, item['position'], item['info'])
    s = sum(probs.values())
    for word in possibleWords:
        probs[word] /= s
    possibleWords = [word for word in possibleWords if probs[word] != 0]
    num_of_hyps = 0
    total_prob = 0
    for prob in sorted(probs.values(), reverse = True):
        num_of_hyps += 1
        total_prob += prob
        if total_prob > 0.99:
            break
    list_of_nums.append(num_of_hyps)
    if len(possibleWords) == 1:
        break
    
fig, ax = plt.subplots()
ax.plot(list_of_nums)
ax.set_yscale('log')
ax.set_title('Number of best hypotheses')
plt.show()

# ---2a---
def symbolAtPosition(word, position):
    if position < len(word):
        return word[position]
    return ''

probs = {}
N = max([len(word) for word in listOfWords])

for position in range(N):
    hyps = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
          'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь',
          'ы', 'ъ', 'э', 'ю', 'я']
    hyps = hyps + [x.upper() for x in hyps] + ['']
    
    for word in listOfWords:
        probs[word]=1 / len(listOfWords)
        
    possibleWords = listOfWords
    prob_letter = {}
    num_of_possible_letters = 67
    for hyp in hyps:
        prob_letter[hyp] = sum([probs[word] for word in possibleWords if symbolAtPosition(word, position) == hyp])
        
    hyps=[h for h in hyps if prob_letter[h] != 0]
    step = 0
    plt.plot([prob_letter[let] for let in hyps])
    plt.title('Position ' + str(position + 1))
    plt.xticks(range(67), ['$' + let + '$' for let in hyps[:-1]] + [''])
    for item in infoList:
        step += 1
        if 'letter' in item:
            for word in possibleWords:
                probs[word] = piLetter(word, item['letter'])
        else:
            for word in possibleWords:
                probs[word] = piInfo(word, item['position'], item['info'])
                
        s = sum(probs.values())
        for word in possibleWords:
            probs[word] /= s
            
        for hyp in hyps:
            prob_letter[hyp] = sum([probs[word] for word in possibleWords if symbolAtPosition(word, position) == hyp])
            
        possibleWords = [word for word in possibleWords if probs[word] != 0]
        
        if len([x for x in prob_letter.values() if x != 0]) / num_of_possible_letters < 0.6:
            plt.plot([prob_letter[let] for let in hyps])
            num_of_possible_letters = len([x for x in prob_letter.values() if x != 0])
            
        if len(possibleWords) == 1: break
        
        if num_of_possible_letters == 1: break
        
    plt.bar([k - 0.5 for k in range(len(hyps))], [prob_letter[let] for let in hyps], alpha = 0.1, color = 'blue')
    plt.show()
    if prob_letter[''] == 1: break

#Гипотезы о типе символа:
# 1) заглавная гласная (uv)
# 2) заглавная согласная звонкая (ucd)
# 3) заглавная согласная глухая (ucs)
# 4) строчная гласная (lv)
# 5) строчная согласная звонкая (lcd)
# 6) строчная согласная глухая (lcs)
# 7) знак (s)
# 8) нет символа ()
probs = {}
hyps = ['uv', 'ucd', 'ucs', 'lv', 'lcd', 'lcs', 's', '']

for position in range(N):
    for word in listOfWords:
        probs[word] = 1 / len(listOfWords)
        
    possibleWords = listOfWords
    probLetterType = {}
    num_of_possible_letter_types = 8
    for hyp in hyps:
        probLetterType[hyp]=sum([probs[word] for word in possibleWords if letterInfo(symbolAtPosition(word, position)) == hyp])
   
    step = 0
    plt.plot([probLetterType[hyp] for hyp in hyps])
    plt.title('Position ' + str(position + 1))
    plt.xticks(range(8), hyps)
    for item in infoList:
        step += 1
        if 'letter' in item:
            for word in possibleWords:
                probs[word] = piLetter(word, item['letter'])
        else:
            for word in possibleWords:
                probs[word] = piInfo(word, item['position'], item['info'])
        
        s = sum(probs.values())
        for word in possibleWords:
            probs[word] /= s
        
        for hyp in hyps:
            probLetterType[hyp] = sum([probs[word] for word in possibleWords if letterInfo(symbolAtPosition(word, position)) == hyp])
        
        possibleWords = [word for word in possibleWords if probs[word] != 0]
        
        if len([x for x in probLetterType.values() if x != 0]) < num_of_possible_letter_types:
            plt.plot([probLetterType[hyp] for hyp in hyps])
            num_of_possible_letter_types = len([x for x in probLetterType.values() if x != 0])
        
        if len(possibleWords) == 1: break
        
        if num_of_possible_letter_types == 1: break
    
    plt.bar([k - 0.5 for k in range(8)], [probLetterType[hyp] for hyp in hyps], alpha = 0.1, color= 'blue')
    plt.show()
    if probLetterType[''] == 1: break
    
# ---2b---
probs = {}
for position in range(N):
    hyps = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
      'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь',
      'ы', 'ъ', 'э', 'ю', 'я']
    
    hyps = hyps + [x.upper() for x in hyps] + ['']
    
    for word in listOfWords:
        probs[word]= 1 / len(listOfWords)
    
    possibleWords = listOfWords
    prob_letter = {}
 
    for hyp in hyps:
        prob_letter[hyp] = sum([probs[word] for word in possibleWords if symbolAtPosition(word, position) == hyp])
    
    hyps=[h for h in hyps if prob_letter[h] != 0]
    step = 0
    best_hyps = []
    for item in infoList:
        step += 1
        if 'letter' in item:
            for word in possibleWords:
                probs[word] = piLetter(word, item['letter'])
        else:
            for word in possibleWords:
                probs[word] = piInfo(word, item['position'], item['info'])
        
        s = sum(probs.values())
        for word in possibleWords:
            probs[word] /= s
        
        for hyp in hyps:
            prob_letter[hyp] = sum([probs[word] for word in possibleWords if symbolAtPosition(word, position) == hyp])
        
        possibleWords = [word for word in possibleWords if probs[word] != 0]
        best_hyps.append(hyps.index(max(prob_letter, key = prob_letter.get)))
        
        if len(possibleWords) == 1: break
    
    plt.plot(best_hyps)
    plt.plot([best_hyps[-1]] * len(best_hyps), alpha = 0.1)
    plt.yticks(range(len(hyps) + 1), ['$' + hyp + '$' for hyp in hyps[:-1]] + [''])
    plt.title('Position ' + str(position + 1))
    plt.show()
    if prob_letter[''] == 1: break
    
#Гипотезы о типе символа:
# 1) заглавная гласная (uv)
# 2) заглавная согласная звонкая (ucd)
# 3) заглавная согласная глухая (ucs)
# 4) строчная гласная (lv)
# 5) строчная согласная звонкая (lcd)
# 6) строчная согласная глухая (lcs)
# 7) знак (s)
# 8) нет символа ()
probs = {}
hyps = ['', 's', 'uv', 'ucd', 'ucs', 'lv', 'lcd', 'lcs']
hypsRussian = ['$нет$ $символа$', '$знак$', '$заглавная$ $гласная$',
                '$заглавная$ $согласная$ $звонкая$', '$заглавная$ $согласная$ $глухая$',
                '$строчная$ $гласная$', '$строчная$ $согласная$ $звонкая$',
                '$строчная$ $согласная$ $глухая$']
dct={'':0, 's':1, 'uv':2, 'ucd':3, 'ucs':4, 'lv':5, 'lcd':6, 'lcs':7}

for position in range(N):
    for word in listOfWords:
        probs[word]= 1 / len(listOfWords)
    
    possibleWords = listOfWords
    probLetterType = {}
    num_of_possible_letter_types = 8
    
    for hyp in hyps:
        probLetterType[hyp] = sum([probs[word] for word in possibleWords if letterInfo(symbolAtPosition(word, position)) == hyp])
    
    step = 0
    best_hyps = []
    for item in infoList:
        step += 1
        if 'letter' in item:
            for word in possibleWords:
                probs[word] = piLetter(word, item['letter'])
        else:
            for word in possibleWords:
                probs[word] = piInfo(word, item['position'], item['info'])
        
        s = sum(probs.values())
        
        for word in possibleWords:
            probs[word] /= s
        
        for hyp in hyps:
            probLetterType[hyp] = sum([probs[word] for word in possibleWords if letterInfo(symbolAtPosition(word, position)) == hyp])
        
        possibleWords = [word for word in possibleWords if probs[word] != 0]
        best_hyps.append(dct[max(probLetterType, key = probLetterType.get)])
        
        if len(possibleWords) == 1: break
        
        if num_of_possible_letter_types == 1: break
    
    plt.plot(best_hyps)
    plt.yticks(range(9), hypsRussian+[''])
    plt.title('Position ' + str(position + 1))
    plt.show()
    if probLetterType[''] == 1: break
    
# ---3a---
frLetters = {}
typesOfLetters = {}
for item in infoList:
    if 'letter' in item:
        if item['letter'] in frLetters:
            frLetters[item['letter']] += 1
        else:
            frLetters[item['letter']] = 1
    else:
        typesOfLetters[item['position']] = item['info']
        
frMin = min(frLetters.values())

lettersOfWord = {}
for letter in frLetters:
    lettersOfWord[letter] = int(frLetters[letter] / frMin)

print('Letters:')
print(lettersOfWord)
print('Types:')
print(typesOfLetters)

# ---3b---
for word in listOfWords:
    letters= [word[i] for i in range(len(word))]
    n = len(letters)
    types = {}
    for i in range(n):
        types[i] = letterInfo(letters[i])
        
    check = types == typesOfLetters
    
    for l in lettersOfWord:
        if len([x for x in letters if x.lower() == l]) != lettersOfWord[l]:
            check = False
            break
    if check: print(word)

# ---3d---
listOfLetters = []
for i in range(n_exp):
    frLetters = {l: 0 for l in listOfLetters}
    typesOfLetters = {}
    
    for item in infoList[:i]:
        if 'letter' in item:
            if item['letter'] in frLetters:
                frLetters[item['letter']] += 1
            else:
                frLetters[item['letter']] = 1
                listOfLetters.append(item['letter'])
        else:
            typesOfLetters[item['position']] = item['info']
            
    if i in [2 ** i for i in range(20)]:
        print(str(i) + ' experiments:')
        print('Types: ', typesOfLetters)
        plt.bar(range(len(frLetters)), [frLetters[l] for l in listOfLetters])
        plt.xticks(range(len(frLetters)),['$' + l + '$' for l in listOfLetters])
        plt.show()