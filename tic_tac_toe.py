# coding=UTF-8
import os

null_1 = '__'
null_2 = '  '
coords = [[null_1,null_1,null_1], [null_1,null_1,null_1], [null_2,null_2,null_2]]

class Player(object):
    def __init__(self, name, num, mark):
        self.name = name
        self.num = num
        self.mark = mark

def display_label():
    print ('\n    ***********************')
    print ('    *    JOGO DA VELHA    *')
    print ('    ***********************\n')

def display_layout():
    os.system('clear')
    display_label()
    print ('            1  2  3')
    print ('         a %s|%s|%s' % (coords[0][0], coords[0][1], coords[0][2]))
    print ('         b %s|%s|%s' % (coords[1][0], coords[1][1], coords[1][2]))
    print ('         c %s|%s|%s' % (coords[2][0], coords[2][1], coords[2][2]))
    print ('\n')

def set_players(num, mark):
    os.system('clear')
    display_label()
    player_name = ''

    while(player_name.strip() == ''):
        player_name = input('    Digite o nome do jogador %d: ' % (num))
        if player_name.strip() == '':
            print ('    O jogador %d ainda precisa de um nome.\n' % (num))
    return Player(player_name, num, mark)

def display_information():
    display_layout()
    print (' ______________________________________________________________')
    print ('| COMO JOGAR:                                                  |')
    print ('|                                                              |')
    print ('| Para fazer uma jogada, digite a linha, coluna desejada,      |')
    print ('| e depois tecle [ENTER].                                      |')
    print ('|                                                              |')
    print ('| Exemplo: \"a1\", \"b3\", \"c2\"...                                 |')
    print ('|______________________________________________________________|\n\n')
    input('Tecle [ENTER] para continuar... ')

def someone_wins():
    # verify the rows
    if coords[0][0][1] == coords[0][1][1] and coords[0][0][1] == coords[0][2][1] and coords[0][0][1] != null_1[1]:
        return True
    elif coords[1][0][1] == coords[1][1][1] and coords[1][0][1] == coords[1][2][1] and coords[1][0][1] != null_1[1]:
        return True
    elif coords[2][0][1] == coords[2][1][1] and coords[2][0][1] == coords[2][2][1] and coords[2][0][1] != null_2[1]:
        return True
    # verify the columns
    elif(coords[0][0][1] == coords[1][0][1] and coords[0][0][1] == coords[2][0][1]):
        return True
    elif(coords[0][1][1] == coords[1][1][1] and coords[0][1][1] == coords[2][1][1]):
        return True
    elif(coords[0][2][1] == coords[1][2][1] and coords[0][2][1] == coords[2][2][1]):
        return True
    # verify the diagonals
    elif(coords[0][0][1] == coords[1][1][1] and coords[0][0][1] == coords[2][2][1]):
        return True
    elif(coords[0][2][1] == coords[1][1][1] and coords[0][2][1] == coords[2][0][1]):
        return True
    return False

def nobody_wins():
    for row in coords:
        for col in row:
            if col == null_1 or col == null_2:
                return False
    return not someone_wins()

def incorrect_row(move):
    return move[0].lower() != 'a' and move[0].lower() != 'b' and move[0].lower() != 'c'

def incorrect_column(move):
    return move[1].lower() != '1' and move[1].lower() != '2' and move[1].lower() != '3'

def player_move(player):
    move = ''
    while move.strip() == '':
        move = input('  %s joga: ' % (player.name))
        if(len(move) < 2 or incorrect_row(move) or incorrect_column(move)):
            print ('  Jogada inválida.\n')
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
            if coords[row][column] == null_1:
                coords[row][column] = '_' + player.mark
            elif coords[row][column] == null_2:
                coords[row][column] = ' ' + player.mark
            else:
                print ('  Essa jogada já foi feita.\n')
                move = ''
    if someone_wins() :
        display_layout()
        print ('    %s VENCE!!!!!!!!!\n' % player.name)

# setting the players --------------------------------
player_1 = set_players(1, 'x')
player_2 = set_players(2, 'o')
display_information()

# starting the game ----------------------------------
player_1_turn = True

while(not someone_wins()):
    display_layout()

    if(player_1_turn):
        player_move(player_1)
    else:
        player_move(player_2)

    player_1_turn = not player_1_turn

    if nobody_wins():
        display_layout()
        print ('    Ninguém ganhou.\n')
        break
