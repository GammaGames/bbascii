from asciimatics.scene import Scene
from asciimatics.effects import Print, Effect
from random import randint, choice
from asciimatics.renderers import DynamicRenderer, StaticRenderer
from datetime import datetime
import math
import yaml
try:
    from tools.style import COLOR
    from tools import time_utils
except Exception:
    from style import COLOR
    import time_utils


def get_grass():
    pass


def get_leaves():
    pass


def get_sky(date=None):
    if date is None:
        date = time_utils.get_timestamp(datetime.now())

    time = time_utils.get_time(date)

    if time_utils.is_sunrise(date):
        time = "sunrise"
    elif time_utils.is_sunset(date):
        time = "sunset"

    top = getattr(COLOR.SKY, f"{time.upper()}_TOP")
    middle = getattr(COLOR.SKY, f"{time.upper()}_MIDDLE")
    bottom = getattr(COLOR.SKY, f"{time.upper()}_BOTTOM")
    return (top, middle, bottom)


class Star():
    def __init__(self, screen, star_choices, color_choices):
        self.screen = screen
        self.star_choices = star_choices
        self.color_choices = color_choices
        self.star_chars = choice(self.star_choices)
        self.color = choice(self.color_choices)
        self.cycle = None
        self.old_char = None
        self.respawn()

    def respawn(self):
        self.cycle = randint(0, len(self.star_chars))
        height, width = self.screen.dimensions
        self.x = randint(0, width - 1)
        self.y = self.screen.start_line + randint(0, height // 1.5)
        self.old_char = "x"

    def update(self):
        if not self.screen.is_visible(self.x, self.y):
            self._respawn()

        self.cycle += 1
        if self.cycle >= len(self.star_chars):
            self.cycle = 0
            self.star_chars = choice(self.star_choices)
            self.color = choice(self.color_choices)

        _, _, _, bg = self.screen.get_from(self.x, self.y)
        new_char = self.star_chars[self.cycle]
        self.screen.print_at(new_char, self.x, self.y, self.color, bg=bg)
        self.old_char = new_char


class Stars(Effect):
    def __init__(self, screen, count, **kwargs):
        with open(f"assets/templates/environment/stars.yaml") as f:
            data = yaml.load(f)
            self.star_choices = data["templates"]
            self.color_choices = data["colors"]

        super(Stars, self).__init__(screen, **kwargs)
        self._max = count
        self.stars = []

    def reset(self):
        self.stars = [Star(self.screen, self.star_choices, self.color_choices) for _ in range(self._max)]

    def _update(self, frame_no):
        for star in self.stars:
            star.update()

    @property
    def stop_frame(self):
        return 0


class Cloud():
    def __init__(self, screen, image):
        self.screen = screen
        self.lines = image.split("\n")
        height, width = self.screen.dimensions
        self.x = randint(len(self.lines[0]) * -1, width - 1)
        self.y = self.screen.start_line + randint(0, height // 3)

    def update(self):
        for offset, line in enumerate(self.lines):
            _, _, _, bg = self.screen.get_from(self.x, self.y + offset)
            self.screen.print_at(line, self.x, self.y + offset, 248, bg=bg)


class Clouds(Effect):
    def __init__(self, screen, coverage, **kwargs):
        with open(f"assets/templates/environment/clouds.yaml") as f:
            data = yaml.load(f)
            self.choices = data["templates"]

        super(Clouds, self).__init__(screen, **kwargs)

        if coverage == "clear":
            self.max = 0
        elif coverage == "light":
            self.max = screen.height // 5
        elif coverage == "moderate":
            self.max = screen.height // 2
        elif coverage == "dense":
            self.max = math.floor(screen.height * 1.7)
        self.stars = []

    def reset(self):
        self.clouds = [Cloud(self.screen, choice(self.choices)) for _ in range(self.max)]

    def _update(self, frame_no):
        for star in self.clouds:
            star.update()

    @property
    def stop_frame(self):
        return 0


class Sky(StaticRenderer):
    def __init__(self, height, width):
        super(Sky, self).__init__()
        self._t = 0
        top, middle, bottom = get_sky()

        image = ""
        for y in range(height):
            if y / height < 0.5:
                image += f"${{0,2,{top}}}{' ' * width}\n"
            elif y / height < 0.8:
                image += f"${{0,2,{middle}}}{' ' * width}\n"
            else:
                image += f"${{0,2,{bottom}}}{' ' * width}\n"

        self._images = [image]


def get_effects(screen):
    effects = []
    effects.append(Print(
        screen,
        Sky(screen.height, screen.width),
        0,
        transparent=False
    ))

    time = time_utils.get_time()
    if time == "night":
        effects.append(Stars(
            screen,
            (screen.width + screen.height) // 6
        ))

    clouds, weather, special = time_utils.get_weather()
    effects.append(Clouds(screen, clouds))

    if weather == "overcast":
        pass

    return effects
