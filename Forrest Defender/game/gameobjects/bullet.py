import math
import pyasge

from game.gameobjects.gamemap import GameMap


class Bullet:
    def __init__(self, spawn: pyasge.Point2D, angle, spawn_x, spawn_y, dir_x, dir_y, player_width) -> None:
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("data/sprites/bullet/bullet.png")
        self.sprite.scale = 3
        self.sprite.z_order = 1
        self.width = self.sprite.width
        self.height = self.sprite.height
        self.angle = angle
        self.shot_by = None

        # Calculate the offset based on the player's rotation
        offset_x = (player_width / 2 + 10)* math.cos(angle)
        offset_y = (player_width / 2 + 10) * math.sin(angle)

        self.sprite.x = spawn.x + offset_x
        self.sprite.y = spawn.y + offset_y
        self.speed = 900
        self.sprite.rotation = angle

        # calculate direction vector
        self.direction_x = dir_x - spawn_x
        self.direction_y = dir_y - spawn_y
        length = math.sqrt(self.direction_x ** 2 + self.direction_y ** 2)
        self.direction_x /= length
        self.direction_y /= length

    def update(self, game_time: pyasge.GameTime, game_map: GameMap) -> None:
        # move the bullet by the direction vector multiplied by speed
        self.sprite.x += self.direction_x * self.speed * game_time.frame_time
        self.sprite.y += self.direction_y * self.speed * game_time.frame_time

    def render(self, renderer: pyasge.Renderer) -> None:
        renderer.render(self.sprite)
