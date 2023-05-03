import pygame
import pytmx


class GameMap:
    def __init__(self):
        self.game_map = pytmx.load_pygame("map/map.tmx", pixelalpha=True)
        self.map_width = self.game_map.tilewidth * self.game_map.width
        self.map_height = self.game_map.tileheight * self.game_map.height
        self.offset_x = 0
        self.offset_y = 0
    def render(self, surface):
        for layer in self.game_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.game_map.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.game_map.tilewidth + self.offset_x, y * self.game_map.tileheight + self.offset_y))

    def make_map(self):
        map_surface = pygame.Surface((self.map_width, self.map_height))
        self.render(map_surface)
        return map_surface
