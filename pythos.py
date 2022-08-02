from time import sleep
import random
import pygame
import json

console = []
max_len = 50

fr = 92

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
        "loading": pygame.image.load("data/imgs/extra/load.gif"),
        "load_fr": []
    },
    "ui": {
        "menubar": pygame.image.load("data/imgs/ui/menubar.png"),
        "btn": {
            "home": pygame.image.load("data/imgs/ui/home-mini.png"),
            "search": pygame.image.load("data/imgs/ui/search-mini.png"),
            "settings": pygame.image.load("data/imgs/ui/settings-mini.png")
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
    "sans_bold": pygame.font.Font("data/fonts/Noto_Sans/normal/NotoSans-Bold.ttf", 16),
    "roboto": pygame.font.Font("data/fonts/Roboto/normal/Roboto-Regular.ttf", 16)
}
bgs = {
    "red2blue": pygame.image.load("data/imgs/bg/red2blue.png"),
    "load": pygame.image.load("data/imgs/bg/load.png"),
    "load25": pygame.image.load("data/imgs/bg/load25.png"),
    "load50": pygame.image.load("data/imgs/bg/load50.png"),
    "colors": pygame.image.load("data/imgs/bg/colors.png")
}
sfx = {
    "boot": pygame.mixer.Sound("data/sound/boot.wav"),
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
    def __init__(self, x: int, y: int, title: str, contents: str, dark: bool = False):
        self.x = x
        self.y = y
        self.title = title
        self.dark = dark
        self.text = contents.split("\n")
    
    def draw(self, screen: pygame.Surface):
        if self.dark:
            screen.blit(imgs["ui"]["window"]["dark"], (self.x, self.y))
        else:
            screen.blit(imgs["ui"]["window"]["light"], (self.x, self.y))

        t = self.title

        if len(t) > max_len:
            t = t[:(max_len-3)] + "..."

        color = None
        if self.dark:
            color = colors["white"]
        else:
            color = colors["black"]

        text = fonts["sans_bold"].render(t, True, color)
        screen.blit(text, (self.x + 10, self.y + 4))

        i = 0
        for line in self.text:
            text = fonts["sans"].render(line, True, color)
            screen.blit(text, (self.x + 10, self.y + 36 + i))
            i += 20


for i in range(fr):
    imgs["extra"]["load_fr"].append(pygame.image.load("data/imgs/extra/load3/frame-" + str(i+1) + ".png"))


def Main():
    scr_size = (1280, 720)
    screen = pygame.display.set_mode(scr_size)
    pygame.display.set_caption("PythOS v0.0.1 - booting environment")

    clock = pygame.time.Clock()
    time = 0
    percentage = 0

    # Settings (these are defaults, change these in data/settings.json)
    HIDE_CONSOLE = False
    CONSOLE_IN_DESKTOP = False
    background = true_bgs[0]
    LIGHT_MODE = True

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

    with open("data/settings.json", "r") as f:
        settings = json.load(f)
        HIDE_CONSOLE = settings["hide_console"]
        CONSOLE_IN_DESKTOP = settings["console_in_desktop"]
        background = true_bgs[int(settings["background"])]
        LIGHT_MODE = settings["light_mode"]
        first_boot = settings["first_boot"]

    windows = []
    first_boot_window_text = (
        "Welcome to PythOS v0.0.1!\n" +
        "PythOS is an \"operating system\" built in Python 3.\n\n" +
        "Looks like this is the first time you are using PythOS.\n" +
        "This window will not appear again.\n\n" +
        "Hope you enjoy using PythOS!"
    )
    first_boot_window = Window(
        # centered window
        (scr_size[0] - 800) // 2,
        (scr_size[1] - 600 + 72) // 2,
        "Welcome to PythOS v0.0.1!",
        first_boot_window_text,
        not LIGHT_MODE
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

        if percentage != 200:
            # Console environment
            console[3] = str(time) + " ticks from boot start"
            screen.blit(bg_img, (0, 0))
            screen.blit(logo_img, logo_pos)
            if time % random.randint(4, 7) == 0 and percentage < 100:
                percentage += 1
                console[1] = "Loading " + str(percentage) + "%..."
            if percentage == 100:
                console[1] = "Loading 100%... finished."
                console[2] = "Starting desktop..."
                percentage = 200
                sleep(random.randint(2000, 5000) / 1000)
                pygame.mixer.Sound.play(sfx["boot"])

            load_pos = (
                (scr_size[0] - imgs["extra"]["loading"].get_width()) // 2,
                (scr_size[1] - imgs["extra"]["loading"].get_height()) // 1.025
            )
            screen.blit(imgs["extra"]["load_fr"][(time % fr)], load_pos)

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

            pygame.display.set_caption("PythOS v0.0.1 - desktop environment")

            screen.blit(background, (0, 0))

            for window in windows:
                window.draw(screen)
            
            with open("data/settings.json", "r") as f:
                # data/settings.json/first_boot should be set to false after first boot
                settings = json.load(f)
                settings["first_boot"] = False
                with open("data/settings.json", "w") as f2:
                    json.dump(settings, f2)
                    
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
                            # todo: this code needs to be improved asap
                            if btn == "settings": print("You must change settings in data/settings.json")
                            else: print(btn + " has been pressed")
                b += 1
                
            console_text = []
            console_text_shadow = []
            #console_color = colors["green"]
            console = [
                "PythOS v0.0.1",
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