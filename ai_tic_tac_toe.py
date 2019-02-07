# coding=UTF-8
import os
from random import shuffle

null_mark_1 = '__'
null_mark_2 = '  '
coordinates = [[null_mark_1,null_mark_1,null_mark_1], [null_mark_1,null_mark_1,null_mark_1], [null_mark_2,null_mark_2,null_mark_2]]
coordinates_ai_values = [[2,4,8],[16,32,64],[128,256,512]]
# coordinates_ai_values = [[2, 3, 5], [7, 11, 13], [17, 19, 23]]
# coordinates_ai_values = [[2, 3, 7], [13, 26, 52], [79, 132, 212]]
# coordinates_ai_values = [[1,2,6], [24,120,720], [5040,40320,362880]]


# start of MoveList class -----------------------------------------------

class MoveList(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_exists = False
        self.moves = []
        self.create_file_if_necessary_and_extract_moves_if_possible()


    def create_file_if_necessary_and_extract_moves_if_possible(self):
        for file in os.listdir("."):
            if file == self.file_name:
                self.file_exists = True
                break

        if not self.file_exists:
            self.update_list_file()
        else:
            list_moves_file = open(self.file_name, "r+")
            array_in_str = list_moves_file.read()
            list_moves_file.close()

            if array_in_str != '[]':
                array_in_str = array_in_str.replace(' ', '').replace('[', '').replace(']', '')
                array_of_string_number = array_in_str.split(',')
                
                for str_num in array_of_string_number:
                    self.moves.append(int(str_num))


    def update_list_file(self):
        blacklist_moves_file = open(self.file_name, "w")
        blacklist_moves_file.write('%s' % self.moves)
        blacklist_moves_file.close()


    def add_move(self, move):
        if move not in self.moves:
            self.moves.append(move)
            self.update_list_file() 


# end of MoveList class -----------------------------------------------

blacklist = MoveList("blacklist_moves.txt")
whitelist = MoveList("whitelist_moves.txt")
greylist = MoveList("greylist_moves.txt")

# start of Player class -----------------------------------------------

class Player(object):
    def __init__(self, name, number, symbol, artificial_intelligence):
        self.name = name
        self.number = number
        self.symbol = symbol
        self.artificial_intelligence = artificial_intelligence
        self.winner = False
        self.last_move = 0


# end of Player class -----------------------------------------------

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
        letter_robot_input = input('    Is player %d a robot? (y/n) ' % (number))
        is_robot = letter_robot_input.strip().lower() == 'y'
       
        if is_robot:
            player_name = 'Robot_%d' % number
        else:
            print('\n')
            player_name = input('    Enter the name of the player %d: ' % (number))
        
        if player_name.strip() == '':
            print ('    The player %d still needs a name.\n' % (number))

    return Player(player_name, number, symbol, is_robot)


def display_information():
    display_layout()
    print (' ________________________________________________________________')
    print ('|                                                                |')
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


def get_current_move_result(player):
    result = 0
    index_r = 0

    for index_r in range(len(coordinates)):
        row = coordinates[index_r]
        index_c = 0
        for index_c in range(len(row)):
            col = row[index_c]
            if col == "_" + player.symbol or col == " " + player.symbol:
                result += coordinates_ai_values[index_r][index_c]
            elif col != null_mark_1 and col != null_mark_2:
                result -= coordinates_ai_values[index_r][index_c]
    return result


def artificial_intelligence_move(player, adversary):
    options = []
    rows = ['a', 'b', 'c']
    cols = ['1', '2', '3']

    index_r = 0
    for index_r in range(len(coordinates)):
        row = coordinates[index_r]
        index_c = 0
        for index_c in range(len(row)):
            col = row[index_c]
            if col == null_mark_1 or col == null_mark_2:
                new_move = [(rows[index_r] + cols[index_c]), coordinates_ai_values[index_r][index_c]]
                options.append(new_move)

    # good to avoid the same draw game
    shuffle(options) 
    current_move_result = get_current_move_result(player)
    
    for option in options:
        if (current_move_result + option[1]) in whitelist.moves:
            player.last_move = option[1]
            return option[0]

    for option in options:
        if (current_move_result + option[1]) not in blacklist.moves:
            player.last_move = option[1]
            return option[0]

    previous_move = current_move_result + adversary.last_move
    blacklist.add_move(previous_move)

    player.last_move = options[0][1]
    return options[0][0]


def move_command(player, adversary):
    input_move = ''

    if player.artificial_intelligence:
        input_move = artificial_intelligence_move(player, adversary)
    else:
        input_move = input('  %s plays: ' % (player.name))

    if(len(input_move) < 2 or incorrect_row(input_move) or incorrect_column(input_move)):
        print ('  Wrong move.\n')
        return ''
    else:
        row = 0
        if input_move[0] == 'a':
            row = 0
        elif input_move[0] == 'b':
            row = 1
        elif input_move[0] == 'c':
            row = 2
        column = int(input_move[1]) - 1

        player.last_move = coordinates_ai_values[row][column]

        if coordinates[row][column] == null_mark_1:
            coordinates[row][column] = '_' + player.symbol
        elif coordinates[row][column] == null_mark_2:
            coordinates[row][column] = ' ' + player.symbol
        else:
            print ('  This move has already been made.\n')
            return ''
    return input_move


def player_move(player, adversary):
    move = ''
    while move.strip() == '':
        move = move_command(player, adversary)
    if someone_wins() :
        display_layout()
        player.winner = True
        print ('    %s WINS!!!!!!!!!\n' % player.name)


def start_game(player1, player2):
    player1_turn = True

    while(not someone_wins()):
        display_layout()

        if(player1_turn):
            player_move(player1, player2)
        else:
            player_move(player2, player1)

        player1_turn = not player1_turn

        if nobody_wins():
            display_layout()
            print ('    Draw game.\n')
            break


def update_move_lists_if_necessary(player, adversary):
    if player.artificial_intelligence:
        if not player.winner and adversary.winner:
            last_move_result = get_current_move_result(player) + adversary.last_move
            blacklist.add_move(last_move_result) 
        elif player.winner and not adversary.winner:
            last_move_result = get_current_move_result(player)
            whitelist.add_move(last_move_result) 
        elif not player.winner and not adversary.winner:
            last_move_result = get_current_move_result(player)
            if player.number == 1:                
                greylist.add_move(last_move_result) 
            elif player.number == 2:
                greylist.add_move(last_move_result + adversary.last_move) 


# setting blacklist file -----------------------
print("blacklist length = %s \n" % len(blacklist.moves))
print("whitelist length = %s" % len(whitelist.moves))
input("...")


# settings and starting the game --------------------------------
player1 = set_players(1, 'x')
player2 = set_players(2, 'o')
display_information()
# start_game(player1, player2)
# update_move_lists_if_necessary(player1, player2)
# update_move_lists_if_necessary(player2, player1)




for i in range(20000):
    start_game(player1, player2)
    update_move_lists_if_necessary(player1, player2)
    update_move_lists_if_necessary(player2, player1)

    player1.winner = False
    player2.winner = False
    player1.last_move = 0
    player2.last_move = 0
    coordinates = [[null_mark_1,null_mark_1,null_mark_1], [null_mark_1,null_mark_1,null_mark_1], [null_mark_2,null_mark_2,null_mark_2]]

