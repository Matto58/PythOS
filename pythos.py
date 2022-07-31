from re import T
from time import sleep
import random
import pygame

console = []
max_len = 50

pygame.init()

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "almost_black": (10, 10, 10),
    "almost_white": (245, 245, 245),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "light_gray": (191, 191, 191),
    "gray": (128, 128, 128),
    "dark_gray": (64, 64, 64)
}
imgs = {
    "logo": {
        "verysmall": {
            "glow": pygame.image.load("data/imgs/logo/logo_small.png"),
            "noglow": pygame.image.load("data/imgs/logo/logo_small_noglow.png")
        },
        "small": {
            "glow": pygame.image.load("data/imgs/logo/logo_small2.png"),
            "noglow": pygame.image.load("data/imgs/logo/logo_small2_noglow.png")
        },
        "medium": {
            "glow": pygame.image.load("data/imgs/logo/logo_medium.png"),
            "noglow": pygame.image.load("data/imgs/logo/logo_medium_noglow.png")
        },
        "large": {
            "glow": pygame.image.load("data/imgs/logo/logo_large.png"),
            "noglow": pygame.image.load("data/imgs/logo/logo_large_noglow.png")
        },
        "largest": {
            "glow": pygame.image.load("data/imgs/logo/logo.png"),
            "noglow": pygame.image.load("data/imgs/logo/logo_noglow.png")
        }
    },
    "extra": {
        "loading": pygame.image.load("data/imgs/extra/load.gif")
    },
    "ui": {
        "menubar": pygame.image.load("data/imgs/ui/menubar.png"),
        "btn": {
            "home": pygame.image.load("data/imgs/ui/home-mini.png"),
            "search": pygame.image.load("data/imgs/ui/search-mini.png")
        },
        "window": {
            "light": pygame.image.load("data/imgs/ui/window-light.png"),
            "dark": pygame.image.load("data/imgs/ui/window-dark.png")
        }
    }
}
fonts = {
    "mono": pygame.font.Font("data/fonts/Source_Code_Pro/normal/SourceCodePro-Regular.ttf", 16),
    "sans": pygame.font.Font("data/fonts/Noto_Sans/normal/NotoSans-Regular.ttf", 16),
}
bgs = {
    "red2blue": pygame.image.load("data/imgs/bg/red2blue.png"),
    "load": pygame.image.load("data/imgs/bg/load.png"),
    "load25": pygame.image.load("data/imgs/bg/load25.png"),
    "load50": pygame.image.load("data/imgs/bg/load50.png"),
    "colors": pygame.image.load("data/imgs/bg/colors.png")
}
sfx = {
    "boot": pygame.mixer.Sound("data/sfx/boot.wav"),
}
true_bgs = [
    bgs["red2blue"],
    bgs["load25"],
    bgs["colors"]
]

def PythOS_print(text: str):
    t = text.split("\n")
    for ln in t:
        console.append(ln)
        if len(console) > max_len:
            console.pop(0)

class Window:
    def __init__(self, x: int, y: int, title: str, dark: bool = False):
        self.x = x
        self.y = y
        self.title = title
        self.dark = dark
    
    def draw(self, screen: pygame.Surface):
        if self.dark:
            screen.blit(imgs["ui"]["window"]["dark"], (self.x, self.y))
        else:
            screen.blit(imgs["ui"]["window"]["light"], (self.x, self.y))

        t = self.title

        if len(t) > max_len:
            t = t[:(max_len-3)] + "..."

        text = fonts["sans"].render(t, True, colors["white"])
        screen.blit(text, (self.x + 6, self.y + 4))


def Main():
    scr_size = (1280, 720)
    screen = pygame.display.set_mode(scr_size)
    pygame.display.set_caption("PythOS v0.0.1 - booting environment")

    clock = pygame.time.Clock()
    time = 0
    percentage = 0

    HIDE_CONSOLE = False
    CONSOLE_IN_DESKTOP = False
    background = true_bgs[0]

    console = [
        "PythOS v0.0.1",
        "",
        "",
        ""
    ]

    logo_img = imgs["logo"]["medium"]["glow"]
    logo_pos = (
        (scr_size[0] - logo_img.get_width()) // 2,
        (scr_size[1] - logo_img.get_height()) // 2
    )
    bg_img = true_bgs[1]
    first_boot = True

    with open("data/isfirstboot", "r") as f:
        first_boot = f.read() == "1"

    windows = []
    first_boot_window = Window(
        # centered window
        (scr_size[0] - 800) // 2,
        (scr_size[1] - 600 + 72) // 2,
        "Welcome to PythOS v0.0.1!",
        True
    )

    if first_boot:
        windows.append(first_boot_window)


    while True:
        screen.fill(colors["black"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        console_text = []
        console_text_shadow = []
        console_color = colors["white"]
        console_color_shadow = colors["dark_gray"]
        shadow_distance = (1, 1)

        pressed_last_frame = False

        if percentage != 200:
            # Console environment
            console[3] = str(time) + " ticks from boot start"
            screen.blit(bg_img, (0, 0))
            screen.blit(logo_img, logo_pos)
            if time % random.randint(2, 4) == 0 and percentage < 100:
                percentage += 1
                console[1] = "Loading " + str(percentage) + "%..."
            if percentage == 100:
                console[1] = "Loading 100%... finished."
                console[2] = "Starting desktop..."
                percentage = 200
                sleep(random.randint(2000, 5000) / 1000)
                pygame.mixer.Sound.play(sfx["boot"])

            if not HIDE_CONSOLE:
                for i in range(len(console)):
                    console_text.append(fonts["mono"].render(console[i], True, console_color))
                    console_text_shadow.append(fonts["mono"].render(console[i], True, console_color_shadow))

                    if shadow_distance != 0:
                        screen.blit(console_text_shadow[i], (4 + shadow_distance[0], 5 + shadow_distance[1] + i * 14))
                        
                    screen.blit(console_text[i], (4, 5 + i * 14))

        else:
            mouse = pygame.mouse.get_pos()
            press = pygame.mouse.get_pressed()
            previous_press = press[0]

            pygame.display.set_caption("PythOS v0.0.1 - desktop environment")
            with open("data/isfirstboot", "w") as f:
                f.write("0")

            screen.blit(background, (0, 0))

            for window in windows:
                window.draw(screen)
            
            b = 0
            btns = imgs["ui"]["btn"]
            screen.blit(imgs["ui"]["menubar"], (0, 0))
            for btn in btns:
                screen.blit(btns[btn], ((4 + btns[btn].get_width()) * b + 4, 4))
                # if the buttons are clicked,
                # print (button name) has been pressed
                # the buttons are: home, search
                if mouse[0] > (4 + btns[btn].get_width()) * b + 4 and mouse[0] < (4 + btns[btn].get_width()) * (b + 1) + 4:
                    if mouse[1] > 4 and mouse[1] < 4 + btns[btn].get_height():
                        if press[0]:
                            if btn == "home":
                                print("home has been pressed")
                            elif btn == "search":
                                print("search has been pressed")
                b += 1
                
            console_text = []
            console_text_shadow = []
            #console_color = colors["green"]
            console = [
                str(time) + " ticks from boot start",
                "You're in the desktop environment.",
            ]

            if CONSOLE_IN_DESKTOP and not HIDE_CONSOLE:
                for i in range(len(console)):
                    console_text.append(fonts["mono"].render(console[i], True, console_color))
                    console_text_shadow.append(fonts["mono"].render(console[i], True, console_color_shadow))

                    if shadow_distance != 0:
                        screen.blit(console_text_shadow[i], (4 + shadow_distance[0], 5 + shadow_distance[1] + i * 14))
                        
                    screen.blit(console_text[i], (4, 5 + i * 14))



        pygame.display.update()
        time += 1
        clock.tick(60)

Main()