# alien-invasion
Alien invasion is a python game created using pygame library, Most of the code here is from Eric Matthes' "Python Crash Course", though I have added some gameplay  changes. 

![Screenshot from 2021-09-29 15-00-55](https://user-images.githubusercontent.com/66839270/135273873-c16cf04f-a8ee-45d2-bcb0-58f0797e8471.png)

#### Major changes include:

  * Changed background color with an image background 
  * Changed ship image and alien image
  * Added key up and down for the ship to apply free moving 
  * Added 'Enter' key to start the game 
  * Added a feature that saves the high score so it isn't reset each time you start the game 
  * Added sound effects
    * background music
    * ship crash sound 
    * shooting sound
    * game over sound 
 
## game description

In Alien Invasion, the player controls a ship that appears at the bottom center of the screen. \
The player can move the ship right, left, up, and down using the arrow keys and shoot bullets using the spacebar. \
When the game begins, a fleet of aliens fills the skyand moves across and down the screen. \
The player shoots and destroys the aliens. If the player shoots all the aliens, a new fleet appears that moves faster than the previous fleet.
If any alien hits the player’s ship or reaches the bottom of the screen, the player loses a ship. If the player loses three ships, the game ends.

## requirements
* python3 
* pygame

To run:
```
python alien_invasion.py
```
