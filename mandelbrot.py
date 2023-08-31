from datetime import datetime
import math
import time

import ray

ray.init()


ARTIFICIAL_SLOWDOWN = 0.01

FILL = " -+o%#@"

SIZE_X = 200
SIZE_Y = 50
X_RANGE = (-2.5, 1.0)
Y_RANGE = (-1.2, 1.2)

X_STEP = (X_RANGE[1] - X_RANGE[0]) / SIZE_X
Y_STEP = (Y_RANGE[1] - Y_RANGE[0]) / SIZE_Y

V_RANGE = (0.0, 1.0)

output = ""

MAX_ITER = 20


def draw_value(v):
    return FILL[math.floor((v - V_RANGE[0]) / (V_RANGE[1] - V_RANGE[0]) * (len(FILL) - 1) )]


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

        time.sleep(ARTIFICIAL_SLOWDOWN)

    return draw_value(i / MAX_ITER)


start = datetime.now()

results = list()

for ys in range(0, SIZE_Y):
    y = Y_RANGE[0] + Y_STEP * ys
    for xs in range(0, SIZE_X):
        x = X_RANGE[0] + X_STEP * xs
        results.append(mandel.remote(x, y))


for ys in range(0, SIZE_Y):
    for xs in range(0, SIZE_X):
        output += ray.get(results.pop(0))
    output += "\n"


end = datetime.now()

print(output)

print(end - start)
