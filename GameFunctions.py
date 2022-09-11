"""
GameFunctions.py
This file contains the functions used throughout the entire game, including event handling and frame by frame updates.
"""

import pygame


# Event Handling
# Check for a quit event or event where escape is pressed, then pass it on to key press handling
def check_events(joystick, jack):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    keypresses(joystick, jack)

    return True


"""
Key press handling as well as joystick
This was written with an xbox 360 controller in mind, but it should work for other controllers as well.  It just might
mean that the buttons are in different places.
This function replaces key down/up events as pygame's event detection has major flaws
"""
def keypresses(joystick, jack):
    # D-pad
    x, y = joystick.get_hat(0)
    # D or D-pad right or Left stick right
    if pygame.key.get_pressed()[pygame.K_d] or x == 1 or joystick.get_axis(0) > 0.5:
        jack.right_press(True)
    else:
        jack.right_press(False)
    # A or D-pad left or Left stick left
    if pygame.key.get_pressed()[pygame.K_a] or x == -1 or joystick.get_axis(0) < -0.5:
        jack.left_press(True)
    else:
        jack.left_press(False)
    # W or D-pad up or Left stick up
    if pygame.key.get_pressed()[pygame.K_w] or y == 1 or joystick.get_axis(1) < -0.5:
        jack.up_press(True)
    else:
        jack.up_press(False)
    # S or D-pad down or Left stick down
    if pygame.key.get_pressed()[pygame.K_s] or y == -1 or joystick.get_axis(1) > 0.5:
        jack.down_press(True)
    else:
        jack.down_press(False)
    # SPACEBAR or bottom button(A)
    if pygame.key.get_pressed()[pygame.K_SPACE] or joystick.get_button(0):
        jack.jump_press(True)
    else:
        jack.jump_press(False)
    # SHIFT or Right shoulder button(RB)
    if pygame.key.get_pressed()[pygame.K_LSHIFT] or joystick.get_button(5):
        jack.invincidash(True)
    else:
        jack.invincidash(False)
    # QUOTE or left button(X)
    if pygame.key.get_pressed()[pygame.K_QUOTE] or joystick.get_button(2):
        jack.melee_pressed = True
    else:
        jack.melee_pressed = False
    # ENTER or right button(B)
    if pygame.key.get_pressed()[pygame.K_RETURN] or joystick.get_button(1):
        jack.ranged_pressed = True
    else:
        jack.ranged_pressed = False


def update_character_inputs(cur_time, jack):
    jack.determine_state(cur_time)

def update_ai(cur_time, surfaces, leaves, jack, enemies):
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
    check_collisions(surfaces, jack, enemies)

    # After Jack's position has been determined create his ranged attack if he is creating one
    if jack.ranged_is_created:
        ranged_attacks.add(jack.create_ranged_attack())


# Deal with any collisions between objects and characters
def check_collisions(surfaces, jack, enemies):
    check_character_to_surface_collision(surfaces, jack, enemies)
    check_attack_collisions(surfaces, enemies)

# Make sure characters do not overlap with surfaces like blocks
def check_character_to_surface_collision(surfaces, jack, enemies):
    jack.check_surface_collisions(surfaces)
    for enemy in enemies:
        enemy.check_surface_collisions(surfaces)

def check_attack_collisions(surfaces, enemies):
    for enemy in enemies:
        enemy.check_collisions(surfaces)

def update_animations(cur_time, ranged_attacks, jack, enemies):
    jack.update_animation()

    for enemy in enemies:
        enemy.update_animation(cur_time)

    for ranged_attack in ranged_attacks:
        ranged_attack.update_animation(cur_time)

# Display a new screen based on all object locations
def update_screen(screen, UI, bg_blocks, surfaces, ranged_attacks, leaves, jack, enemies):
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
    UI.display(screen, jack)

    # Display everything in full screen
    screen.display_frame()
