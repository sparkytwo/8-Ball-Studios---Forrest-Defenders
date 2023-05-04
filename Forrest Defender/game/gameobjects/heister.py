import math

import pyasge
from game.spritesheet import Spritesheet

from game.gameobjects.gamemap import GameMap


class Heister:
    def __init__(self):
        self.spritesheet = Spritesheet("/data/sprites/heisters/elf/elf_spritesheet.png")

        self.torso_unarmed_walk_frames = [
            self.spritesheet.parseSprite('elfWalk_00.png'),
            self.spritesheet.parseSprite('elfWalk_01.png'),
            self.spritesheet.parseSprite('elfWalk_02.png'),
            self.spritesheet.parseSprite('elfWalk_03.png'),
            self.spritesheet.parseSprite('elfWalk_04.png'),
            self.spritesheet.parseSprite('elfWalk_05.png'),
            self.spritesheet.parseSprite('elfWalk_06.png')
        ]

        self.torso_M16_walk_frames = [
            self.spritesheet.parseSprite('elfWalk_00.png'),
            self.spritesheet.parseSprite('elfWalk_01.png'),
            self.spritesheet.parseSprite('elfWalk_02.png'),
            self.spritesheet.parseSprite('elfWalk_03.png'),
            self.spritesheet.parseSprite('elfWalk_04.png'),
            self.spritesheet.parseSprite('elfWalk_05.png'),
            self.spritesheet.parseSprite('elfWalk_06.png'),
            self.spritesheet.parseSprite('elfWalk_07.png')
        ]

        self.torso_M16_attack_frames = [
            self.spritesheet.parseSprite('elfAttack_00.png'),
            self.spritesheet.parseSprite('elfAttack_01.png'),
            self.spritesheet.parseSprite('elfAttack_02.png'),
            self.spritesheet.parseSprite('elfAttack_03.png'),
            self.spritesheet.parseSprite('elfAttack_04.png'),
            self.spritesheet.parseSprite('elfAttack_05.png'),
            self.spritesheet.parseSprite('elfAttack_06.png'),
            self.spritesheet.parseSprite('elfAttack_07.png'),
            self.spritesheet.parseSprite('elfAttack_08.png'),
            self.spritesheet.parseSprite('elfAttack_09.png'),
            self.spritesheet.parseSprite('elfAttack_10.png'),
            self.spritesheet.parseSprite('elfAttack_11.png')
        ]

        self.leg_frames = [
            self.spritesheet.parseSprite('elfLegs_00.png'),
            self.spritesheet.parseSprite('elfLegs_01.png'),
            self.spritesheet.parseSprite('elfLegs_02.png'),
            self.spritesheet.parseSprite('elfLegs_03.png'),
            self.spritesheet.parseSprite('elfLegs_04.png'),
            self.spritesheet.parseSprite('elfLegs_05.png'),
            self.spritesheet.parseSprite('elfLegs_06.png'),
            self.spritesheet.parseSprite('elfLegs_07.png'),
            self.spritesheet.parseSprite('elfLegs_08.png'),
            self.spritesheet.parseSprite('elfLegs_09.png'),
            self.spritesheet.parseSprite('elfLegs_10.png'),
            self.spritesheet.parseSprite('elfLegs_11.png'),
            self.spritesheet.parseSprite('elfLegs_12.png'),
            self.spritesheet.parseSprite('elfLegs_13.png'),
            self.spritesheet.parseSprite('elfLegs_14.png')
        ]

        self.current_weapon = 1
        if self.current_weapon == 0:
            self.active_torso_frame = self.torso_unarmed_walk_frames[0]
            self.active_torso_frame.scale = 3

            self.active_leg_frame = self.leg_frames[0]
            self.active_leg_frame.scale = 3

            # sprite animation variables
            self.torso_animation_frame = 0
            self.torso_animation_frames = self.torso_unarmed_walk_frames

        if self.current_weapon == 1:
            self.active_torso_frame = self.torso_M16_walk_frames[0]
            self.active_torso_frame.scale = 3

            self.active_leg_frame = self.leg_frames[0]
            self.active_leg_frame.scale = 3


            # sprite animation variables
            self.torso_animation_frame = 0
            self.torso_animation_frames = self.torso_M16_walk_frames

        self.pos_x = 200
        self.pos_y = 3500
        self.angle = 0

        self.leg_animation_frame = 0
        self.leg_animation_frames = self.leg_frames

        self.animation_speed = 0.3  # adjust as needed
        self.moving = False

        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/sprites/heisters/chief/debug.png")

        self.max_ammo = 120
        self.ammo = 100
        self.ammo_in_magazine = 20
        self.firing = False
        self.fire_delay = 0
        self.fire_rate = 0.6

        self.active_torso_frame.z_order = 10
        self.active_leg_frame.z_order = 10

        self.health = 5
        self.i_clock = 3

        self.win = False
        self.loose = False

    def update_position(self, key_states: set, game_map: GameMap):
        self.dx, self.dy = 0, 0

        tile_size = game_map.tile_size
        tile_x = int((self.pos_x + self.active_torso_frame.width) / tile_size[0])
        tile_y = int((self.pos_y + self.active_torso_frame.height) / tile_size[1])

        if pyasge.KEYS.KEY_A in key_states:
            if game_map.costs[tile_y][tile_x - 1] == 0:
                self.dx -= 10
                self.moving = True
            if game_map.costs[tile_y][tile_x - 1] == 2:
                self.win = True
                print("pain")
        if pyasge.KEYS.KEY_D in key_states:
            if game_map.costs[tile_y][tile_x + 1] == 0:
                self.dx += 10
                self.moving = True
            if game_map.costs[tile_y][tile_x + 1] == 2:
                self.win = True
                print("pain")
        if pyasge.KEYS.KEY_W in key_states:
            if game_map.costs[tile_y - 1][tile_x] == 0:
                self.dy -= 10
                self.moving = True
            if game_map.costs[tile_y - 1][tile_x] == 2:
                self.win = True
                print("pain")
        if pyasge.KEYS.KEY_S in key_states:
            if game_map.costs[tile_y + 1][tile_x] == 0:
                self.dy += 10
                self.moving = True
            if game_map.costs[tile_y + 1][tile_x] == 2:
                self.win = True
                print("pain")
        if self.dx == 0 and self.dy == 0:
            self.moving = False
        self.pos_x += self.dx
        self.pos_y += self.dy

    def update_cursor(self, cursor: pyasge.Sprite):
        cursor.x += self.dx
        cursor.y += self.dy
        # calculate the angle to the cursor
        cursor_x = cursor.x + cursor.width / 2
        cursor_y = cursor.y + cursor.height / 2
        delta_x = cursor_x - self.pos_x
        delta_y = cursor_y - self.pos_y
        self.angle = math.atan2(delta_y, delta_x)

    def update_animation(self):
        self.active_torso_frame.z_order = 10
        self.active_leg_frame.z_order = 10

        if self.firing:
            self.torso_animation_frames = self.torso_M16_attack_frames
            self.torso_animation_frame += self.animation_speed
            if self.torso_animation_frame >= len(self.torso_animation_frames):
                self.torso_animation_frames = self.torso_M16_walk_frames
                self.torso_animation_frame = 0
            self.active_torso_frame = self.torso_animation_frames[int(self.torso_animation_frame)]


        elif self.moving:
            self.torso_animation_frame += self.animation_speed
            self.leg_animation_frame += self.animation_speed

            if self.torso_animation_frame >= len(self.torso_animation_frames):
                self.torso_animation_frame = 0

            if self.leg_animation_frame >= len(self.leg_animation_frames):
                self.leg_animation_frame = 0

            self.active_torso_frame = self.torso_animation_frames[int(self.torso_animation_frame)]
            self.active_leg_frame = self.leg_animation_frames[int(self.leg_animation_frame)]

        elif self.moving == False:
            self.torso_animation_frame = 0
            self.leg_animation_frame = 0
            self.active_leg_frame = self.leg_animation_frames[int(self.torso_animation_frame)]
            self.active_torso_frame = self.torso_animation_frames[int(self.torso_animation_frame)]

        if self.firing == False:
            self.torso_animation_frames = self.torso_M16_walk_frames
            self.torso_animation_frame = 0
            self.active_torso_frame = self.torso_animation_frames[int(self.torso_animation_frame)]

        torso_half_width = self.active_torso_frame.width / 2
        torso_half_height = self.active_torso_frame.height / 2

        self.active_torso_frame.scale = 3
        self.active_torso_frame.x = self.pos_x - torso_half_width
        self.active_torso_frame.y = self.pos_y - torso_half_height
        self.active_torso_frame.rotation = self.angle

        leg_half_width = self.active_leg_frame.width / 2
        leg_half_height = self.active_leg_frame.height / 2

        self.active_leg_frame.scale = 3
        self.active_leg_frame.x = self.pos_x 
        self.active_leg_frame.y = self.pos_y
        self.active_leg_frame.rotation = self.angle

        self.sprite.scale = 3
        self.sprite.x = self.pos_x - torso_half_width
        self.sprite.y = self.pos_y
        self.sprite.rotation = self.angle

    def click_handler(self, event: pyasge.ClickEvent) -> None:

        if event.button is pyasge.MOUSE.MOUSE_BTN1 and event.action is pyasge.MOUSE.BUTTON_PRESSED:
            self.firing = True
        if event.button is pyasge.MOUSE.MOUSE_BTN1 and event.action is pyasge.MOUSE.BUTTON_RELEASED:
            self.firing = False

    def update(self, key_states: set, bullets, Bullet, cursor: pyasge.Sprite, game_map: GameMap,
               game_time: pyasge.GameTime, audio_system, sounds):

        self.i_clock += 1 * game_time.fixed_timestep

        tile_size = game_map.tile_size
        tile_x = int((self.pos_x + self.active_torso_frame.width) / tile_size[0])
        tile_y = int((self.pos_y + self.active_torso_frame.height) / tile_size[1])




        self.update_position(key_states, game_map)
        self.update_cursor(cursor)
        self.update_animation()
        if self.firing == True:
            if self.fire_delay == 0:
                # Fire bullet
                channel = audio_system.play_sound(sounds["shoot"])

                bullet = Bullet(self.sprite.midpoint, self.angle, self.pos_x,
                                self.pos_y, cursor.x, cursor.y, self.active_torso_frame.width)
                bullet.shot_by = "heister"
                bullets.append(bullet)
            self.fire_delay += self.fire_rate * game_time.fixed_timestep
            print(self.fire_delay)
            if self.fire_delay > 0.5:
                self.fire_delay = 0


    @property
    def midpoint(self) -> pyasge.Point2D:
        return self.sprite.midpoint



