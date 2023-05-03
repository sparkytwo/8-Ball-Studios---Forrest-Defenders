import pyasge

from game.gamestate import GameState
from game.gamestate import GameStateID
from game.gamedata import GameData


class GameOver(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.menu_text = None
        self.id = GameStateID.GAME_OVER
        self.transition = False

        # Background
        self.background = pyasge.Sprite()
        self.title_sprite = pyasge.Sprite()
        self.initBackground()

    def initBackground(self) -> bool:
        if self.background.loadTexture("/data/textures/gamemenu/gameover.png"):
            self.background.z_order = 100
            self.background.scale = 1
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
            return GameStateID.START_MENU

        return GameStateID.GAME_OVER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.background)
