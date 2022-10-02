"""
GameFunctions.py
This file contains the functions used throughout the entire game, including event handling and frame by frame updates.
"""

import pygame


# Event Handling
def check_events(joystick, jack):
    # Check for a quit event or event where escape is pressed, then pass it on to key press handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

    # Keyboard key presses
    key_presses(jack)

    # Controller button presses
    if joystick is not None:
        if joystick.get_name() is 'PS4 Controller':
            PS4_button_presses(joystick, jack)
        else:
            # Assume Xbox 360 controller by default
            Xbox_360_button_presses(joystick, jack)

    # Keep the game running
    return True


# The controls functions do not use key down/up event detection as pygame seems to have major flaws with it
# Keyboard controls
def key_presses(jack):
    # D
    if pygame.key.get_pressed()[pygame.K_d]:
        jack.right_press(True)
    else:
        jack.right_press(False)
    # A
    if pygame.key.get_pressed()[pygame.K_a]:
        jack.left_press(True)
    else:
        jack.left_press(False)
    # W
    if pygame.key.get_pressed()[pygame.K_w]:
        jack.up_press(True)
    else:
        jack.up_press(False)
    # S
    if pygame.key.get_pressed()[pygame.K_s]:
        jack.down_press(True)
    else:
        jack.down_press(False)
    # SPACEBAR
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        jack.jump_press(True)
    else:
        jack.jump_press(False)
    # SHIFT
    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
        jack.invincidash(True)
    else:
        jack.invincidash(False)
    # QUOTE
    if pygame.key.get_pressed()[pygame.K_QUOTE]:
        jack.melee_pressed = True
    else:
        jack.melee_pressed = False
    # ENTER
    if pygame.key.get_pressed()[pygame.K_RETURN]:
        jack.ranged_pressed = True
    else:
        jack.ranged_pressed = False

# PS4 controller controls
def PS4_button_presses(joystick, jack):
    # D-pad
    x, y = joystick.get_hat(0)
    # D-pad right or Left stick right
    if x == 1 or joystick.get_axis(0) > 0.5:
        jack.right_press(True)
    else:
        jack.right_press(False)
    # D-pad left or Left stick left
    if x == -1 or joystick.get_axis(0) < -0.5:
        jack.left_press(True)
    else:
        jack.left_press(False)
    # D-pad up or Left stick up
    if y == 1 or joystick.get_axis(1) < -0.5:
        jack.up_press(True)
    else:
        jack.up_press(False)
    # D-pad down or Left stick down
    if y == -1 or joystick.get_axis(1) > 0.5:
        jack.down_press(True)
    else:
        jack.down_press(False)
    # X button
    if joystick.get_button(0):
        jack.jump_press(True)
    else:
        jack.jump_press(False)
    # Right shoulder button(RB)
    if joystick.get_button(10):
        jack.invincidash(True)
    else:
        jack.invincidash(False)
    # Square button
    if joystick.get_button(2):
        jack.melee_pressed = True
    else:
        jack.melee_pressed = False
    # Circle button
    if joystick.get_button(1):
        jack.ranged_pressed = True
    else:
        jack.ranged_pressed = False

# Xbox 360 controller controls
def Xbox_360_button_presses(joystick, jack):
    # D-pad
    x, y = joystick.get_hat(0)
    # D-pad right or Left stick right
    if x == 1 or joystick.get_axis(0) > 0.5:
        jack.right_press(True)
    else:
        jack.right_press(False)
    # D-pad left or Left stick left
    if x == -1 or joystick.get_axis(0) < -0.5:
        jack.left_press(True)
    else:
        jack.left_press(False)
    # D-pad up or Left stick up
    if y == 1 or joystick.get_axis(1) < -0.5:
        jack.up_press(True)
    else:
        jack.up_press(False)
    # D-pad down or Left stick down
    if y == -1 or joystick.get_axis(1) > 0.5:
        jack.down_press(True)
    else:
        jack.down_press(False)
    # A button
    if joystick.get_button(0):
        jack.jump_press(True)
    else:
        jack.jump_press(False)
    # Right shoulder button(RB)
    if joystick.get_button(5):
        jack.invincidash(True)
    else:
        jack.invincidash(False)
    # X button
    if joystick.get_button(2):
        jack.melee_pressed = True
    else:
        jack.melee_pressed = False
    # B button
    if joystick.get_button(1):
        jack.ranged_pressed = True
    else:
        jack.ranged_pressed = False

def update_character_inputs(cur_time, jack):
    jack.determine_state(cur_time)

def update_ai(cur_time, leaves, jack, enemies):
    for enemy in enemies:
        enemy.decide_next_move(cur_time, leaves, jack)

    for enemy in enemies:
        enemy.update_attacks(cur_time, leaves)

# Update the positions of all moving objects
def update_positions(w_settings, surfaces, ranged_attacks, leaves, jack, enemies, cur_time):
    # Move Jack
    jack.update_pos()

    # Move the enemies
    for enemy in enemies:
        enemy.update_pos()

    # Move all ranged attacks
    for ranged_attack in ranged_attacks:
        ranged_attack.update_position()
        # Delete ranged attacks that have moved off the screen
        if ranged_attack.rect.right < 0 or ranged_attack.rect.left > w_settings.screen_width:
            ranged_attacks.remove(ranged_attack)

    # Move all leaves
    for leaf in leaves:
        leaf.update_pos(cur_time)
        # Delete leaves that have moved off the screen
        if leaf.ready_to_delete():
            leaves.remove(leaf)

    # Immediately after everything has been moved deal with any collisions
    check_collisions(surfaces, ranged_attacks, leaves, jack, enemies)

# Deal with any collisions between objects and characters
def check_collisions(surfaces, ranged_attacks, leaves, jack, enemies):
    check_character_to_character_collisions(jack, enemies)  # Less important position changes first
    check_character_to_surface_collision(surfaces, ranged_attacks, jack, enemies)  # Most important position changes last
    check_attack_collisions(surfaces, ranged_attacks, leaves, jack, enemies)  # Damage and state change checks

# Change position to keep characters from overlapping
def check_character_to_character_collisions(jack, enemies):
    for enemy in enemies:
        jack.check_collision_with_enemy(enemy)

# Make sure characters do not overlap with surfaces like blocks
def check_character_to_surface_collision(surfaces, ranged_attacks, jack, enemies):
    jack.check_surface_collisions(surfaces, ranged_attacks)
    for enemy in enemies:
        enemy.check_surface_collisions(surfaces)

# Damage and state changes due to attacks can be found here
def check_attack_collisions(surfaces, ranged_attacks, leaves, jack, enemies):
    jack.check_attack_collisions(leaves)
    for enemy in enemies:
        enemy.check_attack_collisions(surfaces, ranged_attacks, jack.melee)
        if enemy.health <= 0:
            enemies.remove(enemy)

def update_animations(cur_time, ranged_attacks, jack, enemies):
    jack.update_animation()

    for enemy in enemies:
        enemy.update_animation(cur_time)

    for ranged_attack in ranged_attacks:
        ranged_attack.update_animation(cur_time)

# Display a new screen based on all object locations
def update_screen(screen, UI, bg_blocks, surfaces, ranged_attacks, leaves, jack, boss, enemies):
    # Wipe the current screen
    screen.new_frame()

    # Start with the background
    for bg_block in bg_blocks:
        screen.blit_obj(bg_block)

    # Next the foreground
    for surface in surfaces:
        for block in surface.blocks:
            screen.blit_obj(block)

    # Next the enemies
    for enemy in enemies:
        enemy.blit_me(screen)

    # Next the player's character
    jack.blit_me(screen)

    # Next the enemies attacks
    for leaf in leaves:
        screen.blit_obj(leaf)

    # Next the player's attacks
    for ranged_attack in ranged_attacks:
        screen.blit_obj(ranged_attack)

    # Last the user interface
    UI.display(screen, jack, boss)

    # Display everything in full screen
    screen.display_frame()
