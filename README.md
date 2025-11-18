# **ROGUE-LITE 2D DUNGEON CRAWLER (V1.0)**

Project Page: *(replace with your link)*

A generated rogue lite game built using **Python** and **pygame**. Your goal: survive, descend as many levels as possible, and achieve the highest score.

------------------------------------------------------------------------

## **1. Game Overview & Features**

### **Core Features**

-   **Dynamic Procedural Map Generation**\
    Every level is fully randomized with unique rooms and tunnels.

-   **Four Enemy Types (with AI behaviors):**

    -   **Standard (Red):** Basic chasing behavior.\
    -   **Tank (Grey):** Slow, high health, damage sponge.\
    -   **Shooter (Green):** Maintains distance, fires magical
        projectiles.\
    -   **Charger (Orange):** Stops, locks onto the player, and dashes
        at high speed.

-   **Player Progression**

    -   XP & level-up system\
    -   Increased max health on level-up\
    -   Score saving (persistent high score)

-   **Game Juice / Visual Feedback**

    -   Screen shake when taking damage\
    -   Floating damage numbers (e.g., `-5`)\
    -   Particle explosions on kills and projectile impacts\
    -   Invincibility frames (flashing)

-   **Persistence**

    -   High score saved to `highscore.txt`

------------------------------------------------------------------------

## **2. Getting Started**

### **Requirements**

-   Python 3.x\
-   Pygame

Install Pygame:

``` bash
pip install pygame
```

### **Running the Game**

1.  Place `main.py`, `sprites.py`, and `map.py` **in the same folder**.
2.  Open a terminal and navigate to the folder.
3.  Run:

``` bash
python main.py
```

------------------------------------------------------------------------

## **3. Audio Asset Setup (IMPORTANT)**

The game expects specific audio filenames.\
Without them the game will run but **without sound**.

### Required Audio Files

| Type   | Filename            | Used For                      |
|--------|----------------------|-------------------------------|
| .wav   | `music.wav`          | Background music (loops)      |
| .wav   | `shoot.wav`          | Player ranged attack          |
| .wav   | `player_hit.wav`     | Player taking damage          |
| .wav   | `enemy_hit.wav`      | Enemy taking damage           |
| .wav   | `level_up.wav`       | Player leveling up            |
| .wav   | `pickup_powerup.wav` | Picking up a power-up         |


These files must be in the **same folder as `main.py`**.

------------------------------------------------------------------------

## **4. Controls & Objectives**

### Controls

| Input              | Action                       |
|--------------------|------------------------------|
| **W A S D**        | Movement                     |
| **Left Mouse Click** | Shoot projectile (Magic Bolt) |
| **Spacebar**       | Melee attack (Sword)         |
| **Space** (Menu)   | Start the game               |
| **R** (Game Over)  | Restart the game             |


### **Objective**

Find the **stairs (yellow tile)** on each floor to descend deeper.\
Defeat enemies, gain XP, level up, and try to beat your high score!

