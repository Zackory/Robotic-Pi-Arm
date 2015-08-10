import pygame
import lightblue

# Connect to bluetooth on Raspberry Pi
s = lightblue.socket()
s.connect(('00:0A:3A:84:1F:A6', 5))

# Initialize arm positions
done = False
base = 90
arm = 90
forearm = 90
gripper = 45

pygame.init()

while not done:
    keys = pygame.key.get_pressed()

    done = keys[pygame.K_ESCAPE]

    if keys[pygame.K_d] and base < 180:
        base += 1
    if keys[pygame.K_a] and base > 0:
        base -= 1

    if keys[pygame.K_w] and arm < 180:
        arm += 1
    if keys[pygame.K_s] and arm > 1:
        arm -= 1

    if keys[pygame.K_UP] and forearm < 180:
        forearm += 1
    elif keys[pygame.K_DOWN] and forearm > 1:
        forearm -= 1

    if keys[pygame.K_LEFT] and gripper < 70:
        gripper += 1
    elif keys[pygame.K_RIGHT] and gripper > 25:
        gripper -= 1

    s.send('%f,%f,%f,%f' % (base, arm, forearm, gripper))

s.send('Done')

s.close()
