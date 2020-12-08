import pygame
import numpy as np

from pydub import AudioSegment

# PARAMETERS

FPS = 30
fpsClock = pygame.time.Clock()

LINE_COUNT = 16
HORZ_MARGIN_PERCENTAGE = 40
VERT_MARGIN_PERCENTAGE = 70
NOISE_SCALE = .003
NOISE_GATE = 640

LINE_WIDTH = 2

TIME_BEFORE_EXIT = 10 # IN SECONDS

# Preload the sound file
sound = AudioSegment.from_mp3("pulsar.wav")
sample_rate = sound.frame_rate // FPS
sound_raw_data = np.fromstring(sound.raw_data[::sample_rate], dtype=np.int16)
sample_count = len(sound_raw_data)

# Samples per line
SPL = sample_count // LINE_COUNT

# Init PyGame
pygame.init()
soundObj = pygame.mixer.Sound('pulsar.wav')
soundObj.play()

screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()


def refine_coords(x,y):
    line = x // SPL
    x %= SPL

    x *= (width*HORZ_MARGIN_PERCENTAGE/100.0) /SPL
    x += (1.0-HORZ_MARGIN_PERCENTAGE/100.0)/2.0 * width

    line_height = height*(1.0-VERT_MARGIN_PERCENTAGE/100.0)/2.0 + \
    line*(height*VERT_MARGIN_PERCENTAGE/ 100.0 / LINE_COUNT) + \
    NOISE_SCALE * 22000 # Adjust for height bump

    y = line_height - NOISE_SCALE*(max(NOISE_GATE, y) - NOISE_GATE)

    return (x,y)
# Calculate Points
points = [refine_coords(x,y) for (x,y) in enumerate(sound_raw_data)]

# Set a blank slate
screen.fill((0, 0, 0))
iters = 1
for iters in range(len(points) + FPS * TIME_BEFORE_EXIT):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not iters%SPL==0 and iters < len(points):
        cache = [(points[iters - 1][0], points[iters-1][1] + LINE_WIDTH/2),
                 (points[iters][0] + LINE_WIDTH * 2, points[iters][1] + LINE_WIDTH/2),
                 (points[iters - 1][0], height + LINE_WIDTH/2),
                 (points[iters][0] + LINE_WIDTH * 2,height + LINE_WIDTH/2)]
        pygame.draw.polygon(screen, (0, 0, 0), cache)
        pygame.draw.line(screen, (255, 255, 255), points[iters-1], points[iters], width=2)

    pygame.display.flip()
    fpsClock.tick(FPS)

# Done! Time to quit.
pygame.quit()

