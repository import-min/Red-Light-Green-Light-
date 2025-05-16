<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;"># Minahal Aisha
# vnc9uv

import pygame
import gamebox
import random

# setting up the screen size
camera = gamebox.Camera(800, 600)

# global variables
frame_player = 0
counter = 0
marker = 0
alive = True
health = 100
timer_tracker = 0
game_start = False


# setup default values in a function
def setup():
    """
    This function resets all the global variables and images to their original values. It is called when the game is
    reset.
    :return: None
    """
    global frame_player, counter, marker, alive, player_character, player_sprite_sheet, rocks, logs, health_coins
    global timer_coins, health, timer, timer_tracker, time_left

    # resetting global variables
    frame_player = 0
    counter = 0
    marker = 0
    health = 100
    timer_tracker = 0
    time_left = 60
    timer = gamebox.from_text(775, 30, str(time_left), 50, "dark gray")
    alive = True

    # resetting player position
    player_sprite_sheet = gamebox.load_sprite_sheet("player-sprite.png", 1, 6)
    player_character = gamebox.from_image(400, 550, player_sprite_sheet[frame_player])

    # resetting obstacle &amp; coin placement
    rocks = [gamebox.from_image(random.randint(50, 180), random.randint(180, 280), "rock1.png"),
             gamebox.from_image(random.randint(370, 450), random.randint(180, 280), "rock2.png"),
             gamebox.from_image(random.randint(670, 750), random.randint(180, 280), "rock3.png"),
             gamebox.from_image(random.randint(50, 200), random.randint(300, 410), "rock4.png"),
             gamebox.from_image(random.randint(300, 500), random.randint(300, 410), "rock5.png"),
             gamebox.from_image(random.randint(570, 750), random.randint(300, 410), "rock6.png")]
    logs = [gamebox.from_image(random.randint(50, 200), random.randint(420, 560), "log1.png"),
            gamebox.from_image(random.randint(300, 500), random.randint(420, 480), "log2.png"),
            gamebox.from_image(random.randint(570, 750), random.randint(420, 560), "log3.png")]
    health_coins = [gamebox.from_image(random.randint(250, 275), random.randint(300, 410), "health-coin1.png"),
                    gamebox.from_image(random.randint(520, 560), random.randint(420, 560), "health-coin1.png")]
    timer_coins = [gamebox.from_image(random.randint(250, 275), random.randint(420, 560), "timer-coin.png"),
                   gamebox.from_image(random.randint(520, 560), random.randint(300, 410), "timer-coin.png")]

    # redrawing obstacles
    for rock in rocks:
        camera.draw(rock)
    for log in logs:
        camera.draw(log)
    # redrawing collectibles
    for coin in health_coins:
        camera.draw(coin)
    for coin in timer_coins:
        camera.draw(coin)


# drawing stationary items
background = gamebox.from_image(400, 300, "background.jpgw")
finish_line = gamebox.from_color(400, 148, "red", 800, 2)
stationary_items = [background, finish_line]

# these are stationary items that get randomized placement every time
rocks = [gamebox.from_image(random.randint(50, 180), random.randint(180, 280), "rock1.png"),
         gamebox.from_image(random.randint(370, 450), random.randint(180, 280), "rock2.png"),
         gamebox.from_image(random.randint(670, 750), random.randint(180, 280), "rock3.png"),
         gamebox.from_image(random.randint(50, 200), random.randint(300, 410), "rock4.png"),
         gamebox.from_image(random.randint(300, 500), random.randint(300, 410), "rock5.png"),
         gamebox.from_image(random.randint(570, 750), random.randint(300, 410), "rock6.png")]
logs = [gamebox.from_image(random.randint(50, 200), random.randint(420, 560), "log1.png"),
        gamebox.from_image(random.randint(300, 500), random.randint(420, 480), "log2.png"),
        gamebox.from_image(random.randint(570, 750), random.randint(420, 560), "log3.png")]
health_coins = [gamebox.from_image(random.randint(250, 275), random.randint(300, 410), "health-coin1.png"),
                gamebox.from_image(random.randint(520, 560), random.randint(420, 560), "health-coin1.png")]
timer_coins = [gamebox.from_image(random.randint(250, 275), random.randint(420, 560), "timer-coin.png"),
               gamebox.from_image(random.randint(520, 560), random.randint(300, 410), "timer-coin.png")]

# drawing the player
player_sprite_sheet = gamebox.load_sprite_sheet("player-sprite.png", 1, 6)
player_character = gamebox.from_image(400, 550, player_sprite_sheet[frame_player])

# drawing the doll
doll = gamebox.from_image(400, 80, "doll.png")
doll_facing_front = gamebox.from_image(402, 40, "dollhead.png")

# drawing the timer
time_left = 60
timer = gamebox.from_text(775, 30, str(time_left), 50, "dark gray")


# drawing the game over screen
def game_over():
    """
    This function draws the game over screen.
    :return: None
    """
    game_over_image = gamebox.from_image(400, 300, "game-over-sign.jpg")
    camera.draw(game_over_image)


# making player move
def player_movement():
    """
    This function allows the sprite of the player to move as the user moves forward or to the right/left.
    :return: None
    """
    global frame_player, counter
    counter += 1
    if counter % 1 == 0:
        frame_player += 1
        if frame_player == 5:
            frame_player = 0
        player_character.image = player_sprite_sheet[frame_player]
        counter = 0


# updating the timer as the game is played
def update_timer():
    """
    This function is what makes the timer go down from 60 seconds to 0 seconds.
    :return: None
    """
    global timer_tracker, time_left, timer
    timer_tracker += 1
    if timer_tracker % 10 == 0:
        time_left -= 1
        timer = gamebox.from_text(775, 30, str(time_left), 50, "dark gray")
    camera.draw(timer)


def tick(keys):
    """
    This is the function that makes the game playable as it breaks down every screen based on a tick. The individual
    components of this function are commented on throughout it. In general, it updates the screen every .1 second.
    :param keys: This is the required parameter for a gamebox tick function.
    :return: None
    """
    global game_start, frame_player, counter, alive, marker, health, time_left
    if game_start:  # if the user follows the start screen instructions, the game starts and this section runs
        if alive:
            # stationary items
            for item in stationary_items:
                camera.draw(item)
            # obstacles
            for rock in rocks:
                camera.draw(rock)
            for log in logs:
                camera.draw(log)
            # collectibles
            for coin in health_coins:
                camera.draw(coin)
            for coin in timer_coins:
                camera.draw(coin)

            # timer
            update_timer()
            if time_left == 0:
                game_over()
                alive = False

            # health bar
            health_bar = gamebox.from_color(110, 20, "yellow", health, 20)
            camera.draw(health_bar)

            # reducing health if player touches obstacle
            for rock in rocks:
                if player_character.touches(rock):
                    health -= 10
                    if health &lt; 0:
                        game_over()
                        alive = False
            for log in logs:
                if player_character.touches(log):
                    health -= 10
                    if health &lt; 0:
                        game_over()
                        alive = False

            # increasing health/time with collectibles
            for coin in health_coins:
                if player_character.touches(coin):
                    health += 20
                    health_coins.remove(coin)
            for coin in timer_coins:
                if player_character.touches(coin):
                    time_left += 20
                    timer_coins.remove(coin)

            # player sprite movement
            if pygame.K_SPACE in keys:
                player_movement()
                player_character.y -= 3
            if pygame.K_LEFT in keys:
                player_character.x -= 3
            if pygame.K_RIGHT in keys:
                player_character.x += 3

            # displaying character
            camera.draw(player_character)

            # moving the doll and eliminating player if they move while the doll is facing the character
            marker += 1
            if marker % 40 == 0:
                camera.draw(doll)
                camera.draw(doll_facing_front)
                if pygame.K_SPACE in keys:
                    game_over()
                    alive = False
                if pygame.K_LEFT in keys:
                    game_over()
                    alive = False
                if pygame.K_RIGHT in keys:
                    game_over()
                    alive = False
            else:
                camera.draw(doll)

            # winning
            if player_character.y &lt; 118:
                win_screen = gamebox.from_image(400, 300, "win-screen.jpg")
                camera.draw(win_screen)
                alive = False
        else:  # if the player looses the game and they want to restart
            if pygame.K_UP in keys:
                alive = True
                setup()
    else:  # this code runs if the game has just been started and it displays the start screen
        start_screen_image = gamebox.from_image(400, 300, "starting-screen.jpg")
        camera.draw(start_screen_image)
        if pygame.K_m in keys:
            game_start = True
    camera.display()


# this calls the tick function every .1 second
gamebox.timer_loop(10, tick)

# image citations
# player-sprite.png
    # https://i.postimg.cc/c1Y9q87P/player-sprite.png
# rock1.png
    # https://i.postimg.cc/BvL5xdMR/rock1.png
# rock2.png
    # https://i.postimg.cc/J4rbTypN/rock2.png
# rock3.png
    # https://i.postimg.cc/4dv9PZt2/rock3.png
# rock4.png
    # https://i.postimg.cc/vZpxdDtS/rock4.png
# rock5.png
    # https://i.postimg.cc/MKLvyXNK/rock5.png
# rock6.png
    # https://i.postimg.cc/T14YqHkH/rock6.png
# log1.png
    # https://i.postimg.cc/LX49dMwb/log1.png
# log2.png
    # https://i.postimg.cc/0ypPbQq4/log2.png
# log3.png
    # https://i.postimg.cc/k45m1vtr/log3.png
# health_coin1.png
    # https://i.postimg.cc/w38npX3j/health-coin1.png
# timer_coin.png
    # https://i.postimg.cc/G2Bc3j3F/timer-coin.png
# background.jpgw
    # https://i.postimg.cc/J4r2bzJg/background.jpgw
# doll.png
    # https://i.postimg.cc/sDHw793Q/doll.png
# dollhead.png
    # https://i.postimg.cc/mk2yFhqy/dollhead.png
# game_over_sign.jpg
    # https://i.postimg.cc/5NrS64m8/game-over-sign.jpg
# win_screen.jpg
    # https://i.postimg.cc/J0njzvDT/win-screen.jpg
# starting-screen.jpg
    # https://i.postimg.cc/Hnb1VYJz/starting-screen.jpg</pre></body></html>
