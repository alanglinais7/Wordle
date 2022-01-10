#import libraries
from random import randint
import csv
from termcolor import colored, cprint
#from english_words import english_words_set
import enchant

#create global variables
word_bank = []
game_on = True
dictionary = enchant.Dict('en_US')

#takes file pointer as an arg, and loads words of the desired length into a list
def load_word(fp, length):
    all_words = []
    for line in fp:
        line_list = line.split(',')
        #check to see if word is the right length, if so, we add it
        if int(line_list[1]) == length:
            all_words.append(line_list[0])
    return all_words

#loads the scoreboard
def load_scoreboard(fp, name, length, guesses):
    num_of_losses = 0
    #this will only take the number of guesses it took in the wins
    wins = []
    #skip header
    next(fp)
    for line in fp:
        line_list = line.split(',')
        #make sure we're only grabbing relevant stats, and we only want the # of tries
        if name == line_list[0] and length == int(line_list[1]) and guesses == int(line_list[2]):
            if int(line_list[4]) == 1:
                wins.append(int(line_list[3]))
            #add one loss to the loss column
            else:
                num_of_losses += 1
    return wins, num_of_losses



#checks to see how long of a word the user wants to guess
def user_length():
    while True:
        try:
            length = int(input('How many letters in the word? '))
            break
        except ValueError:
            print(colored("That's not a number. Try again please",'red'))
    return length

#checks to see how many attempts the user wants
def user_guesses():
    while True:
        try:
            guesses = int(input('How many guesses do you want? '))
            break
        except ValueError:
            print(colored("That's not a number. Try again please",'red'))
    return guesses

#prints blank spaces for remaining guesses
def print_game_board(guesses, length):
    for x in range(guesses):
        #at first I thought this was bad, but it's acutally kind of elegant?
        for index, y in enumerate(range(length)):
            if index != length-1:
                print('_', end = " ")
            else:
                print('_')

#prints out the guesses so far, with checks included
def print_guess_board(list_of_guesses, list_of_checks):
    for index, x in enumerate(list_of_guesses):
        #cast the the words in the lists as lists so we can iterate through each letter
        guess_temp = list(x)
        check_temp = list_of_checks[index]
        for count, y in enumerate(guess_temp):
            #check to see if the letter is the last one in the word
            if count != len(guess_temp)-1:
                if check_temp[count] == 2:
                    print(colored(f'{guess_temp[count]}', 'green'), end = ' ')
                elif check_temp[count] == 1:
                    print(colored(f'{guess_temp[count]}', 'yellow'), end = ' ')
                else:
                    print(f'{y}', end = ' ')
            #ugliest part of the code here—in order to get a line wrap, we need to make sure the last letter doesn't include the end = ''
            else:
                if check_temp[count] == 2:
                    print(colored(f'{guess_temp[count]}', 'green' ))
                elif check_temp[count] == 1:
                    print(colored(f'{guess_temp[count]}', 'yellow'))
                else:
                    print(f'{y}')

#ask user how many guesses they want at the word
def input_guess(length):
    while True:
        word = input('Take your guess: ')
        #make sure the guess is equal to the length
        if len(word) != length:
            print(colored('Word does not match length. Try again','red'))
        else:
            #now check to see if the guess is a word
            if dictionary.check(word) == False:
                print(colored('Word is not in English. Try again','red'))
            else:
                break
    return word

#takes the user's name
def user_name():
    name = input('What is your name (all lowercase please): ')
    return name

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

#Here we check to see if the letter in the guess is in the word, but just not in the right place
#We'll use 1 in the list to indicate that. Maybe not the best solution
def check_right_letter(attempt, game_word, right):
    list_game = list(game_word)
    list_attempt = list(attempt)
    for index, x in enumerate(right):
        #Make sure we don't overwrite the 2 already there
        if x != 2:
            if list_attempt[index] in game_word:
                right[index] = 1
    return right

#We check to see if the player won by confirming that every letter is in the right spot. If so we return True
#That would mean a list of only twos. If we see anything else we return False
def check_win(right):
    for x in right:
        if x != 2: return False
    return True

#check the file for score and calculates stats
def check_scoreboard(wins, losses):
    print(f'The average amount of tries it takes you is {sum(wins)/len(wins)}')
    print(f'Your winning percentage is {len(wins)/(len(wins)+losses)*100}%')

#Adds a new row to the scoreboard with all the data. We don't need to return anything here
def add_to_scoreboard(fp_write, name, length, guesses, count_guesses, win):
    csv_writer = csv.writer(fp_write)
    csv_writer.writerow([name, length, guesses, count_guesses, win])

def play_again():
    answer = input('Do you want to play again? (y/n): ')
    if answer.lower() == 'y':
        main()
    else:
        return False


def main():
    #Get inputs from user
    length = user_length()
    guesses = user_guesses()
    name = user_name()
    count_guesses = 0
    list_of_guesses = []
    list_of_checks = []
    right = []
    game_on = True
    losses = 0

    #open file, parse for words that fit user input
    fp_words = open('words.csv','r')
    word_bank = load_word(fp_words, length)

    fp_wins = open('score_tracker.csv','r')
    fp_write = open('score_tracker.csv', 'a', newline = '')

    #checks to see if there are available words
    #pick random word from list
    if len(word_bank) == 0:
        print('There are no words of this length available in the data set')
    else:
        seed = randint(0, len(word_bank)-1)
        game_word = word_bank[seed]


    #draw game board
    print(colored('Right letter, right space: green', 'green'))
    print(colored('Right letter, wrong space: yellow', 'yellow'))
    print_game_board(guesses, length)

    #master control of the game, a while loop isn't great but a good stop gap for a hacky project
    while game_on == True:
        victory = False
        #iterate the guesses at the top in case the user is correct right away
        count_guesses += 1
        #check to see if user has guesses left, it not they lose
        #TO-DO Make this a function lmao
        if count_guesses > guesses:
            print(colored('You lose', 'red'))
            print(f'The word was {game_word}')
            #add the user's scores, check the scoreboard, and show stats
            add_to_scoreboard(fp_write, name, length, guesses, count_guesses, 0)
            wins, losses = load_scoreboard(fp_wins, name, length, guesses)
            check_scoreboard(wins, losses)
            play_again()
            game_on = False
            break
        #Only show guess again after the player has already guessed once
        if count_guesses > 1:
            print('Guess again: ')
        attempt = input_guess(length)
        list_of_guesses.append(attempt)
        right = check_right_spot(attempt, game_word)
        victory = check_win(right)
        #we just need to check victory after checking if all the letters are in the right spot
        #TO-DO Make this a function lmao
        if victory == True:
            #I want to print a finished gameboard with the word all in green so I have to add this to list of checks first
            list_of_checks.append(right)
            #Now we print the gameboard
            print_guess_board(list_of_guesses, list_of_checks)
            print_game_board(guesses-count_guesses, length)
            print(colored('You win','green'))
            #Lets show the user their stats now
            print(f'It took you {count_guesses} tries')
            #Add this game's stats to the scoreboard file
            add_to_scoreboard(fp_write, name, length, guesses, count_guesses, 1)
            #now lets check load the relevant scores
            wins, losses = load_scoreboard(fp_wins, name, length, guesses)
            #finally we show the user the stats
            check_scoreboard(wins, losses)
            play_again()
            game_on = False
            break
        #now we check to see if the guess contained correct letters
        right = check_right_letter(attempt, game_word, right)
        #add the list of checks to the master list to print out the board
        list_of_checks.append(right)
        #first we print the guesses with the correct formatting
        print_guess_board(list_of_guesses, list_of_checks)
        #Then we print the game board minus the amount of times we've guessed.
        #I.e. if a player wanted 5 attempts and has tried twice, we only need to print 3 blank rows
        print_game_board(guesses-count_guesses, length)
        #Add some spacing
        print("")
        #Head back up to the top of the loop
        continue


if __name__ == '__main__':
    main()
