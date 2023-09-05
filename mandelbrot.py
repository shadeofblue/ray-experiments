from datetime import datetime
import math
import time

from PIL import Image
import ray

ray.init()


ARTIFICIAL_SLOWDOWN = 0.01

FILL = " -+o%#@"

ZOOM = 100000
ASPECT_RATIO = 2.0

SIZE_X = 200
SIZE_Y = 50

X_RANGE = (-.743643135 - 1.0 / ZOOM, -.743643135 + 1.0 / ZOOM)
Y_RANGE = (.131825963 - 1.0 / (ZOOM * ASPECT_RATIO), .131825963 + 1.0 / (ZOOM * ASPECT_RATIO))

X_STEP = (X_RANGE[1] - X_RANGE[0]) / SIZE_X
Y_STEP = (Y_RANGE[1] - Y_RANGE[0]) / SIZE_Y

V_RANGE = (0.0, 1.0)

output = ""

MAX_ITER = 500


def draw_value(v):
    return FILL[math.floor((v - V_RANGE[0]) / (V_RANGE[1] - V_RANGE[0]) * (len(FILL) - 1) )]


def draw_pixel(v):
    return math.floor(v * 256)


@ray.remote
def mandel(x0, y0):
    x = 0.0
    y = 0.0
    i = 0

    while x * x + y * y < 4 and i < MAX_ITER:
        x1 = x * x  - y * y + x0
        y = 2 * x * y + y0
        x = x1
        i += 1

        # time.sleep(ARTIFICIAL_SLOWDOWN)

    return draw_value(i / MAX_ITER)


start = datetime.now()

results = list()

for ys in range(0, SIZE_Y):
    y = Y_RANGE[0] + Y_STEP * ys
    for xs in range(0, SIZE_X):
        x = X_RANGE[0] + X_STEP * xs
        results.append(mandel.remote(x, y))

print("end calculations: ", datetime.now() - start)

for ys in range(0, SIZE_Y):
    for xs in range(0, SIZE_X):
        output += ray.get(results.pop(0))
    output += "\n"


end = datetime.now()

print(output)

print("finished: ", datetime.now() - start)
