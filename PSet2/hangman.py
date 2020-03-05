# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for _ch in secret_word:
        if not _ch in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    _s = ""
    for _ch in secret_word:
        if _ch in letters_guessed:
            _s += _ch
        else:
            _s += "_ "
    return _s


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    _s = ""
    for _ch in string.ascii_lowercase:
        if _ch not in letters_guessed:
            _s += _ch
    return _s
    
def is_letter_in_secret_word(letter, secret_word):
    vowels = 'aeiou'
    if letter not in secret_word:
        if letter in vowels:
            return 2, 'Oops! That letter is not in my word:'
        return 1, 'Oops! That letter is not in my word:'
    return 0, 'Good guess:'

def print_remaining_guesses_and_avail_letters(guesses, warnings, avail_letters):
    print(f'You have {warnings} warnings left.')
    print(f'You have {guesses} guesses left.')
    print(f'Available letters: {avail_letters}')

def letter_already_used(_l, guessed_letters):   
    if _l in guessed_letters:    
        return True
    return False
    
def guess_letter(guessed_letters):
    print('Guess a letter:')
    _l = input()

    if str.isalpha(_l) and len(_l) == 1:
        _l = str.lower(_l)

        if letter_already_used(_l, guessed_letters):
            return None, 'Oops! You\'ve already guessed that letter.'
        return _l, None
    return None, 'Oops! That is not a valid letter.'

def guess_letter_w_hint(guessed_letters):
    print('Guess a letter:')
    _l = input()

    if _l == '*':
        return _l, None

    if str.isalpha(_l) and len(_l) == 1:
        _l = str.lower(_l)

        if letter_already_used(_l, guessed_letters):
            return None, 'Oops! You\'ve already guessed that letter.'
        return _l, None
    return None, 'Oops! That is not a valid letter.'

def decrease_warnings(warnings):
    warnings -= 1
    return warnings

def decrease_guesses(guesses):
    guesses -= 1
    return guesses

def is_lost_and_message(guesses, secret_word):
    if guesses == 0:
        print(f'You lose. The word was {secret_word}.')
        return True
    return False


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses = 6
    warnings = 3
    guessed_letters = []

    print('Welcome!')
    print(f'I\'m thinking of a word that is {len(secret_word)} letters long.')    
    print('------')
    while guesses > 0:

        avail_letters = get_available_letters(guessed_letters)

        print_remaining_guesses_and_avail_letters(guesses, warnings, avail_letters)        

        _l, print_guess_type = guess_letter(guessed_letters)

        if _l is None:
            warnings = decrease_warnings(warnings)
            warnings_msg = f'You have {warnings} warnings left:'
            if warnings < 0:
                warnings_msg = f'You have no warnings left so you lose one guess:'
                guesses = decrease_guesses(guesses)
                if is_lost_and_message(guesses, secret_word):
                    return None
                warnings = 3
            print(print_guess_type, warnings_msg, get_guessed_word(secret_word, guessed_letters))
            print('------')
            continue

        if not _l in guessed_letters:
            guessed_letters.append(_l)

        if is_word_guessed(secret_word, guessed_letters):
            break
        
        lost_guesses, print_guess_type = is_letter_in_secret_word(_l, secret_word)

        guesses -= lost_guesses
        print(print_guess_type, get_guessed_word(secret_word, guessed_letters))
        print('------')
        
    if is_lost_and_message(guesses, secret_word):
        return None
    else:
        print('You won! Congrats!')
        print(f'Your score is {guesses*len(set(secret_word))}.')
        return None

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word = my_word.replace(" ","")
    if len(my_word) != len(other_word):
        return False

    missing_letters = []
    for i in range(len(my_word)):
        if my_word[i] == "_":
            if other_word[i] not in missing_letters:
                missing_letters.append(other_word[i])
        else:
            if my_word[i] != other_word[i] or my_word[i] in missing_letters:
                return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    matches = []
    for w in wordlist:
        if match_with_gaps(my_word, w):
            matches.append(w)
    if matches:
        print(*matches)
    else:
        print("No matches found")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses = 6
    warnings = 3
    guessed_letters = []

    print('Welcome!')
    print(f'I\'m thinking of a word that is {len(secret_word)} letters long.')    
    print('------')
    while guesses > 0:

        avail_letters = get_available_letters(guessed_letters)

        print_remaining_guesses_and_avail_letters(guesses, warnings, avail_letters)        

        _l, print_guess_type = guess_letter_w_hint(guessed_letters)

        if _l == '*':
            print('-------')
            print('You used a hint')
            show_possible_matches(get_guessed_word(secret_word, guessed_letters))
            print('-------')
            continue

        if _l is None:
            warnings = decrease_warnings(warnings)
            warnings_msg = f'You have {warnings} warnings left:'
            if warnings < 0:
                warnings_msg = f'You have no warnings left so you lose one guess:'
                guesses = decrease_guesses(guesses)
                if is_lost_and_message(guesses, secret_word):
                    return None
                warnings = 3
            print(print_guess_type, warnings_msg, get_guessed_word(secret_word, guessed_letters))
            print('------')
            continue

        if not _l in guessed_letters:
            guessed_letters.append(_l)

        if is_word_guessed(secret_word, guessed_letters):
            break
        
        lost_guesses, print_guess_type = is_letter_in_secret_word(_l, secret_word)

        guesses -= lost_guesses
        print(print_guess_type, get_guessed_word(secret_word, guessed_letters))
        print('------')
        
    if is_lost_and_message(guesses, secret_word):
        return None
    else:
        print('You won! Congrats!')
        print(f'Your score is {guesses*len(set(secret_word))}.')
        return None



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
