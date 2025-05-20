# Zork I Guide and AI Processing Instructions

## AI Processing Instructions
- **Emulator Information**: Ignore any text related to dosemu2, FDPP kernel, or disk drive information that appears before the actual Zork game starts
- **Game Start Indicator**: The actual game content begins with "West of House" and "ZORK I: The Great Underground Empire"
- **System Messages to Skip**: 
  - Information about dosemu2 versions
  - GPL license notices
  - Disk drive information (C:, D:, E:, F: HD entries)
  - XMS support messages
  - Any other system or emulator-related output

# Zork I Location Guide

## Above Ground Locations

### West of House
- **Description**: Starting point of the game, an open field west of a white house with a boarded front door
- **Items**: Small mailbox containing a leaflet
- **Exits**: North (to North of House), South (to South of House), West (to Forest), East (blocked by front door)
- **Commands**: `open mailbox`, `read leaflet`
- **Navigation Tip**: "The message of the leaflet starts with: 'WELCOME TO ZORK!', you can avoid reading it"

### North of House
- **Description**: North side of the white house with no door and boarded windows
- **Items**: None
- **Exits**: North (to Forest Path), South (to West of House), East (to East of House)
- **Key Navigation**: This is a critical junction for returning from the forest

### South of House
- **Description**: South side of the white house with no door and boarded windows
- **Items**: None
- **Exits**: North (to West of House), East (to Behind House)

### East of House
- **Description**: East side of the white house with no door and boarded windows
- **Items**: None
- **Exits**: North (to Behind House), South (to South of House), West (to North of House)

### Behind House
- **Description**: Behind the white house with a path leading to the forest and a slightly ajar window
- **Items**: Window (entry point to house)
- **Exits**: West (to South of House), North (to East of House), East (to Forest), Window (to Kitchen)
- **Commands**: `open window`, `enter house`

### Kitchen
- **Description**: Kitchen of the white house with a table, passage west, and dark staircase upward
- **Items**: Brown sack (contains garlic and lunch), bottle of water
- **Exits**: West (to Living Room), Up (to Attic), Down (to Cellar via chimney)

### Living Room
- **Description**: Main room with a trophy case, wooden door, and oriental rug
- **Items**: Sword, brass lantern, trap door (under rug)
- **Exits**: East (to Kitchen), Down (to Cellar via trap door)
- **Commands**: `move rug`, `open trap door`

### Attic
- **Description**: Attic with only a stairway leading down
- **Items**: Coil of rope, nasty-looking knife
- **Exits**: Down (to Kitchen)

## Forest and Outdoor Areas

### Forest Path
- **Description**: Path winding through dimly lit forest with a large tree
- **Items**: Tree with bird's nest containing jeweled egg
- **Exits**: North (deeper into forest), South (to North of House)
- **Commands**: `climb tree`, `get egg from nest`
- **Navigation Tip**: After getting the egg, go SOUTH to return to the house

### Clearing
- **Description**: Small clearing in a well-marked forest path
- **Items**: Grating (when opened from below)
- **Exits**: East (to Canyon View), West (to Forest)

### Canyon View
- **Description**: Top of the Great Canyon with view of Frigid River and Aragain Falls
- **Items**: None
- **Exits**: Northwest (to Clearing), Down (to Rocky Ledge)

### Rocky Ledge
- **Description**: Ledge halfway up the wall of the river canyon
- **Items**: None
- **Exits**: Up (to Canyon View), Down (to Canyon Bottom)

### Canyon Bottom
- **Description**: Bottom of the canyon beneath climbable walls
- **Items**: None
- **Exits**: North (to End of Rainbow), Up (to Rocky Ledge)

### End of Rainbow
- **Description**: Small rocky beach on the Frigid River past the Falls
- **Items**: Rainbow (becomes solid when sceptre is waved)
- **Exits**: Southwest (to Canyon Bottom)
- **Commands**: `wave sceptre` (creates rainbow bridge and pot of gold)

## Underground Locations

### Cellar
- **Description**: Dark and damp cellar with narrow passageway and crawlway
- **Items**: None
- **Exits**: North (to Troll Room), South (to East of Chasm), Up (to Living Room via trap door)

### Troll Room
- **Description**: Small room with bloodstained walls and scratches
- **Items**: Troll (enemy), bloody axe
- **Exits**: East (to East-West Passage), South (to Cellar), West (to Maze)
- **Commands**: `kill troll with sword` (multiple times)

### East-West Passage
- **Description**: Narrow east-west passageway with stairway leading down
- **Items**: None
- **Exits**: East (to Round Room), West (to Troll Room), North (to Chasm)

### Round Room
- **Description**: Circular stone room with passages in all directions
- **Items**: None
- **Exits**: Southeast (to Engravings Cave), East (to Loud Room), West (to East-West Passage)

### Maze
- **Description**: Confusing maze of twisty little passages
- **Items**: Skeleton key, bag of coins (in upper level)
- **Exits**: Multiple confusing exits
- **Navigation**: From Troll Room: `west`, `north`, `east`, `south`, `west`, `up` (get items), `down`, `north`, `east`, `northeast`, `northwest` (exit to Dam Lobby)

### Cyclops Room
- **Description**: Room with a cyclops blocking a staircase
- **Items**: Cyclops (enemy)
- **Exits**: Northwest (to Maze), Up (to Treasure Room, blocked by cyclops), East (to Strange Passage, blocked by wall)
- **Commands**: `say Ulysses` or `say Odysseus` (makes cyclops flee)

### Treasure Room
- **Description**: Large room with east wall of solid granite
- **Items**: Thief (enemy), silver chalice
- **Exits**: Down (to Cyclops Room)
- **Commands**: `kill thief with knife` (multiple times)

## Complex Areas and Puzzles

### The Maze
- **Entry Point**: West from Troll Room
- **Exit Point**: Northwest to Dam Lobby or Northeast to Grating Room
- **Key Items**: Skeleton key, bag of coins
- **Exact Path**: `west`, `north`, `east`, `south`, `west`, `up`, `down`, `north`, `east`, `northeast`, `northwest`

### Dealing with the Thief
1. Avoid the thief until you have the nasty knife
2. Find him in the Treasure Room (up from Cyclops Room)
3. Kill him with the knife to recover stolen treasures
4. He will open the jeweled egg if he steals it

### Navigating from Forest to House
- **From Forest Path (after getting egg)**:
  1. `go south` → North of House
  2. `go east` → East of House
  3. `go north` → Behind House
  4. `open window` → Opens window
  5. `enter house` → Kitchen

### All Treasures and Their Locations
1. Painting - Gallery
2. Gold Coffin - Egyptian Room
3. Jeweled Sceptre - Inside Coffin
4. Pot of Gold - End of Rainbow (after waving sceptre)
5. Crystal Skull - Land of the Dead
6. Trunk of Jewels - Reservoir
7. Crystal Trident - Atlantis Room
8. Jeweled Egg - Tree in Forest Path
9. Golden Canary - Inside Egg (opened by thief)
10. Large Emerald - Inside Buoy
11. Scarab - Sandy Cave (must dig)
12. Bag of Coins - Maze
13. Platinum Bar - Loud Room (say "echo")
14. Jade Figurine - Bat Room
15. Silver Chalice - Treasure Room
16. Sapphire Bracelet - Gas Room
17. Brass Bauble - From songbird (after winding canary)
18. Diamond - From coal in machine
19. Ancient Map - Appears when all treasures are collected
