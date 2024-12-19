import os

files_to_check = [
    "background.jpg",
    "player.png",
    "enemy.png",
    "bullet.png",
    "powerup.png",
    "boss.png",
    "shoot.wav",
    "hit.wav",
    "powerup.wav",
    "boss_hit.wav",
    "background_music.mp3"
]

missing_files = [file for file in files_to_check if not os.path.exists(file)]

if missing_files:
    print("Missing files:", missing_files)
else:
    print("All files are in place!")
