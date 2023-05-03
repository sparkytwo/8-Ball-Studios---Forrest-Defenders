import pyasge
from game.gamedata import GameData
from game.gamestate import GameState
from game.gamestate import GameStateID

class GameMenu(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.menu_text = None
        self.id = GameStateID.START_MENU
        self.transition = False

        # Background
        self.background = pyasge.Sprite()
        self.title_sprite = pyasge.Sprite()
        self.initBackground()
        self.initMenu()


    def initBackground(self) -> bool:
        if self.background.loadTexture("/data/textures/gamemenu/MenuBackground.png"):
            self.background.z_order = 1
            self.background.scale = 1
            return True
        else:
            return False

    def initMenu(self) -> bool:
        if self.title_sprite.loadTexture("/data/textures/gamemenu/Logo.png"):
            self.title_sprite.z_order = 2
            self.title_sprite.scale = 1
            self.title_sprite.x = 150
            self.title_sprite.y = 750
            return True
        else:
            return False

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if event.button == pyasge.MOUSE.MOUSE_BTN1:
            self.transition = True

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.key == pyasge.KEYS.KEY_ENTER:

            self.transition = True

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        pass

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:

        if self.transition:
            return GameStateID.GAMEPLAY

        return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.background)
        self.data.renderer.render(self.title_sprite)

