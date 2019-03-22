import pygame
import random
from polylines import ManyCurves

SCREEN_DIM = (800, 600)

def draw_help(steps):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Z", "Increase velocity by factor 2"])
    data.append(["X", "Decrease velocity by factor 2"])
    data.append(["C", "Delete last point"])
    data.append(["V", "New curve"])
    data.append(["B", "Delete last curve"])
    data.append(["N", "Next curve"])
    data.append(["M", "Previous curve"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))



# main
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True
    curves = ManyCurves(steps)
    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    curves = ManyCurves(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_z:
                    curves.update_velocity(2)
                if event.key == pygame.K_x:
                    curves.update_velocity(0.5)
                if event.key == pygame.K_c:
                    curves.pop_point()
                if event.key == pygame.K_v:
                    curves.new_curve()
                if event.key == pygame.K_b:
                    curves.del_curve()
                if event.key == pygame.K_n:
                    curves.change_curve(1)
                if event.key == pygame.K_m:
                    curves.change_curve(-1)
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                    curves.update_steps(steps)
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                    curves.update_steps(steps)

            if event.type == pygame.MOUSEBUTTONDOWN:
                point = event.pos
                speed = (random.random() * 2, random.random() * 2)
                curves.new_point(point, speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        curves.draw_points(gameDisplay, color=color)
        if not pause:
            curves.set_points(SCREEN_DIM)
        if show_help:
            draw_help(steps)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)