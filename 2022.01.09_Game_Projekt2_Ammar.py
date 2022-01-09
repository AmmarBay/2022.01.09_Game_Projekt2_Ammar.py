import os
import random
from math import sqrt
import pygame
from pygame import mixer

class Settings:
    height = 550
    width = 750
    fps = 60
    title = "Bubble"
    path_working_directory = os.path.dirname(os.path.abspath(__file__))
    path_contents = os.path.join(path_working_directory, 'contents')
    path_images = os.path.join(path_contents, 'images')
    path_sounds = os.path.join(path_contents, 'sounds')
    path_highscore = os.path.join(path_working_directory, 'highscore.txt')
    bubble_radius = 5
    bubble_delay = 1000
    bubble_speed = 1
    bubbles_max = 9

    # Schriftart und -größe 
    font_pause = ('arial.ttf', 64)
    font_gameover = ('arial.ttf', 64)
    font_restart = ('arial.ttf', 34)
    font_score = ('arial.ttf', 48)
    font_highscore = ('arial.ttf', 30)
    font_points = ('arial.ttf', 30)

    
    title_score = "Score: %s"
    title_highscore = "Highscore: %s"

class Timer:
    def __init__(self, duration, start=False):
        self.duration = duration
        self.next = pygame.time.get_ticks()

        if not start:
            self.next += self.duration

    def reached(self):

        if pygame.time.get_ticks() >= self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

class Background(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_images, filename))
        self.image = pygame.transform.scale(self.image, (Settings.width,Settings.height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

class Cursor(pygame.sprite.Sprite):
    # Zeigereinstellungen
    def __init__(self):
        super().__init__()
        self.cursors = [
            pygame.image.load(os.path.join(Settings.path_images,'cursor1.png')),
            pygame.image.load(os.path.join(Settings.path_images,'cursor2.png'))
        ]

        self.image = self.cursors[0]
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

    def select_cursor(self, cursor_number):

        self.image = self.cursors[cursor_number]
        self.image = pygame.transform.scale(self.image, (20, 20))

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def update(self, pos):

        self.rect = pos

class Bubble(pygame.sprite.Sprite):
    # Bubble einstellungen
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join(Settings.path_images, 'bubble1.png')) 
        self.image = pygame.transform.scale(self.image,(30,30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(10 + Settings.bubble_radius,Settings.width -Settings.bubble_radius -10),
                    random.randint(10 + Settings.bubble_radius,Settings.height -Settings.bubble_radius -10))
        pygame.mixer.Sound.play(game.spawn)



    def is_hovered(self, mouse_pos):

        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):

        screen.blit(self.image, self.rect)


    def check_window_collision(self):
  
        left_pos = self.rect.center[0] - self.rect.width // 2
        if left_pos < 0:
            pygame.mixer.Sound.play(game.collision)
            game.gameover()

        right_pos = self.rect.center[0] + self.rect.width // 2
        if right_pos > Settings.width:
            pygame.mixer.Sound.play(game.collision)
            game.gameover()

        top_pos = self.rect.center[1] - self.rect.height // 2
        if top_pos < 0:
            pygame.mixer.Sound.play(game.collision)
            game.gameover()

        bottom_pos = self.rect.center[1] + self.rect.height // 2
        if bottom_pos > Settings.height:
            pygame.mixer.Sound.play(game.collision)
            game.gameover()


    def update(self):
        self.check_window_collision()


class Game:
    # Haupteinstellungen
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Settings.title)
        pygame.mouse.set_visible(False)

        self.running = True
        self.screen = pygame.display.set_mode((Settings.width,Settings.height))
        self.clock = pygame.time.Clock()
        self.cursor = Cursor()
        self.bubble_delay_timer = Timer(Settings.bubble_delay)
        self.bubble_size_timer = Timer(Settings.bubble_delay)
        self.background = Background("background.jpg")
        self.bubbles = pygame.sprite.Group()
        self.bubbles_limit = Settings.bubbles_max
        self.game_over = False
        self.pause = False
        self.points = 0
        # Toneinstellungen
        self.pop = pygame.mixer.Sound(os.path.join(Settings.path_sounds,'pop.mp3'))
        self.spawn = pygame.mixer.Sound(os.path.join(Settings.path_sounds,'spawn.mp3'))
        self.collision = pygame.mixer.Sound(os.path.join(Settings.path_sounds,'collision.mp3'))

        self.restart_surface = pygame.Surface((200, 50))
        self.restart_surface.fill((255, 255, 255))
        self.restart_surface_rect = self.restart_surface.get_rect()
        self.restart_surface_rect.center = (
            Settings.width // 2, Settings.height // 2 + 175)

    def run(self):

        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_event()
            self.draw()
            self.cursor.update(pygame.mouse.get_pos())
            if not self.pause and not self.game_over:
                self.update()
            

    def watch_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                #mein spiel noch nicht fertig aber mit x kann man es beenden
                elif event.key == pygame.K_x:
                    self.gameover()
                    pygame.mixer.Sound.play(self.collision)
                elif event.key == pygame.K_p:
                    self.pause = not self.pause

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.pause = not self.pause
                if self.pause:
                    return

                if event.button == 1:
                    if self.game_over:
                        self.click_restart(event.pos)
                        return

                for bubble in self.bubbles:
                    if bubble.is_hovered(event.pos):
                        bubble.kill()
                        self.points += 7
                        pygame.mixer.Sound.play(self.pop)
                        break

    def respawn_bubbles(self):

        if len(self.bubbles.sprites()) <= self.bubbles_limit:
            if self.bubble_delay_timer.reached():
                self.bubbles.add(Bubble())

    def update(self):
        self.respawn_bubbles()
        self.bubbles.update()
        cursor_on_bubble = False
        for bubble in self.bubbles.sprites():
            if bubble.is_hovered(pygame.mouse.get_pos()):
                cursor_on_bubble = True
            self.cursor.select_cursor(1 if cursor_on_bubble else 0)

    def draw(self):
        self.background.draw(self.screen)
        self.bubbles.draw(self.screen)
        self.draw_points()
        if self.pause:
            self.draw_pause()
        if self.game_over:
            self.draw_gameover()
        self.cursor.draw(self.screen)
        pygame.display.flip()

    def draw_pause(self):
    # Die Pause-Bildschirm

        end = pygame.Surface(self.screen.get_size())
        end.set_alpha(180)
        self.screen.blit(end, (0, 0))
        font = pygame.font.SysFont(Settings.font_pause[0],Settings.font_pause[1])
        pause_text = font.render('PAUSE', True, (255, 255, 255))
        pause_text_rect = pause_text.get_rect()
        pause_text_rect.center = (Settings.width // 2, Settings.height // 2)
        self.screen.blit(pause_text, pause_text_rect)

    def draw_gameover(self):
    # Points, Highscore ,GAME OVER und RESTART  auf dem Game-Over-Bildschirm
        end = pygame.Surface(self.screen.get_size())
        end.set_alpha(180)
        self.screen.blit(end, (0, 0))
        font = pygame.font.SysFont(Settings.font_gameover[0],Settings.font_gameover[1])
        gameover_text = font.render('GAME OVER', True, (255, 0, 0))
        gameover_text_rect = gameover_text.get_rect()
        gameover_text_rect.center = (Settings.width // 2, Settings.height // 2 - 30)
        self.screen.blit(gameover_text, gameover_text_rect)

        font = pygame.font.SysFont(Settings.font_score[0],Settings.font_score[1])
        points_text = font.render(Settings.title_score.replace('%s', str(self.points)), True, (255, 255, 255))
        points_text_rect = points_text.get_rect()
        points_text_rect.center = (Settings.width // 2, Settings.height // 2 + 50)

        self.screen.blit(points_text, points_text_rect)
        font = pygame.font.SysFont(Settings.font_highscore[0],Settings.font_highscore[1])
        highscore_text = font.render(Settings.title_highscore.replace('%s', str(self.get_highscore())), True, (250, 255, 0))
        highscore_text_rect = highscore_text.get_rect()
        highscore_text_rect.center = (Settings.width // 2, Settings.height // 2 + 115)
        self.screen.blit(highscore_text, highscore_text_rect)

        font = pygame.font.SysFont(Settings.font_restart[0],Settings.font_restart[1])
        restart_text = font.render("RESTART", True, (250, 150, 0))
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = (Settings.width // 2, Settings.height // 2 + 175)
        self.screen.blit(restart_text, restart_text_rect)


    def click_restart(self, mouse_position):

        if self.restart_surface_rect.collidepoint(mouse_position):
            self.restart()

    def restart(self):
    # Spiel neustarten
        self.points = 0
        self.bubbles.empty()
        self.game_over = False
        self.pause = False


    def get_highscore(self):

        with open(Settings.path_highscore) as file:
            highscore = file.read()
        return highscore

    def set_highscore(self,highscore):
        with open(Settings.path_highscore, 'w') as file:
            file.write(str(highscore))

    def save_highscore(self):
    # Highscore in Datei speichern
        if self.points > int(self.get_highscore()):
            self.set_highscore(self.points)
            
    def gameover(self) -> None:

        self.save_highscore()
        self.game_over = True

    def draw_points(self):
    # points und highscore auf dem bildschirm
        
        font = pygame.font.SysFont(
            Settings.font_points[0],
            Settings.font_points[1])
        points_text = font.render(Settings.title_score.replace('%s', str(self.points)), True, (255, 150, 0))
        points_text_rect = points_text.get_rect()
        points_text_rect.top = Settings.height - 30
        points_text_rect.left = 25
        self.screen.blit(points_text, points_text_rect)

        font = pygame.font.SysFont(Settings.font_highscore[0],Settings.font_highscore[1])
        highscore_text = font.render(Settings.title_highscore.replace('%s', str(self.get_highscore())), True, (255, 150, 0))
        highscore_text_rect = highscore_text.get_rect()
        highscore_text_rect.top = Settings.height - 30
        highscore_text_rect.left = 580
        self.screen.blit(highscore_text, highscore_text_rect)



if __name__ == '__main__':
    os.environ
    game = Game()
    game.run()
