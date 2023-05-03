import pyasge
import json

import config.definitions


class Spritesheet:

    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pyasge.Sprite()
        self.sprite_sheet.loadTexture(file_path=self.filename)
        self.sprite_sheet.scale = 2
        self.sprite_sheet.z_order = 3
        self.sprite_sheet.setMagFilter(pyasge.MagFilter.NEAREST)
        self.meta_data = self.filename.replace('png', 'json')
        self.meta_data = config.definitions.ROOT_DIR + self.meta_data
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def getSprite(self, x, y, w, h):
        sprite = pyasge.Sprite()
        sprite.loadTexture(file_path=self.filename)
        sprite.scale = 2
        sprite.z_order = 3
        sprite.setMagFilter(pyasge.MagFilter.NEAREST)
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = x
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = w
        sprite.width = w
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = y
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_Y] = h
        sprite.height = h
        return sprite

    def parseSprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.getSprite(x, y, w, h)
        return image

