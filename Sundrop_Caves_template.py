#Ferlynn
#CICTP01
#5 August 2025

from random import randint

#New game
def newgame():
    name=input('Greetings, miner! What is your name?')
    print(f'Pleased to meet you, {name}. Welcome to Sundrop town!')
    player['name']=name
    player['day']=1
    player['GP']=0
    player['pickaxe_lvl']=1
    player['backpack_capacity']=8
    initialize_game(game_map, fog, player)
    while True:
        print('DAY ',player['day'])
        print('----- Sundrop Town -----')
        print('(B)uy stuff\nSee Player (I)nformation\nSee Mine (M)ap\n(E)nter mine\nSa(V)e game\n(Q)uit to main menu')
        print('------------------------')
        choice=input('Your choice?').strip().lower()
        if choice=='b':
            print('----------------------- Shop Menu -------------------------')
            print('(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP \n(B)ackpack upgrade to carry 12 items for 20 GP \n(L)eave shop')
            print('-----------------------------------------------------------')
            print('GP: ',player['GP'])
            print('-----------------------------------------------------------')
            shopchoice=input('Your choice?').strip().lower()
            if shopchoice=='p':
                if player['pickaxe_lvl']==1 and player['GP']>=50:
                    player['GP']-=50
                    player['pickaxe_lvl']=2
                    print('Pickaxe level upgraded to 2!')
                elif player['pickaxe_lvl']>1:
                    print('Pickaxe level have already been upgraded')
                else:
                    print('Not enough GP')
            elif shopchoice=='b':
                price=player['backpack_capacity']*2
                if player['GP']>=price:
                    player['GP']-=price
                    player['backpack_capacity']+=2
                    print('Congratulations! you can now hold', player['backpack_capacity'] ,'items!')
                else:
                    print('Not enough GP')
            elif shopchoice=='l':
                break
        elif choice=='i':
            show_information(player)
        elif choice=='m':
            draw_map(game_map, fog, player)
        elif choice=='e':
            player['day']+=1
            print('---------------------------------------------------')
            print('\nDay ',player['day'])
            print('---------------------------------------------------')
        elif choice=='v':
            save_game(game_map, fog, player)
        elif choice=='q':
            print('Returning to main menu')
            break
        else:
            print('Invalid choice, please enter again')




#Main menu
def displaymainmenu():
    print('\n---------------- Welcome to Sundrop Caves! ----------------')
    print('You spent all your money to get the deed to a mine, a small backpack, a simple pickaxe and a magical portal stone.')
    print('How quickly can you get the 500 GP you need to retire and live happily ever after? ')
    print('-----------------------------------------------------------')
    print('----Main Menu ---')
    print('(N)ew game')
    print('(L)oad saved game')
    print('(Q)uit')
    print('------------------')
    while True:
        choice=input('Your choice?').strip().lower()
        if choice in['n','l','q']:
            return choice
        print('Invalid choice, Please enter N,L or Q.')
        
player = {}
game_map = []
fog = []
while True:
    playerschoice=displaymainmenu()
    if playerschoice=='n':
        newgame()
    elif playerschoice=='l':
        load_game(game_map,fog,player)
    elif playerschoice=='q':
        print('Thanks for playing, bye!')
        break

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
    
    
