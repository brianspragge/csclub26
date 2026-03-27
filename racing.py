# title: Racing!
# authors: Brian Spragge, (Add your name here)
# desc: A Pyxel racing game
# site: https://github.com/brianspragge/csclub26
# license: MIT (If that is ok with ya'll)
# version: 0.1

import pyxel
import math

SCREEN_W = 256
SCREEN_H = 256
SCORE_H  = pyxel.FONT_HEIGHT
PI       = math.pi

class App:
    def __init__(self):
        pyxel.init(
            SCREEN_W,
            SCREEN_H,
            title="Racing!",
            fps=30,
            display_scale=12,
            capture_scale=6,
        )
        pyxel.load("resources.pyxres")
        self.init_sound()
        self.car = {"pos": {"x":  SCREEN_W / 2,
                            "y":  SCREEN_H / 2},
                    "angle":      0.0,           # Radians
                    "speed":      0.0,
                    "max_speed":  5,
                    "turn_speed": 0.07}
        self.reset()
        pyxel.run(self.update, self.draw)

    def init_sound(self):
        """Music taken from Pyxel's snake game example."""
        pyxel.sounds[0].set(
            notes="c3e3g3c4c4", tones="s", volumes="4",
            effects="nnnnf", speed=7
        )
        pyxel.sounds[1].set(
            notes="f3 b2 f2 b1  f1 f1 f1 f1",
            tones="p",
            volumes="44444321",
            effects="nnnnnnnf",
            speed=9,
        )

        melody1 = (
            "c3 c3 c3 d3 e3 r e3 r"
            "rrrrrrrr"
            "e3 e3 e3 f3 d3 r c3 r"
            "rrrrrrrr"
            "c3 c3 c3 d3 e3 r e3 r"
            "rrrrrrrr"
            "b2 b2 b2 f3 d3 r c3 r"
            "rrrrrrrr"
        )
        melody2 = (
            "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
            "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
            "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
            "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
            "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
            "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
            "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
            "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
        )
        pyxel.sounds[2].set(
            notes=melody1 * 2 + melody2 * 2,
            tones="s",
            volumes="3",
            effects="nnnsffff",
            speed=20,
        )

        harmony1 = (
            "a1 a1 a1 b1  f1 f1 c2 c2  c2 c2 c2 c2  g1 g1 b1 b1" * 3
            + "f1 f1 f1 f1 f1 f1 f1 f1 g1 g1 g1 g1 g1 g1 g1 g1"
        )
        harmony2 = (
            ("f1" * 8 + "g1" * 8 + "a1" * 8 + "c2" * 7 + "d2") * 3
            + "f1" * 16
            + "g1" * 16
        )
        pyxel.sounds[3].set(
            notes=harmony1 * 2 + harmony2 * 2,
            tones="t",
            volumes="5",
            effects="f",
            speed=20,
        )
        pyxel.sounds[4].set(
            notes="f0 r a4 r  f0 f0 a4 r  f0 r a4 r  f0 f0 a4 f0",
            tones="n",
            volumes="6622 6622 6622 6426",
            effects="f",
            speed=20,
        )

        pyxel.musics[0].set([], [2], [3], [4])

    def reset(self):
        """Reset game state and objects on game restart."""
        self.death           = False
        self.car["pos"]["x"] = SCREEN_W / 2
        self.car["pos"]["y"] = SCREEN_H / 2
        self.car["angle"]    = 0.0
        self.car["speed"]    = 0.0
        pyxel.playm(0, loop=True)

    def update(self):
        """Update game state each frame."""
        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Reset game
        if pyxel.btnp(pyxel.KEY_R) \
        or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.reset()

        if not self.death:
            self.update_car()
            self.check_death()

    def update_car(self):
        """Calculate new position of car based on key press."""
        # Gas and brake
        if pyxel.btn(pyxel.KEY_UP) \
        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.car["speed"] = min(self.car["speed"] + 0.1, 
                                    self.car["max_speed"])
        elif pyxel.btn(pyxel.KEY_DOWN) \
        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.car["speed"] = max(self.car["speed"] - 0.1,
                                    -self.car["max_speed"]/2)
        else:
            self.car["speed"] *= 0.95  # Gradually slow down

        # Turning left and right
        if pyxel.btn(pyxel.KEY_LEFT) \
        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.car["angle"] -= self.car["turn_speed"]

        if pyxel.btn(pyxel.KEY_RIGHT) \
        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.car["angle"] += self.car["turn_speed"]

        new_x = math.cos(self.car["angle"]) * self.car["speed"]
        new_y = math.sin(self.car["angle"]) * self.car["speed"]
        self.car["pos"]["x"] += new_x
        self.car["pos"]["y"] += new_y

        # Reset angle after one complete rotation
        self.car["angle"] = self.car["angle"] % (2 * PI)

    def blt_car(self):
        """Determine which sprite to blit based on axis snapping."""
        x     = int(self.car["pos"]["x"])
        y     = int(self.car["pos"]["y"])
        angle = self.car["angle"]

        # Snap sprite on nearest 90 degrees based on car angle
        direction = round((angle % (2 * PI)) / (PI / 2)) % 4

        # RIGHT
        if direction == 0:
            pyxel.blt(x, y, 0, 8, 0, 8, 8, 0)
        # DOWN
        elif direction == 1:
            pyxel.blt(x, y, 0, 0, 0, 8, -8, 0)
        # LEFT
        elif direction == 2:
            pyxel.blt(x, y, 0, 8, 0, -8, 8, 0)
        # UP
        elif direction == 3:
            pyxel.blt(x, y, 0, 0, 0, 8, 8, 0)
        # DEBUG
        print(f"Direction: {direction}", '\n'
              f"Angle:     {angle:.2f}")

    def check_death(self):
        if self.car["pos"]["x"] <  0 \
        or self.car["pos"]["y"] <  0 \
        or self.car["pos"]["x"] >= SCREEN_W \
        or self.car["pos"]["y"] >= SCREEN_H:
            self.death = True
            pyxel.stop()
            pyxel.play(0, 1)

    def draw(self):
        """Blit entities onto screen each frame."""
        if self.death:
            self.draw_death()
            return

        pyxel.cls(3)

        # Draw triangle
        # x1 = self.car["pos"]["x"] + math.cos(self.car["angle"]) * 8
        # y1 = self.car["pos"]["y"] + math.sin(self.car["angle"]) * 8
        # x2 = self.car["pos"]["x"] + math.cos(self.car["angle"] + 2.5) * 5
        # y2 = self.car["pos"]["y"] + math.sin(self.car["angle"] + 2.5) * 5
        # x3 = self.car["pos"]["x"] + math.cos(self.car["angle"] - 2.5) * 5
        # y3 = self.car["pos"]["y"] + math.sin(self.car["angle"] - 2.5) * 5
        # pyxel.tri(x1, y1, x2, y2, x3, y3, 200)

        self.blt_car()

        # Draw speedometer
        pyxel.rect(0, 0, SCREEN_W/6, SCORE_H, 5)
        pyxel.text(1, 1, f"SPEED: {self.car["speed"]:.1f}", 6)

    def draw_death(self):
        """Show death screen."""
        pyxel.cls(8)
        for i, text in enumerate(
            ["GAME OVER", "(Q)UIT", "(R)ESTART"]
        ):
            x = (SCREEN_W - len(text) * pyxel.FONT_WIDTH) // 2
            pyxel.text(x, 5 + (pyxel.FONT_HEIGHT + 2) * i, text, 0)


# Run the program
if __name__ == "__main__":
    App()

