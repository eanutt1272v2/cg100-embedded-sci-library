# Plot logistic-map bifurcation behaviour on the Casio fx-CG100.

from casioplot import clear_screen, set_pixel, show_screen

try:
    from casioplot import getkey
except ImportError:
    getkey = None


def wait_for_exit():
    if getkey is not None:
        getkey()
    else:
        input("\nPress any key to exit: ")


def main():
    r_min = 2.5
    r_max = 4.0
    W = 384
    H = 180
    skip = 300
    keep = 150

    clear_screen()
    show_screen()

    for px in range(W):
        r = r_min + (r_max - r_min) * px / W
        x = 0.5
        for _ in range(skip):
            x = r * x * (1 - x)
        for _ in range(keep):
            x = r * x * (1 - x)
            py = H - int(x * H)
            if 0 <= py <= H:
                set_pixel(px, py + 10, (0, 0, 0))

    show_screen()
    wait_for_exit()


main()
