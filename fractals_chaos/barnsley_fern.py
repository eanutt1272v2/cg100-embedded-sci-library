import random
from casioplot import clear_screen, set_pixel, show_screen
from fractal_lib import SCR_W, SCR_H, read_int, wait_for_exit

N = read_int("Points (default=5000): ", default=5000, min_value=1000, max_value=100000)

def ifs(x, y):
    r = random.random()
    if r < 0.01:
        return 0, 0.16 * y
    elif r < 0.86:
        return 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
    elif r < 0.93:
        return 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
    else:
        return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44


def main():
    clear_screen()

    ss = show_screen
    x, y = 0.0, 0.0

    for _ in range(N):
        x, y = ifs(x, y)
        px = int((x + 2.5) / 5.0 * SCR_W)
        py = int((1 - y / 10.0) * SCR_H)
        if 0 <= px <= SCR_W and 0 <= py <= SCR_H:
            set_pixel(px, py, (0, 150, 0))

        ss()

    wait_for_exit()


main()
