import random

import pyasge
import math
from game.gamedata import GameData
from game.gameobjects.heister import Heister
from game.gameobjects.enemy import *
from game.gamestate import GameState
from game.spritesheet import Spritesheet
from game.gameobjects.bullet import Bullet
from game.gamestate import GameStateID


class GamePlay(GameState):

    def __init__(self, data: GameData):

        super().__init__(data)

        self.transition = False

        self.ui_health_frames = None
        self.total_ammo = None
        self.ui_active_weapon = None
        self.ui_ammo_count = None
        self.ui_m16_frames = None
        self.ui_m16_spritesheet = None
        self.heister = Heister()
        self.init_ui()

        self.key_states = set()
        self.init_cursor()
        self.bullets = []
        self.enemies = []

        self.enemy_count = 9
        self.spawn_points = len(self.data.game_map.spawns)
        rands = random.sample(self.data.game_map.spawns, self.spawn_points)
        for i in range(0, self.enemy_count):
            ran_enemy =  random.randint(1,2)
            if ran_enemy == 1:
                enemy = Enemy_Melee()
            if ran_enemy == 2:
                enemy = Enemy_Ranged()

            self.enemies.append(enemy)
            x, y = rands.pop()
            self.enemies[i].pos_x = x * 2
            self.enemies[i].pos_y = y * 2

        map_mid = [
            self.data.game_map.width * self.data.game_map.tile_size[0] * 0.5,
            self.data.game_map.height * self.data.game_map.tile_size[1] * 0.5
        ]

        self.camera = pyasge.Camera(map_mid, self.data.game_resolution[0], self.data.game_resolution[1])
        self.camera.zoom = 1.3
        self.camera.zoom = 1.2
        self.camera.lookAt(self.heister.sprite.midpoint)

        self.sounds = {"shoot": self.data.audio_system.create_sound("./data/audio/gunshot.mp3"),
                       "shell": self.data.audio_system.create_sound("./data/audio/shells.mp3")}

    def init_cursor(self):
        """Initialises the mouse cursor and hides the OS cursor."""
        self.data.cursor.loadTexture("/data/sprites/crosshair/crosshair.png")
        self.data.cursor.width = 32
        self.data.cursor.height = 32
        # self.data.cursor.src_rect = [0, 0, 128, 128]
        self.data.cursor.scale = 1
        self.data.cursor.z_order = 127
        # self.data.cursor.opacity = 100
        # self.data.cursor.colour = pyasge.COLOURS.HOTPINK
        self.data.cursor.setMagFilter(pyasge.MagFilter.NEAREST)
        self.data.inputs.setCursorMode(pyasge.CursorMode.HIDDEN)

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        cursor_x = event.x - self.data.cursor.width * 0.5
        cursor_y = event.y - self.data.cursor.height * 0.5
        heister_x = self.heister.pos_x + self.heister.active_torso_frame.width * 0.5
        heister_y = self.heister.pos_y + self.heister.active_torso_frame.height * 0.5

        # calculate distance between cursor and heister
        distance = math.sqrt((cursor_x - heister_x) ** 2 + (cursor_y - heister_y) ** 2)

        # clamp cursor position within the circle
        if distance > 300:
            angle = math.atan2(cursor_y - heister_y, cursor_x - heister_x)
            cursor_x = heister_x + 300 * math.cos(angle) - self.data.cursor.width * 0.5
            cursor_y = heister_y + 300 * math.sin(angle) - self.data.cursor.height * 0.5

        self.data.cursor.x = cursor_x
        self.data.cursor.y = cursor_y

    def init_ui(self):
        self.ui_health_spritesheet = Spritesheet("/data/sprites/UI/health/health_bar.png")
        self.ui_health_frames = [
            self.ui_health_spritesheet.parseSprite('Health0.png'),
            self.ui_health_spritesheet.parseSprite('Health1.png'),
            self.ui_health_spritesheet.parseSprite('Health2.png'),
            self.ui_health_spritesheet.parseSprite('Health3.png'),
            self.ui_health_spritesheet.parseSprite('Health4.png'),
            self.ui_health_spritesheet.parseSprite('Health5.png')
        ]
        self.ui_active_health = self.ui_health_frames[5]
        self.ui_active_health.scale = 0.3
        self.ui_active_health.x = 1600
        self.ui_active_health.y = 50

        self.ui_active_health.z_order = 100

        self.ui_joystick_spritesheet = Spritesheet("/data/sprites/UI/joystick_spritesheet.png")
        self.ui_joystick_frames = [
            self.ui_joystick_spritesheet.parseSprite('joystick_center.png'),
            self.ui_joystick_spritesheet.parseSprite('joystick_left.png'),
            self.ui_joystick_spritesheet.parseSprite('joystick_right.png'),
            self.ui_joystick_spritesheet.parseSprite('joystick_up.png'),
            self.ui_joystick_spritesheet.parseSprite('joystick_down.png')
        ]
        self.ui_active_joystick = self.ui_joystick_frames[0]
        self.ui_active_joystick.scale = 1.5
        self.ui_active_joystick.x = 65
        self.ui_active_joystick.y = 800

        self.ui_shoot_spritesheet = Spritesheet("/data/sprites/UI/shoot_spritesheet.png")
        self.ui_shoot_frames = [
            self.ui_shoot_spritesheet.parseSprite('shoot_up.png'),
            self.ui_shoot_spritesheet.parseSprite('shoot_down.png')
        ]
        self.ui_active_shoot = self.ui_shoot_frames[0]
        self.ui_active_shoot.scale = 1.5
        self.ui_active_shoot.x = 380
        self.ui_active_shoot.y = 850





    def click_handler(self, event: pyasge.ClickEvent) -> None:
        self.heister.click_handler(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:
            self.key_states.add(event.key)
        elif event.action == pyasge.KEYS.KEY_RELEASED:
            self.key_states.discard(event.key)

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if len(self.enemies) == 0:
            rands = random.sample(self.data.game_map.spawns, self.enemy_count)
            for i in range(0, self.enemy_count):
                ran_enemy = random.randint(1,2)
                if ran_enemy == 1:
                    enemy = Enemy_Melee()
                elif ran_enemy == 2:
                    enemy = Enemy_Ranged()
                self.enemies.append(enemy)
                x, y = rands.pop()
                self.enemies[i].pos_x = x * 2
                self.enemies[i].pos_y = y * 2
        cdx = 1000
        cdy = 1000
        edx = 0
        edy = 0
        dx = 0
        dy = 0
        for i in range(0, len(self.enemies)):
            if self.enemies[i].pos_x > self.heister.pos_x - 350 and self.enemies[i].pos_x < self.heister.pos_x + 350 and self.enemies[i].pos_y > self.heister.pos_y - 350 and self.enemies[i].pos_y < self.heister.pos_y + 350:
                print("found")
                if self.enemies[i].alive:
                    self.heister.found = True
                    dx = self.enemies[i].pos_x
                    dy = self.enemies[i].pos_y
                    edx = self.enemies[i].pos_x
                    edy = self.enemies[i].pos_y
                else:
                    self.heister.found = False
            if dx < cdx:
                cdx = dx
            if dy < cdy:
                cdy = dy
        dx = dx - self.heister.pos_x
        dy = dy - self.heister.pos_y
        self.heister.angle = math.atan2(dy, dx)
        self.heister.target_x = edx
        self.heister.target_y = edy


        self.update_camera()
        self.update_bullets(game_time)
        self.heister.update(self.key_states, self.bullets, Bullet, self.data.game_map, game_time,
                            self.data.audio_system, self.sounds)
        c_health = self.heister.health
        for enemy in self.enemies:
            if self.heister.i_clock > 3:
                self.heister.health = enemy.update(self.heister.pos_x, self.heister.pos_y, self.data, game_time, self.bullets, Bullet, self.data.audio_system, self.sounds, self.heister.health)
                if self.heister.health < c_health:
                    self.heister.i_clock = 0
            else:
                enemy.update(self.heister.pos_x, self.heister.pos_y, self.data, game_time, self.bullets, Bullet,
                             self.data.audio_system, self.sounds, self.heister.health)

        self.render_ui()

        if len(self.enemies) < 1:
            quit()
        if self.transition == True and self.heister.win:
            return GameStateID.GAME_WIN

    def update_bullets(self, game_time):
        bullets_to_remove = []
        enemies_to_remove = []
        for bullet in self.bullets:
            tile_size = self.data.game_map.tile_size
            bullet_tile_x = int(bullet.sprite.x / tile_size[0])
            bullet_tile_y = int(bullet.sprite.y / tile_size[1])
            for enemy in self.enemies:

                if enemy.alive:
                    # Check for collision with enemy
                    bullet_pos = (bullet.sprite.x, bullet.sprite.y)
                    enemy_pos = (enemy.pos_x, enemy.pos_y)
                    distance = math.sqrt((bullet_pos[0] - enemy_pos[0]) ** 2 + (bullet_pos[1] - enemy_pos[1]) ** 2)
                    if distance <= (bullet.width ) + (
                    enemy.active_torso_frame.width) and bullet.shot_by == "heister":
                        # remove bullet and enemy
                        bullets_to_remove.append(bullet)
                        enemy.health -= 1

                elif enemy.alive == False:
                    enemies_to_remove.append(enemy)

                bullet_pos = (bullet.sprite.x, bullet.sprite.y)
                player_pos = (self.heister.pos_x, self.heister.pos_y)
                distance = math.sqrt((bullet_pos[0] - player_pos[0]) ** 2 + (bullet_pos[1] - player_pos[1]) ** 2)
                if distance <= (bullet.width * 0.015) + (
                        self.heister.active_torso_frame.width) and bullet.shot_by == "enemy" and self.heister.i_clock > 1:
                    self.heister.health -= 1
                    self.heister.i_clock = 0

            # Check for collision with walls
            if self.data.game_map.costs[bullet_tile_y][bullet_tile_x - 1] == 0 and \
                    self.data.game_map.costs[bullet_tile_y][
                        bullet_tile_x + 1] == 0 and self.data.game_map.costs[bullet_tile_y - 1][bullet_tile_x] == 0 and \
                    self.data.game_map.costs[bullet_tile_y + 1][bullet_tile_x] == 0:
                bullet.update(game_time, self.data.game_map)
            else:
                bullets_to_remove.append(bullet)

        # Remove bullets that hit walls
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
            else:
                pass
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)

    def update_camera(self):
        self.camera.lookAt(self.heister.sprite.midpoint)

        view = [
            self.data.game_resolution[0] * 0.5 / self.camera.zoom,
            self.data.game_map.width * 32 - self.data.game_resolution[0] * 0.5 / self.camera.zoom,
            self.data.game_resolution[1] * 0.5 / self.camera.zoom,
            self.data.game_map.height * 32 - self.data.game_resolution[1] * 0.5 / self.camera.zoom
        ]
        self.camera.clamp(view)

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setViewport(
            pyasge.Viewport(0, 0, self.data.game_resolution[0], self.data.game_resolution[1]))
        self.data.renderer.setProjectionMatrix(self.camera.view)
        self.data.game_map.render(self.data.renderer, game_time)
        self.data.renderer.render(self.heister.active_leg_frame)
        # self.data.renderer.render(self.heister.sprite)
        self.data.renderer.render(self.heister.active_torso_frame)

        for enemy in self.enemies:
            enemy.render(self.data.renderer)
        for bullet in self.bullets:
            bullet.render(self.data.renderer)

        #self.data.renderer.render(self.data.cursor)

    def render_ui(self) -> None:
        vp = self.data.renderer.resolution_info.viewport
        self.data.renderer.setProjectionMatrix(0, 0, vp.w, vp.h)


        self.ui_active_health = self.ui_health_frames[self.heister.health]
        self.ui_active_health.scale = 0.3
        self.ui_active_health.x = 40
        self.ui_active_health.y = 50
        self.ui_active_health.z_order = 100

        if not self.heister.left and not self.heister.right and not self.heister.up and not self.heister.down:
            self.ui_active_joystick = self.ui_joystick_frames[0]
            self.ui_active_joystick.scale = 1.5
            self.ui_active_joystick.x = 65
            self.ui_active_joystick.y = 800
        if self.heister.left and not self.heister.right and not self.heister.up and not self.heister.down:
            self.ui_active_joystick = self.ui_joystick_frames[1]
            self.ui_active_joystick.scale = 1.5
            self.ui_active_joystick.x = 65
            self.ui_active_joystick.y = 800
        if not self.heister.left and self.heister.right and not self.heister.up and not self.heister.down:
            self.ui_active_joystick = self.ui_joystick_frames[2]
            self.ui_active_joystick.scale = 1.5
            self.ui_active_joystick.x = 65
            self.ui_active_joystick.y = 800
        if not self.heister.left and not self.heister.right and  self.heister.up and not self.heister.down:
            self.ui_active_joystick = self.ui_joystick_frames[3]
            self.ui_active_joystick.scale = 1.5
            self.ui_active_joystick.x = 65
            self.ui_active_joystick.y = 800
        if not self.heister.left and not self.heister.right and not self.heister.up and  self.heister.down:
            self.ui_active_joystick = self.ui_joystick_frames[4]
            self.ui_active_joystick.scale = 1.5
            self.ui_active_joystick.x = 65
            self.ui_active_joystick.y = 800

        if self.heister.firing == False:
            self.ui_active_shoot = self.ui_shoot_frames[0]

            self.ui_active_shoot.scale = 1.5
            self.ui_active_shoot.x = 380
            self.ui_active_shoot.y = 850

        if self.heister.firing == True:
            self.ui_active_shoot = self.ui_shoot_frames[1]

            self.ui_active_shoot.scale = 1.5
            self.ui_active_shoot.x = 380
            self.ui_active_shoot.y = 850


        self.data.renderer.render(self.ui_active_health)
        self.data.renderer.render(self.ui_active_joystick)
        self.data.renderer.render(self.ui_active_shoot)

