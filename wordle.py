#import libraries
from random import randint
import csv

#create global variables
word_bank = []
game_on = True

#takes file pointer as an arg, and loads words of the desired length into a list
def load_word(fp, length):
    all_words = []
    for line in (fp):
        line_list = line.split(',')
        #check to see if word is the right length, if so, we add it
        if int(line_list[1]) == length:
            all_words.append(line_list[0])
    return all_words

#checks to see how long of a word the user wants to guess
def user_length():
    while True:
        try:
            length = int(input('How many letters in the word? '))
            break
        except ValueError:
            print("That's not a number. Try again please")
    return length

#checks to see how many attempts the user wants
def user_guesses():
    while True:
        try:
            guesses = int(input('How many guesses do you want? '))
            break
        except ValueError:
            print("That's not a number. Try again please")
    return guesses

#prints blank spaces for remaining guesses
def print_game_board(guesses, length):
    for x in range(guesses):
        #TO-DO Fix this abomination
        for index, y in enumerate(range(length)):
            if index != length-1:
                print('_', end = " ")
            else:
                print('_')

#prints out the guesses so far, with checks included
def print_guess_board(list_of_guesses, list_of_checks):
    for index, x in enumerate(list_of_guesses):
        guess_temp = list(x)
        check_temp = list_of_checks[index]
        for count, y in enumerate(guess_temp):
            if count != len(guess_temp)-1:
                if check_temp[count] == 2:
                    print(f':{guess_temp[count]}:', end = ' ')
                elif check_temp[count] == 1:
                    print(f'.{guess_temp[count]}.', end = ' ')
                else:
                    print(f'{y}', end = ' ')
            else:
                if check_temp[count] == 2:
                    print(f':{guess_temp[count]}:')
                elif check_temp[count] == 1:
                    print(f'.{guess_temp[count]}.')
                else:
                    print(f'{y}')

def input_guess(length):
    while True:
        word = input('Take your guess: ')
        if len(word) != length:
            print('Word does not match length. Try again')
        else:
            break
    return word

#checks guess vs actual word, places a 2 in the list if the position is the same
def check_right_spot(attempt, game_word):
    right = []
    list_game = list(game_word)
    list_attempt = list(attempt)
    for index, x in enumerate(list_game):
        if x == list_attempt[index]:
            right.append(2)
        else:
            right.append(0)
    return right

def check_right_letter(attempt, game_word, right):
    list_game = list(game_word)
    list_attempt = list(attempt)
    for index, x in enumerate(right):
        if x != 2:
            if list_attempt[index] in game_word:
                right[index] = 1
    return right

def check_win(right):
    for x in right:
        if x != 2: return False
    return True

def main():
    #Get inputs from user
    length = user_length()
    guesses = user_guesses()
    count_guesses = 0
    list_of_guesses = []
    list_of_checks = []
    right = []
    game_on = True

    #open file, parse for words that fit user input
    fp = open('words.csv','r')
    word_bank = load_word(fp, length)
    #checks to see if there are available words
    #pick random word from list
    if len(word_bank) == 0:
        print('There are no words of this length available in the data set')
    else:
        seed = randint(0, len(word_bank)-1)
        game_word = word_bank[seed]


    #draw game board
    print('Right letter, right space: :letter):')
    print('Right letter, wrong space: .(letter).')
    print_game_board(guesses, length)

    while game_on == True:
        victory = False
        count_guesses += 1
        #check to see if user has guesses left
        if count_guesses > guesses:
            print('You lose')
            print(f'The word was {game_word}')
            game_on = False
            break
        if count_guesses > 1:
            print('Guess again: ')
        attempt = input_guess(length)
        list_of_guesses.append(attempt)
        right = check_right_spot(attempt, game_word)
        victory = check_win(right)
        #we just need to check victory after checking if all the letters are in the right spot
        if victory == True:
            print('You win')
            print(f'It took you {count_guesses} tries')
            game_on = False
            break
        #now we check to see if the guess contained correct letters
        right = check_right_letter(attempt, game_word, right)
        list_of_checks.append(right)
        print_guess_board(list_of_guesses, list_of_checks)
        print_game_board(guesses-count_guesses, length)
        print("")
        continue


if __name__ == '__main__':
    main()
