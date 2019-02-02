# coding=UTF-8
import os

null_mark_1 = '__'
null_mark_2 = '  '
coordinates = [[null_mark_1,null_mark_1,null_mark_1], [null_mark_1,null_mark_1,null_mark_1], [null_mark_2,null_mark_2,null_mark_2]]

class Player(object):
    def __init__(self, name, number, symbol):
        self.name = name
        self.number = number
        self.symbol = symbol

def display_label():
    print ('\n    ***********************')
    print ('    *     TIC TAC TOE     *')
    print ('    ***********************\n')

def display_layout():
    os.system('clear')
    display_label()
    print ('            1  2  3')
    print ('         a %s|%s|%s' % (coordinates[0][0], coordinates[0][1], coordinates[0][2]))
    print ('         b %s|%s|%s' % (coordinates[1][0], coordinates[1][1], coordinates[1][2]))
    print ('         c %s|%s|%s' % (coordinates[2][0], coordinates[2][1], coordinates[2][2]))
    print ('\n')

def set_players(number, symbol):
    os.system('clear')
    display_label()
    player_name = ''

    while(player_name.strip() == ''):
        player_name = input('    Enter the name of the player %d: ' % (number))
        if player_name.strip() == '':
            print ('    The player %d still needs a name.\n' % (number))
    return Player(player_name, number, symbol)

def display_information():
    display_layout()
    print (' ________________________________________________________________')
    print ('| HOW TO PLAY:                                                   |')
    print ('|                                                                |')
    print ('| To make a move, enter the row, column, and then press [ENTER]. |')
    print ('|                                                                |')
    print ('| Example: \"a1\", \"b3\", \"c2\"...                                   |')
    print ('|________________________________________________________________|\n\n')
    input('Press [ENTER] to continue... ')

def someone_wins():
    # verify the rows
    if coordinates[0][0][1] == coordinates[0][1][1] and coordinates[0][0][1] == coordinates[0][2][1] and coordinates[0][0][1] != null_mark_1[1]:
        return True
    elif coordinates[1][0][1] == coordinates[1][1][1] and coordinates[1][0][1] == coordinates[1][2][1] and coordinates[1][0][1] != null_mark_1[1]:
        return True
    elif coordinates[2][0][1] == coordinates[2][1][1] and coordinates[2][0][1] == coordinates[2][2][1] and coordinates[2][0][1] != null_mark_2[1]:
        return True
    # verify the columns
    elif(coordinates[0][0][1] == coordinates[1][0][1] and coordinates[0][0][1] == coordinates[2][0][1]):
        return True
    elif(coordinates[0][1][1] == coordinates[1][1][1] and coordinates[0][1][1] == coordinates[2][1][1]):
        return True
    elif(coordinates[0][2][1] == coordinates[1][2][1] and coordinates[0][2][1] == coordinates[2][2][1]):
        return True
    # verify the diagonals
    elif(coordinates[0][0][1] == coordinates[1][1][1] and coordinates[0][0][1] == coordinates[2][2][1]):
        return True
    elif(coordinates[0][2][1] == coordinates[1][1][1] and coordinates[0][2][1] == coordinates[2][0][1]):
        return True
    return False

def nobody_wins():
    for row in coordinates:
        for col in row:
            if col == null_mark_1 or col == null_mark_2:
                return False
    return not someone_wins()

def incorrect_row(move):
    return move[0].lower() != 'a' and move[0].lower() != 'b' and move[0].lower() != 'c'

def incorrect_column(move):
    return move[1].lower() != '1' and move[1].lower() != '2' and move[1].lower() != '3'

def player_move(player):
    move = ''
    while move.strip() == '':
        move = input('  %s plays: ' % (player.name))
        if(len(move) < 2 or incorrect_row(move) or incorrect_column(move)):
            print ('  Wrong move.\n')
            move = ''
        else:
            row = 0
            if move[0] == 'a':
                row = 0
            elif move[0] == 'b':
                row = 1
            elif move[0] == 'c':
                row = 2
            column = int(move[1]) - 1
            if coordinates[row][column] == null_mark_1:
                coordinates[row][column] = '_' + player.symbol
            elif coordinates[row][column] == null_mark_2:
                coordinates[row][column] = ' ' + player.symbol
            else:
                print ('  This move has already been made.\n')
                move = ''
    if someone_wins() :
        display_layout()
        print ('    %s WINS!!!!!!!!!\n' % player.name)

def start_game(player1, player2):
    player1_turn = True

    while(not someone_wins()):
        display_layout()

        if(player1_turn):
            player_move(player1)
        else:
            player_move(player2)

        player1_turn = not player1_turn

        if nobody_wins():
            display_layout()
            print ('    Draw game.\n')
            break

# settings and starting the game --------------------------------
player1 = set_players(1, 'x')
player2 = set_players(2, 'o')
display_information()
start_game(player1, player2)

