import math
import random

import pyasge
from game.spritesheet import Spritesheet
from game.pathfinding import pathfind


class Enemy_Ranged:
    def __init__(self):
        self.alive_spritesheet = Spritesheet("/data/sprites/SWAT/swatGruntSpriteSheet.png")

        self.torso_walk_frames = [
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_0.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_1.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_2.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_3.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_4.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_5.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_6.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_7.png')
        ]

        self.leg_frames = [
            self.alive_spritesheet.parseSprite('swatGruntLegs_00.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_01.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_02.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_03.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_04.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_05.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_06.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_07.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_08.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_09.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_10.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_11.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_12.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_13.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_14.png')
        ]

        self.dead_spritesheet = Spritesheet("/data/sprites/SWAT/swatGruntDeadSpriteSheet.png")
        self.dead_frames = [
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_1.png'),
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_2.png'),
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_3.png'),
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_4.png')
        ]
        self.active_dead_frame = self.dead_frames[0]

        self.active_torso_frame = self.torso_walk_frames[0]


        self.active_leg_frame = self.leg_frames[0]
        self.active_leg_frame.scale = 3

        self.pos_x = 0
        self.pos_y = 0
        self.angle = 0

        # sprite animation variables
        self.torso_animation_frame = 0
        self.torso_animation_frames = self.torso_walk_frames

        self.leg_animation_frame = 0
        self.leg_animation_frames = self.leg_frames

        self.animation_speed = 0.2  # adjust as needed
        self.moving = False

        self.health = 1
        self.alive = True

        self.active_torso_frame.z_order = 5
        self.active_dead_frame.z_order = 5

        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/sprites/heisters/chief/debug.png")

        self.destination = []
        self.speed = 10

        self.state = 0

        self.clock = 0

    def update_position(self, player_x, player_y, data, game_time: pyasge.GameTime,bullets, Bullets, audio_system, sounds):
        if self.state == 0 and player_y > self.pos_y - 400 and player_y < self.pos_y + 400 and player_x > self.pos_x - 400 and player_x < self.pos_x + 400:
            self.move(pathfind(pyasge.Point2D(self.pos_x, self.pos_y), pyasge.Point2D(player_x, player_y), data))
            r_offset = random.randint(6, 10)
            if len(self.destination) > r_offset:
                self.tile_move()
            if len(self.destination) < r_offset + 1:
                self.state = 1
        if self.state == 1:
            self.destination = []
            # Find player's current tile
            tile_size = data.game_map.tile_size
            player_tile_x = int(player_x - self.pos_x)
            player_tile_y = int(player_y - self.pos_y)

            # Calculate angle to player's current tile

            dx = player_tile_x
            dy = player_tile_y
            self.angle = math.atan2(dy, dx)
            r_delay = random.randint (1,4)
            if self.clock > r_delay:
                self.state = 0
                self.clock = 0
                bullet = Bullets(self.sprite.midpoint, self.angle, self.pos_x,
                                 self.pos_y, player_x, player_y, self.active_torso_frame.width)
                bullet.shot_by = "enemy"
                channel = audio_system.play_sound(sounds["shoot"])
                bullets.append(bullet)
            else:
                self.clock += 1 * game_time.fixed_timestep


    def move(self, path: list[pyasge.Point2D]) -> None:
        self.destination = path
    def tile_move(self):
        self.position = pyasge.Point2D(self.pos_x, self.pos_y)
        v1 = self.position
        v2 = self.destination[0]

        dx = v2.x - v1.x
        dy = v2.y - v1.y
        self.angle = math.atan2(dy, dx)
        if dx > 0:
            self.pos_x += self.speed
            if self.pos_x > v2.x:
                self.pos_x = v2.x

        elif dx < 0:
            self.pos_x -= self.speed
            if self.pos_x < v2.x:
                self.pos_x = v2.x
        if dy > 0:
            self.pos_y += self.speed
            if self.pos_y > v2.y:
                self.pos_y = v2.y
        elif dy < 0:
            self.pos_y -= self.speed
            if self.pos_y < v2.y:
                self.pos_y = v2.y
        if dx == 0 and dy == 0:
            self.destination = []


    def update_animation(self):
        if self.moving:

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

        torso_half_width = self.active_torso_frame.width / 2
        torso_half_height = self.active_torso_frame.height / 2

        self.active_torso_frame.scale = 3
        self.active_torso_frame.x = self.pos_x - torso_half_width
        self.active_torso_frame.y = self.pos_y - torso_half_height
        self.active_torso_frame.rotation = self.angle

        leg_half_width = self.active_leg_frame.width / 2
        leg_half_height = self.active_leg_frame.height / 2

        self.active_leg_frame.scale = 3
        self.active_leg_frame.x = self.pos_x - leg_half_width
        self.active_leg_frame.y = self.pos_y - leg_half_height
        self.active_leg_frame.rotation = self.angle

        self.active_torso_frame.z_order = 5
        self.active_dead_frame.z_order = 5

    def update(self, player_x, player_y, data, game_time: pyasge.GameTime, bullets, Bullets, audio_system, sounds):
        self.sprite.scale = 3
        self.sprite.x = self.pos_x - self.active_torso_frame.width / 2
        self.sprite.y = self.pos_y
        self.sprite.rotation = self.angle
        if self.alive:
            self.update_position(player_x, player_y, data, game_time, bullets, Bullets, audio_system, sounds)
            self.update_animation()
        if self.health <= 0 and self.alive:
            self.alive = False
            random_death = random.randint(0, 3)
            if random_death == 0:
                self.active_dead_frame = self.dead_frames[0]
            elif random_death == 1:
                self.active_dead_frame = self.dead_frames[1]
            elif random_death == 2:
                self.active_dead_frame = self.dead_frames[2]
            else:
                self.active_dead_frame = self.dead_frames[3]
            self.active_dead_frame.scale = 2.5
            self.active_dead_frame.x = self.active_torso_frame.x
            self.active_dead_frame.y = self.active_torso_frame.y

    def render(self, renderer: pyasge.Renderer):
        if self.alive:
            renderer.render(self.active_torso_frame)
        else:
            renderer.render(self.active_dead_frame)

class Enemy_Melee:
    def __init__(self):
        self.alive_spritesheet = Spritesheet("/data/sprites/SWAT/swatGruntSpriteSheet.png")

        self.torso_walk_frames = [
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_0.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_1.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_2.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_3.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_4.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_5.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_6.png'),
            self.alive_spritesheet.parseSprite('swatGruntM16Walk_7.png')
        ]

        self.leg_frames = [
            self.alive_spritesheet.parseSprite('swatGruntLegs_00.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_01.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_02.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_03.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_04.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_05.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_06.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_07.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_08.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_09.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_10.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_11.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_12.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_13.png'),
            self.alive_spritesheet.parseSprite('swatGruntLegs_14.png')
        ]

        self.dead_spritesheet = Spritesheet("/data/sprites/SWAT/swatGruntDeadSpriteSheet.png")
        self.dead_frames = [
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_1.png'),
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_2.png'),
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_3.png'),
            self.dead_spritesheet.parseSprite('swatGruntDeadSpriteSheet_4.png')
        ]
        self.active_dead_frame = self.dead_frames[0]

        self.active_torso_frame = self.torso_walk_frames[0]


        self.active_leg_frame = self.leg_frames[0]
        self.active_leg_frame.scale = 3

        self.pos_x = 0
        self.pos_y = 0
        self.angle = 0

        # sprite animation variables
        self.torso_animation_frame = 0
        self.torso_animation_frames = self.torso_walk_frames

        self.leg_animation_frame = 0
        self.leg_animation_frames = self.leg_frames

        self.animation_speed = 0.2  # adjust as needed
        self.moving = False

        self.health = 1
        self.alive = True

        self.active_torso_frame.z_order = 5
        self.active_dead_frame.z_order = 5

        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/sprites/heisters/chief/debug.png")

        self.destination = []
        self.speed = 10

        self.state = 0

        self.clock = 0

    def update_position(self, player_x, player_y, data, game_time: pyasge.GameTime,bullets, Bullets, audio_system, sounds):
        if self.state == 0 and player_y > self.pos_y - 400 and player_y < self.pos_y + 400 and player_x > self.pos_x - 400 and player_x < self.pos_x + 400:
            self.move(pathfind(pyasge.Point2D(self.pos_x, self.pos_y), pyasge.Point2D(player_x, player_y), data))
            r_offset = random.randint(6, 10)
            if len(self.destination) > r_offset:
                self.tile_move()
            if len(self.destination) < r_offset + 1:
                self.state = 1
        if self.state == 1:
            self.destination = []
            # Find player's current tile
            tile_size = data.game_map.tile_size
            player_tile_x = int(player_x - self.pos_x)
            player_tile_y = int(player_y - self.pos_y)

            # Calculate angle to player's current tile

            dx = player_tile_x
            dy = player_tile_y
            self.angle = math.atan2(dy, dx)
            r_delay = random.randint (1,4)
            if self.clock > r_delay:
                self.state = 0
                self.clock = 0
                bullet = Bullets(self.sprite.midpoint, self.angle, self.pos_x,
                                 self.pos_y, player_x, player_y, self.active_torso_frame.width)
                bullet.shot_by = "enemy"
                channel = audio_system.play_sound(sounds["shoot"])
                bullets.append(bullet)
            else:
                self.clock += 1 * game_time.fixed_timestep


    def move(self, path: list[pyasge.Point2D]) -> None:
        self.destination = path
    def tile_move(self):
        self.position = pyasge.Point2D(self.pos_x, self.pos_y)
        v1 = self.position
        v2 = self.destination[0]

        dx = v2.x - v1.x
        dy = v2.y - v1.y
        self.angle = math.atan2(dy, dx)
        if dx > 0:
            self.pos_x += self.speed
            if self.pos_x > v2.x:
                self.pos_x = v2.x

        elif dx < 0:
            self.pos_x -= self.speed
            if self.pos_x < v2.x:
                self.pos_x = v2.x
        if dy > 0:
            self.pos_y += self.speed
            if self.pos_y > v2.y:
                self.pos_y = v2.y
        elif dy < 0:
            self.pos_y -= self.speed
            if self.pos_y < v2.y:
                self.pos_y = v2.y
        if dx == 0 and dy == 0:
            self.destination = []


    def update_animation(self):
        if self.moving:

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

        torso_half_width = self.active_torso_frame.width / 2
        torso_half_height = self.active_torso_frame.height / 2

        self.active_torso_frame.scale = 3
        self.active_torso_frame.x = self.pos_x - torso_half_width
        self.active_torso_frame.y = self.pos_y - torso_half_height
        self.active_torso_frame.rotation = self.angle

        leg_half_width = self.active_leg_frame.width / 2
        leg_half_height = self.active_leg_frame.height / 2

        self.active_leg_frame.scale = 3
        self.active_leg_frame.x = self.pos_x - leg_half_width
        self.active_leg_frame.y = self.pos_y - leg_half_height
        self.active_leg_frame.rotation = self.angle

        self.active_torso_frame.z_order = 5
        self.active_dead_frame.z_order = 5

    def update(self, player_x, player_y, data, game_time: pyasge.GameTime, bullets, Bullets, audio_system, sounds):
        self.sprite.scale = 3
        self.sprite.x = self.pos_x - self.active_torso_frame.width / 2
        self.sprite.y = self.pos_y
        self.sprite.rotation = self.angle
        if self.alive:
            self.update_position(player_x, player_y, data, game_time, bullets, Bullets, audio_system, sounds)
            self.update_animation()
        if self.health <= 0 and self.alive:
            self.alive = False
            random_death = random.randint(0, 3)
            if random_death == 0:
                self.active_dead_frame = self.dead_frames[0]
            elif random_death == 1:
                self.active_dead_frame = self.dead_frames[1]
            elif random_death == 2:
                self.active_dead_frame = self.dead_frames[2]
            else:
                self.active_dead_frame = self.dead_frames[3]
            self.active_dead_frame.scale = 2.5
            self.active_dead_frame.x = self.active_torso_frame.x
            self.active_dead_frame.y = self.active_torso_frame.y

    def render(self, renderer: pyasge.Renderer):
        if self.alive:
            renderer.render(self.active_torso_frame)
        else:
            renderer.render(self.active_dead_frame)



