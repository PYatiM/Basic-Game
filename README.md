
## Game Structure
The game is structured as a Python script with a single file. Here’s how it works:
1. The `show_menu` function displays the game menu.
2. The main game loop handles player inputs, enemy spawns, and game mechanics.
3. Collision detection checks if bullets hit enemies, power-ups are collected, and boss interactions.
4. The `draw_objects` function renders the player, bullets, enemies, and power-ups on the screen.
5. The game tracks player health, score, and level, and handles game over scenarios.

## License
This project is open-source and free to use. Feel free to modify and expand upon it for your needs.



### Asset Requirements
Ensure the following files are available in the same directory as the game script:
- `background.jpg`: Background image for the game.
- `player.png`: Image of the player character.
- `enemy.png`: Image of the enemy character.
- `bullet.png`: Image of the bullet.
- `powerup.png`: Image of the power-up item.
- `boss.png`: Image of the boss character.
- `shoot.wav`: Sound effect for shooting.
- `hit.wav`: Sound effect for enemy hit.
- `powerup.wav`: Sound effect for collecting a power-up.
- `boss_hit.wav`: Sound effect for boss hit.
- `background_music.mp3`: Background music for the game.

## Game Controls
- **Left Arrow**: Move player left
- **Right Arrow**: Move player right
- **Spacebar**: Shoot bullets
- **R**: Restart the game after Game Over
- **Enter**: Start the game from the menu
- **Q**: Quit the game from the menu



## How to Run
1. Place this script in a directory with all the necessary image and sound files listed above.
2. Make sure you have installed Python and Pygame.
3. Run the following command to start the game: python doom_game.py
