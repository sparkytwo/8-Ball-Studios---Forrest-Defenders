import pyasge
from game.gamedata import GameData
from game.gameobjects.gamemap import GameMap
from game.gamestates.gamemenu import GameMenu

class MyASGEGame(pyasge.ASGEGame):
    """ main game class """

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.

        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setBaseResolution(580, 1080, pyasge.ResolutionPolicy.MAINTAIN)
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)

        # create game data object for shared data
        self.data = GameData()
        self.data.cursor = pyasge.Sprite()

        self.data.game_map = GameMap(self.renderer, "./data/map/map.tmx")
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_resolution = [580, 1080]


        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.key_handler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_handler)
        self.mousemove_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.move_handler)

        self.current_state = GameMenu(self.data)
        self.init_audio()
        self.init_cursor()

    def init_audio(self)-> None:
        self.data.audio_system.init()
        self.data.bg_audio = self.data.audio_system.create_sound("./data/Audio/level_music.wav")
        #self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_audio)
        #self.data.bg_audio_channel.volume = 0.25


    def init_cursor(self):
        """Initialises the mouse cursor and hides the OS cursor."""
        self.data.cursor.loadTexture("/data/sprites/crosshair/cursor.png")
        self.data.cursor.width = 32
        self.data.cursor.height = 32
        #self.data.cursor.src_rect = [0, 0, 128, 128]
        self.data.cursor.scale = 1
        self.data.cursor.z_order = 127
        # self.data.cursor.opacity = 100
        # self.data.cursor.colour = pyasge.COLOURS.HOTPINK
        self.data.cursor.setMagFilter(pyasge.MagFilter.NEAREST)
        self.inputs.setCursorMode(pyasge.CursorMode.HIDDEN)

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """Handles the mouse movement and delegates to the active state."""
        self.data.cursor.x = event.x
        self.data.cursor.y = event.y
        self.current_state.move_handler(event)

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        """Forwards click events on to the active state."""
        self.current_state.click_handler(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """Forwards Key events on to the active state."""
        self.current_state.key_handler(event)
        if event.key == pyasge.KEYS.KEY_ESCAPE:
            self.signalExit()

    def update(self, game_time: pyasge.GameTime) -> None:
        self.current_state.update(game_time)

    # DO NOT REMOVE, used to update states
    from game.update_gamestate import update

    def render(self, game_time: pyasge.GameTime) -> None:
        self.current_state.render(game_time)
        self.renderer.render(self.data.cursor)

def main():
    settings = pyasge.GameSettings()
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.FULLSCREEN
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()

if __name__ == "__main__":
    main()
