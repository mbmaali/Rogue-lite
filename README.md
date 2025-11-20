# **ROGUE-LITE**

Project Page: *https://mbmaali.itch.io/rogue-lite-2*

A generated rogue lite game built using **Python** and **pygame**. Your goal: survive, descend as many levels as possible, and achieve the highest score.

------------------------------------------------------------------------

## 1. Game Overview

This game features fully procedural levels, multiple enemy types, and a
simple progression system that keeps each run feeling different.

### Main Features

-   **Randomly generated maps**\
    Every floor is new---rooms, tunnels, enemy placement, all different
    each time.

-   **Four enemy types**, each with unique behavior:

    -   **Red -- Chaser:** Runs straight at you.
    -   **Grey -- Tank:** Slow, bulky, takes a lot of hits.
    -   **Green -- Shooter:** Keeps distance and fires projectiles.
    -   **Orange -- Charger:** Pauses, locks on, then dashes fast.

-   **Player progression**

    -   Gain XP from kills\
    -   Level up to increase max health\
    -   Persistent high score saved locally

-   **Visual feedback / Game juice**

    -   Screen shake when you take damage\
    -   Floating damage numbers\
    -   Particle effects on hits and kills\
    -   Temporary invincibility flashes after being hit

-   **Data saved locally**

    -   High score stored in `highscore.txt`

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

