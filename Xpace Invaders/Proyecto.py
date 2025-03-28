import pygame
import pygame_menu

pygame.init()
pantalla=pygame.display.set_mode((600, 400))

class Game:
    screen=None
    aliens=[]
    rockets=[]
    lost=False
    win=False

    def __init__(self,width, height, dificultad):
        self.ancho=width
        self.alto=height
        self.screen= pygame.display.set_mode((width, height))
        self.clock= pygame.time.Clock()
        self.fondo=pygame.image.load("fondo.jpg")
        self.dificultad=dificultad
        done=False

        pygame.mixer.music.load("Purgatorium.wav")
        pygame.mixer.music.play(-1)

        hero=Hero(self, width/2, height-20)
        generator=Generator(self, self.dificultad)

        while not done:
            if len(self.aliens)==0:
                self.win = True
                self.displayText("You win!!")

            pressed=pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 5 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 5 if hero.x < width - 20 else 0
            elif pressed[pygame.K_UP]:
                hero.y -= 5 if hero.y > 20 else 0
            elif pressed[pygame.K_DOWN]:
                hero.y += 5 if hero.y < height - 20 else 0


            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    done=True
                if event.type==pygame.KEYDOWN and event.key== pygame.K_SPACE and len(self.rockets)<4:
                    self.rockets.append(Rocket(self, hero.x + 24, hero.y - 5))


            pygame.display.flip()
            self.clock.tick(60)
            #self.screen.fill((0, 0, 0))
            self.screen.blit(self.fondo, (0,0))


            for alien in self.aliens:
                alien.draw()
                alien.checkColission(self)

                if (alien.y > height):
                    self.lost=True
                    self.displayText("Try again")

            for rocket in self.rockets:
                if not self.win: rocket.draw()
                if rocket.y <=0:
                    self.rockets.remove(rocket)

            if not self.lost : hero.draw()
            
            
    def displayText(self, text):
        pygame.font.init()
        font=pygame.font.SysFont("Arial", size=50, bold=True, italic=True)
        textSurface=font.render(text, False, (255,255,255))
        self.screen.blit(textSurface, (190,100))


class Alien:
    def __init__(self, game, x, y, speed):
        self.x=x
        self.game=game
        self.y=y
        self.size=30
        self.image=pygame.image.load("alien.png")
        self.speed=speed

    def draw(self):

        self.game.screen.blit(self.image,(self.x, self.y))

        self.y += self.speed

    def checkColission(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + self.size and rocket.x > self.x - self.size and rocket.y < self.y + self.size and rocket.y > self.y - self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)


class Hero:
    def __init__(self, game, x, y):
        self.x=x
        self.y=y
        self.game=game
        self.image = pygame.image.load("nave.png")

    def draw(self):
        #pygame.draw.rect(self.game.screen, (58, 206, 233), pygame.Rect(self.x, self.y, 35, 8))
        self.game.screen.blit(self.image, (self.x, self.y))


class Rocket:
    def __init__(self, game, x, y):
        self.x=x
        self.y=y
        self.game=game


    def draw(self):
        pygame.draw.rect(self.game.screen, (25,169,169), pygame.Rect(self.x, self.y, 4, 6))

        self.y-=6


class Generator:
    def __init__(self, game, speed):
        margin=30
        width=50

        for x in range(margin, game.ancho-margin,width):
            for y in range(margin, int(game.alto/2), width):
                game.aliens.append(Alien(game, x, y,speed))




def Start_easy():
    Game(600, 400, 0.1)

def Start_medium():
    Game(600, 400, 0.3)

def Start_hard():
    Game(600, 400, 0.5)



menu=pygame_menu.Menu(height=400, theme= pygame_menu.themes.THEME_DARK, title="Welcome", width=600)

menu.add.button("Easy", Start_easy)
menu.add.button("Medium", Start_medium)
menu.add.button("Hard", Start_hard)
menu.add.button("Exit", pygame_menu.events.EXIT)





if __name__ == "__main__":
    menu.mainloop(pantalla)