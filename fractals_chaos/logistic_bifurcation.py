from casioplot import clear_screen, set_pixel, show_screen
from fractal_lib import SCR_W, SCR_H, wait_for_exit


def main():
    clear_screen()

    ss = show_screen

    for x in range(SCR_W):
        r = 2.5 + 1.5 * x / SCR_W
        val = 0.5

        for _ in range(300 + 128):
            val = r * val * (1 - val)
            if _ >= 300:
                y = SCR_H - int(val * SCR_H)
                set_pixel(x, y, (0, 0, 0))

        ss()
        
    wait_for_exit()


main()
