def word_to_dict(word):
    d = dict()
    for i in word:
        if i not in d:
            d[i] = 0
        d[i] += 1
    return d

def check_guess(guess):
    # if len(guess) != WORD_LENGTH:
    #     return "Your guess is not the right length!"
    guess = guess.lower()
    actual_dict = ACTUAL_DICT.copy()

    green_ls = []
    yellow_ls = []
    for i in range(len(guess)):
        if guess[i] == ACTUAL_WORD[i]:
            green_ls.append(i)
            actual_dict[guess[i]] -= 1

    for i in range(len(guess)):
        if i not in green_ls and guess[i] in actual_dict and actual_dict[guess[i]] > 0:
            yellow_ls.append(i)
            actual_dict[guess[i]] -= 1
    
    result = guess.upper() + "\n"
    for i in range(len(guess)):
        if i in green_ls:
            result += GREEN_SQUARE
        elif i in yellow_ls:
            result += YELLOW_SQUARE
        else:
            result += RED_SQUARE
    return result

def correct_answer(word):
    return word.lower() == ACTUAL_WORD

GREEN_SQUARE = u"\U0001F7E9"
YELLOW_SQUARE = u"\U0001F7E8"
RED_SQUARE = u"\U0001F7E5"
ACTUAL_WORD = "hello"
WORD_LENGTH = len(ACTUAL_WORD)
ACTUAL_DICT = word_to_dict(ACTUAL_WORD)
MAX_ATTEMPTS = 6
MAX_POINTS = MAX_ATTEMPTS + 1

print(word_to_dict("hello"))