"""
GameFunctions.py
This file contains the functions used throughout the entire game, including event handling and frame by frame updates.
"""

import pygame
import MapGenerator as mg
from Classes.JackLumber import JackLumber
from Classes.TwistedLumber import TwistedLumber


# Event Handling
def check_events(joystick, jack, in_start_area, game_over, toggle_pause, pause_already_toggled):
    # Check for a quit event or event where escape is pressed, then pass it on to key press handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False, False, False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, False, False, False

    # Update currently pressed buttons and axes positions on controller
    joystick.set_all_values()

    # Apply values from the controller and keyboard key presses
    ready_to_load_next_area, toggle_pause, pause_already_toggled = key_presses(joystick, jack, in_start_area, game_over, toggle_pause, pause_already_toggled)

    # Keep the game running
    return True, ready_to_load_next_area, toggle_pause, pause_already_toggled

# This function does not use key down/up event detection as pygame seems to have major flaws with it
# Keyboard and Controller controls
def key_presses(joystick, jack, in_start_area, game_over, toggle_pause, pause_already_toggled):
    # D, D-pad right, or Left stick right
    if pygame.key.get_pressed()[pygame.K_d] or joystick.right_is_pressed():
        jack.right_press(True)
    else:
        jack.right_press(False)
    # A, D-pad left, or Left stick left
    if pygame.key.get_pressed()[pygame.K_a] or joystick.left_is_pressed():
        jack.left_press(True)
    else:
        jack.left_press(False)
    # W, D-pad up, or Left stick up
    if pygame.key.get_pressed()[pygame.K_w] or joystick.up_is_pressed():
        jack.up_press(True)
    else:
        jack.up_press(False)
    # S, D-pad down, or Left stick down
    if pygame.key.get_pressed()[pygame.K_s] or joystick.down_is_pressed():
        jack.down_press(True)
    else:
        jack.down_press(False)
    # SPACEBAR or controller's jump button
    if pygame.key.get_pressed()[pygame.K_SPACE] or joystick.jump_is_pressed():
        jack.jump_press(True)
    else:
        jack.jump_press(False)
    # SHIFT or controller's dash button
    if pygame.key.get_pressed()[pygame.K_LSHIFT] or joystick.dash_is_pressed():
        jack.invincidash(True)
    else:
        jack.invincidash(False)
    # QUOTE or controller's melee button
    if pygame.key.get_pressed()[pygame.K_QUOTE] or joystick.melee_is_pressed():
        jack.melee_pressed = True
    else:
        jack.melee_pressed = False
    # ENTER or controller's ranged button
    if pygame.key.get_pressed()[pygame.K_RETURN] or joystick.ranged_is_pressed():
        jack.ranged_pressed = True
    else:
        jack.ranged_pressed = False
    # / or controller's pause button
    ready_to_load_next_area = False
    if pygame.key.get_pressed()[pygame.K_SLASH] or joystick.pause_is_pressed():
        if not pause_already_toggled:
            if in_start_area or game_over:
                ready_to_load_next_area = True
            else:
                toggle_pause = True
            pause_already_toggled = True
    else:
        pause_already_toggled = False
        toggle_pause = False
    return ready_to_load_next_area, toggle_pause, pause_already_toggled


def update_character_inputs(cur_time, time_passed, jack):
    jack.determine_state(cur_time, time_passed)

def update_ai(cur_time, time_passed, leaves, jack, enemies):
    for enemy in enemies:
        enemy.decide_next_move(cur_time, time_passed, leaves, jack)

    for enemy in enemies:
        enemy.update_attacks(cur_time, leaves)

# Update the positions of all moving objects
def update_positions(w_settings, surfaces, ranged_attacks, leaves, jack, enemies, cur_time, time_passed):
    # Move Jack
    jack.update_pos(time_passed)

    # Move the enemies
    for enemy in enemies:
        enemy.update_pos(time_passed)

    # Move all ranged attacks
    for ranged_attack in ranged_attacks:
        ranged_attack.update_position(time_passed)
        # Delete ranged attacks that have moved off the screen
        if ranged_attack.rect.right < 0 or ranged_attack.rect.left > w_settings.screen_width:
            ranged_attacks.remove(ranged_attack)

    # Move all leaves
    for leaf in leaves:
        leaf.update_pos(cur_time, time_passed)
        # Delete leaves that have moved off the screen
        if leaf.ready_to_delete():
            leaves.remove(leaf)

    # Immediately after everything has been moved deal with any collisions
    check_collisions(surfaces, ranged_attacks, leaves, jack, enemies, time_passed)

# Deal with any collisions between objects and characters
def check_collisions(surfaces, ranged_attacks, leaves, jack, enemies, time_passed):
    check_character_to_character_collisions(jack, enemies, time_passed)  # Less important position changes first
    check_character_to_surface_collision(surfaces, ranged_attacks, jack, enemies)  # Most important position changes last
    check_attack_collisions(surfaces, ranged_attacks, leaves, jack, enemies)  # Damage and state change checks

# Change position to keep characters from overlapping
def check_character_to_character_collisions(jack, enemies, time_passed):
    for enemy in enemies:
        jack.check_collision_with_enemy(enemy, time_passed)

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
def update_screen(screen, in_start_area, UI, background, ranged_attacks, leaves, jack, boss, enemies):
    # Wipe the current screen
    screen.new_frame()

    # First the background
    screen.blit_img(background, [0, 0])

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
    game_over = False
    if in_start_area:
        UI.display_start_ui(screen, jack)
    else:
        UI.display_fight_ui(screen, jack, boss)
        game_over = check_for_game_over(screen, UI, jack, boss)  # Check for a game over

    # Display everything in full screen
    screen.display_frame()
    return game_over

def check_for_game_over(screen, UI, jack, boss):
    if jack.health <= 0 or boss is None or boss.health <= 0:
        UI.display_game_over(screen)
        return True
    return False

def load_next_area(w_settings, in_start_area, jack, enemies, ranged_attacks, leaves):
    if in_start_area:
        in_start_area = False
        boss = TwistedLumber(w_settings, 0, 0, True)
        enemies.add(boss)
        jack.__init__(w_settings, 0, 0, True)
        mg.load_map_vs_twisted_lumber(w_settings, jack, boss)
    else:  # If game over is True go back to the start screen
        in_start_area = True
        ranged_attacks.empty()
        leaves.empty()
        enemies.empty()
        boss = None
        jack.__init__(w_settings, 0, 0, True)
        mg.reload_map_start(w_settings, jack)
    return in_start_area, boss
