import sys
from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", ["rock"]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", ["umbrella", "rug", "candle"]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", ["knife", "binoculars"]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", ["lantern"]),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", ["dust", "coin", "chest", "map"]),
}

# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player_name = input("What is your name? >> ")
player = Player(player_name, room['outside'])
print(f'Welcome, {player.name}.')

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
# "i" prints player's inventory.

while True:
    print(f'{player.room}')
    print(f'Description: {player.room.description}')
    print(f'Items in room: {player.room.items}')
    move = input(">> ").split(" ")
    if len(move) == 1:
        try:
            if move[0] == 'n':
                player.room = player.room.n_to
            elif move[0] == 's':
                player.room = player.room.s_to
            elif move[0] == 'e':
                player.room = player.room.e_to
            elif move[0] == 'w':
                player.room = player.room.w_to
            elif move[0] in ['i', 'inventory']:
                print(f'Inventory: {player.items}')
            elif move[0] == 'q':
                print("Goodbye!")
                break
        except:
            print("You run into a wall, try another direction")
    elif len(move) == 2:
        if move[0] == 'get':
            if move[1] in player.room.items:
                player.room.remove_item(move[1])
                Item(move[1]).on_take()
                player.add_item(move[1])
            else:
                print(f"{move[1]} not found.")
        elif move[0] == 'drop':
            if move[1] in player.items:
                player.remove_item(move[1])
                Item(move[1]).on_drop()
                player.room.add_item(move[1])
            else:
                print(f'{move[1]} not in inventory. Type "i" to check inventory.')
        else:
            print("Unable to parse. Commands for items include: get, drop")
