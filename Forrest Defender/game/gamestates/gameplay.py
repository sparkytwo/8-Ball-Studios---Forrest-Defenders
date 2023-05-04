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

        self.enemy_count = 17
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
        self.camera.zoom = 1.5
        self.camera.lookAt(self.heister.sprite.midpoint)

        self.sounds = {"shoot": self.data.audio_system.create_sound("./data/audio/gunshot.wav"),
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
        self.ui_m16_spritesheet = Spritesheet("/data/sprites/UI/M16/ui_m16.png")
        self.ui_m16_frames = [
            self.ui_m16_spritesheet.parseSprite('M16_00.png'),
            self.ui_m16_spritesheet.parseSprite('M16_01.png'),
            self.ui_m16_spritesheet.parseSprite('M16_02.png'),
            self.ui_m16_spritesheet.parseSprite('M16_03.png'),
            self.ui_m16_spritesheet.parseSprite('M16_04.png'),
            self.ui_m16_spritesheet.parseSprite('M16_05.png'),
            self.ui_m16_spritesheet.parseSprite('M16_06.png'),
            self.ui_m16_spritesheet.parseSprite('M16_07.png'),
            self.ui_m16_spritesheet.parseSprite('M16_08.png'),
            self.ui_m16_spritesheet.parseSprite('M16_09.png'),
            self.ui_m16_spritesheet.parseSprite('M16_10.png'),
            self.ui_m16_spritesheet.parseSprite('M16_11.png'),
            self.ui_m16_spritesheet.parseSprite('M16_12.png'),
            self.ui_m16_spritesheet.parseSprite('M16_13.png'),
            self.ui_m16_spritesheet.parseSprite('M16_14.png'),
            self.ui_m16_spritesheet.parseSprite('M16_15.png'),
            self.ui_m16_spritesheet.parseSprite('M16_16.png'),
            self.ui_m16_spritesheet.parseSprite('M16_17.png'),
            self.ui_m16_spritesheet.parseSprite('M16_18.png'),
            self.ui_m16_spritesheet.parseSprite('M16_19.png'),
            self.ui_m16_spritesheet.parseSprite('M16_20.png'),
            self.ui_m16_spritesheet.parseSprite('M16_21.png')
        ]
        self.ui_active_weapon = self.ui_m16_frames[21]
        self.ui_active_weapon.scale = 5
        self.ui_active_weapon.x = 20
        self.ui_active_weapon.y = 10
        self.total_ammo = self.heister.ammo + self.heister.ammo_in_magazine
        self.ui_ammo_count = pyasge.Text(self.data.renderer.getDefaultFont(), str(self.total_ammo), 100, 100)
        self.ui_ammo_count.z_order = 100
        self.ui_ammo_count.x = 10
        self.ui_ammo_count.y = 155
        self.ui_ammo_count.colour = pyasge.COLOURS.WHITE
        self.ui_ammo_count.scale = 1

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
        self.ui_active_health.scale = 3
        self.ui_active_health.x = 1550
        self.ui_active_health.y = 40

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

        self.update_camera()
        self.update_bullets(game_time)
        self.heister.update(self.key_states, self.bullets, Bullet, self.data.cursor, self.data.game_map, game_time,
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

        if self.heister.health < 1 or self.heister.win == True:
            self.transition = True
        if self.transition == True and not self.heister.win:
            return GameStateID.GAME_OVER
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

        self.data.renderer.render(self.data.cursor)

    def render_ui(self) -> None:
        vp = self.data.renderer.resolution_info.viewport
        self.data.renderer.setProjectionMatrix(0, 0, vp.w, vp.h)

        self.ui_active_weapon = self.ui_m16_frames[self.heister.ammo_in_magazine]
        self.ui_active_weapon.scale = 5
        self.ui_active_weapon.x = 20
        self.ui_active_weapon.y = 10
        self.total_ammo = self.heister.ammo + self.heister.ammo_in_magazine
        self.ui_ammo_count = pyasge.Text(self.data.renderer.getDefaultFont(), str(self.total_ammo).zfill(3), 100, 100)
        self.ui_ammo_count.z_order = 100
        self.ui_ammo_count.x = 10
        self.ui_ammo_count.y = 155
        if self.total_ammo <= 20:
            self.ui_ammo_count.colour = pyasge.COLOURS.RED
        elif self.total_ammo <= 40 and self.total_ammo > 20:
            self.ui_ammo_count.colour = pyasge.COLOURS.YELLOW
        else:
            self.ui_ammo_count.colour = pyasge.COLOURS.WHITE
        self.ui_ammo_count.scale = 1

        self.ui_active_health = self.ui_health_frames[self.heister.health]
        self.ui_active_health.scale = 3
        self.ui_active_health.x = 1550
        self.ui_active_health.y = 40


        self.data.renderer.render(self.ui_active_health)
