#Ferlynn
#CICTP01
#5 August 2025

from random import randint
import os
minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

# This function shows the information for the player
def show_information(player):
    print('--- Player Information ---')
    print('Name: ', player.get('name', 'Unknown'))
    print('Portal position: ',(player['x'],player['y']))
    if player['pickaxe_lvl']==1:
        pickaxe_mineral='copper'
    elif player['pickaxe_lvl']==2:
        pickaxe_mineral='silver'
    elif player['pickaxe_lvl']>2:
        pickaxe_mineral='gold'
    print('Pickaxe level: ',player['pickaxe_lvl'],',',(pickaxe_mineral))
    print('Gold: ',player['gold'])
    print('Silver: ',player['silver'])
    print('Copper: ',player['copper'])
    load=player['gold']+player['silver']+player['copper']
    print('--------------------------')
    print('Load: ',load,'/',player['backpack_capacity'])
    print('--------------------------')
    print('GP: ',player['GP'])
    print('Steps taken: ',player['steps'])
    return

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    global MAP_WIDTH
    global MAP_HEIGHT
    map_struct.clear()
    with open(filename,'r')as f:
        for line in f:
            map_struct.append(list(line.rstrip('\n')))
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    px,py=player['x'],player['y']
    for y in range(py-1,py+2):
        for x in range(px-1,px+2):
            if 0<=y<MAP_HEIGHT and 0<=x<MAP_WIDTH:
                fog[y][x]=False
    return

#Initialize game state
def initialize_game(game_map, fog, player):
    # initialize map
    map_path=os.path.join(os.path.dirname(__file__), 'level1.txt')
    load_map(map_path, game_map)
    # TODO: initialize fog
    fog.clear()
    for _ in range(MAP_HEIGHT):
        fog.append([True]*MAP_WIDTH)
    #   You will probably add other entries into the player dictionary
    name=player.get('name','')
    player.clear()
    player['name']=name
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 1
    player['steps'] = 0
    player['pickaxe_lvl']=1
    player['backpack_capacity']=10
    clear_fog(fog, player)

# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print('+------------------------------+')
    for y in range(MAP_HEIGHT):
        row='|'
        for x in range(MAP_WIDTH):
            if not fog[y][x] or (-1<=(x - player['x'])<=1 and -1<=(y - player['y'])<=1):
                if x==player['x'] and y==player['y']:
                    row += 'M' #Player
                elif player.get('portal_x')==x and player.get('portal_y')==y:
                    row += 'P' #Portal
                else:
                    row += game_map[y][x]
            else:
                row+='?'
        row+='|'
        print(row)
    print('+------------------------------+')

mineral_required_level = {'copper': 1,'silver': 2,'gold': 3}

#Player's movement
def move_player(action, player):
    temp_x,temp_y=player['x'],player['y']
    if action=='w' and player['y']>0:
        temp_y-=1
        return True
    elif action=='s' and player['y']<MAP_HEIGHT-1:
        temp_y+=1
        return True
    elif action=='a' and player['x']>0:
        temp_x-=1
        return True
    elif action=='d' and player['x']<MAP_WIDTH-1:
        temp_x+=1
    else:
        return False
    tile=game_map[temp_y][temp_x]
    if tile in mineral_names:
        minerals=mineral_names[tile]
        required_lvl=minerals.index(minerals)+1
        if player['pickaxe_lvl']<required_lvl:
            print(f'Your pickaxe is too weak to mine {minerals}, you cannot step there.')
            return False
    player['x'],player['y']=temp_x,temp_y
    return True

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print('+---+')
    for dy in range (-1,2):
        row='|'
        for dx in range(-1,2):
            x=player['x']+dx
            y=player['y']+dy
            if 0<=x<MAP_WIDTH and 0<=y<MAP_HEIGHT:
                if x==player['x'] and y==player['y']:
                    row+='M'  #Player's position
                elif fog[y][x]:
                    row+='#'
                else:
                    row+=game_map[y][x]
            else:
                row+=' '
        row+='|'
        print(row)
    print('+---+')

#Sell Ore function
def sell_ore(player):
    total_GP=0
    for mineral in ['copper','silver','gold']:
        quantity=player[mineral]
        if quantity>0:
            price=randint(*prices[mineral])
            earnings=quantity*price
            print(f'You sell {quantity} {mineral} ore for {earnings} GP.')
            total_GP+=earnings
            player[mineral]=0
    player['GP']+=total_GP
    print('You now have ',player['GP'],' GP!')

#Mining logic function for when player steps on a mineral
def mine_tile(game_map,player):
    x,y=player['x'],player['y']
    tile=game_map[y][x]
    load=player['copper']+player['silver']+player['gold']
    capacity=player['backpack_capacity']
    if tile in mineral_names:
        mineral=mineral_names[tile]
        required_lvl=minerals.index(mineral)+1
        if player['pickaxe_lvl']>=required_lvl:
            if load<capacity:
                if mineral=='copper':
                    amount=randint(1,5)
                elif mineral=='silver':
                    amount=randint(1,3)
                else:
                    amount=randint(1,2)
                spaceleft=capacity-load
                mined_amount=min(amount,spaceleft)
                player[mineral]+=mined_amount
                game_map[y][x]=' '
                print(f'You mined {mined_amount} piece(s) of {mineral}')
                if mined_amount<amount:
                    print(f'but you can only carry {mined_amount} more piece(s)')
            else:
                print('Your backpack is full! You cannot step on this mineral.')
        else:
            print(f'Your pickaxe is too weak to mine {mineral}')

#This function checks if the player has reached 500 GP to see if player has won
def check_GP(player):
    if player['GP']>=WIN_GP:
        print(f'Woo-hoo! Well done, {player['name']}, you have {player['GP']} GP!')
        print('You now have enough to retire and play video games every day.')
        print(f'And it only took you {player['day']} days and {player['steps']} steps! You win!')
        return True
    return False

# This function saves the game
def save_game(game_map, fog, player):
    # save player
    with open('save_player.txt','w') as f:
        print('[PLAYER]',file=f)
        for key, value in player.items():
            print(f'{key}:{value}',file=f)
    # save map
        print('[MAP]',file=f)
        for row in game_map:
            print(''.join(row),file=f)
    # save fog
        print('[FOG]',file=f)
        for row in fog:
            print(''.join(['1' if cell else '0' for cell in row]),file=f)
    print('Game saved')
    return
        
#Player's dictionary
player_types={'name':str,'day':int,'GP':int,'pickaxe_lvl':int,
              'backpack_capacity':int,'copper':int,'silver':int,
              'gold':int,'steps':int,'turns':int,'x':int,'y':int,
              'portal_x':int,'portal_y':int}
# This function loads the game
def load_game(game_map, fog, player):
    section_of_file=None
    with open('save_player.txt','r') as f:
        for line in f:
            line=line.strip()
            if line=='[PLAYER]':
                section_of_file='player'
                continue
            elif line=='[MAP]':
                section_of_file='map'
                game_map.clear()
                continue
            elif line=='[FOG]':
                section_of_file='fog'
                fog.clear()
                continue
            if section_of_file=='player':
                key,value=line.split(':',1)
                if key in player_types:
                    player[key]=player_types[key](value)
                else:
                    player[key]=value
            elif section_of_file=='map':
                game_map.append(list(line))
            elif section_of_file=='fog':
                fog.append([cell=='1' for cell in line])
    global MAP_WIDTH,MAP_HEIGHT
    MAP_HEIGHT=len(game_map)
    MAP_WIDTH=len(game_map[0]) if MAP_HEIGHT>0 else 0
    print('Game loaded')
    # load map
    # load fog
    # load player
    return

#New game
def newgame():
    name=input('Greetings, miner! What is your name?')
    print(f'Pleased to meet you, {name}. Welcome to Sundrop town!')
    player['name']=name
    player['day']=1
    player['GP']=0
    player['pickaxe_lvl']=1
    player['backpack_capacity']=10
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
                if player['pickaxe_lvl']==1:
                    if player['GP']>=50:
                        player['GP']-=50
                        player['pickaxe_lvl']=2
                        print('Congratulations! You can now mine silver!')
                    else:
                        print('You do not have enough GP to upgrade to Level 2')
                elif player['pickaxe_lvl']==2:
                    if player['GP']>=150:
                        player['GP']-=150
                        player['pickaxe_lvl']=3
                        print('Congratulations! You can now mine gold!')
                    else:
                        print('You do not have enough GP to upgrade to Level 3')
                else:
                    print('Your pickaxe level is already at the max level!')
            elif shopchoice=='b':
                price=player['backpack_capacity']*2
                if player['GP']>=price:
                    player['GP']-=price
                    player['backpack_capacity']+=2
                    print(f'Backpack upgrade to hold {player["backpack_capacity"]} items for {price} GP')
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
            player['x']=0
            player['y']=0
            player['turns']=TURNS_PER_DAY
            print('You have entered the mine')
            if 'portal_x' in player and 'portal_y' in player:
                player['x']=player['portal_x']
                player['y']=player['portal_y']
                print(f'Returned to portal at ({player['x']}, {player['y']})')
            else:
                player['x']=0
                player['y']=0
                print('Entered mine at (0,0)')
            player['turns']=TURNS_PER_DAY
            while player['turns']>0:
                print('---------------------------------------------------')
                print('\nDay ',player['day'])
                print('---------------------------------------------------')
                print('DAY ',player['day'])
                draw_view(game_map, fog, player)
                load=player['gold']+player['silver']+player['copper']
                print('Turns left: ',player['turns'],'\tLoad: ',load,'/',player['backpack_capacity'],'\tSteps: ',player['steps'])
                print('(WASD) to move')
                print('(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu)')
                action=input('Action?').strip().lower()
                if action in ['w','a','s','d']:
                    if move_player(action, player):
                        player['steps']+=1
                        player['turns']-=1
                        clear_fog(fog, player)
                        mine_tile(game_map,player)
                elif action=='m':
                    draw_map(game_map, fog, player)
                elif action=='i':
                    show_information(player)
                elif action=='p':
                    player['portal_x']=player['x']
                    player['portal_y']=player['y']
                    print(f'You place your portal stone ({player['x']},{player['y']}) and zap back to town.')
                    sell_ore(player)
                    player['day']+=1
                    break
                elif action=='q':
                    return
                else:
                    print('Invalid action. Please try again')
            if player['turns']==0:
                print('You are exhausted, please return to town')
                sell_ore(player)
                player['day']+=1
        elif choice=='v':
            save_game(game_map, fog, player)
        elif choice=='q':
            print('Returning to main menu')
            break
        else:
            print('Invalid choice, please enter again')       

#--------------------------- MAIN GAME ---------------------------
def displaymainmenu():
    print("---------------- Welcome to Sundrop Caves! ----------------")
    print("You spent all your money to get the deed to a mine, a small")
    print("  backpack, a simple pickaxe and a magical portal stone.")
    print()
    print("How quickly can you get the 500 GP you need to retire")
    print("  and live happily ever after?")
    print("-----------------------------------------------------------")
    return show_main_menu()
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(Q)uit")
    print("------------------")
    while True:
        choice=input('Your choice?').strip().lower()
        if choice in['n','l','q']:
            return choice
        print('Invalid choice, Please enter N,L or Q.')
while True:
    playerschoice=displaymainmenu()
    if playerschoice=='n':
        newgame()
    elif playerschoice=='l':
        load_game(game_map,fog,player)
    elif playerschoice=='q':
        print('Thanks for playing, bye!')
        break
    
    
