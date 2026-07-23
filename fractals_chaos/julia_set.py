from casioplot import clear_screen, draw_string, set_pixel, show_screen
from math import log
from fractal_lib import (
    PY,
    SAMP,
    LEG_X,
    LEG_W,
    LEG_H,
    LEG_LABEL_X,
    CMAP_REGISTRY,
    read_int,
    read_float,
    wait_for_exit,
    generate_color_lut,
)

max_iter = read_int("max_iter (32-256, default=64): ", min_value=32, max_value=256, default=64)
c_re = read_float("c_re (default=-0.7): ", default=-0.7)
c_im = read_float("c_im (default=0.27): ", default=0.27)
zr0 = read_float("zr0 (default=0.0): ", default=0.0)
zi0 = read_float("zi0 (default=0.0): ", default=0.0)
R = read_float("R (0=auto, default=2.0): ", min_value=0.0, default=2.0)

print("Colour Maps:")
for idx, entry in CMAP_REGISTRY.items():
    print("%s: %s" % (idx, entry[0]))
cm_choice = read_int("Map (1-8, default=6): ", min_value=1, max_value=8, default=6)

colour_lut, cm_str = generate_color_lut(cm_choice, CMAP_REGISTRY)

samp_den = SAMP - 1 if SAMP > 1 else 1
step = 2.0 * R / samp_den
x_min, y_max = zr0 - R, zi0 + R

def main():
    clear_screen()

    hdr = "max_iter=%d R=%.1f c=(%.2f,%.2f) %s" % (max_iter, R, c_re, c_im, cm_str)
    draw_string(0, 0, hdr, (0, 0, 160), "small")

    sp, ss = set_pixel, show_screen
    log2 = log(2.0)

    py = 0
    while py < SAMP:
        zi_row = y_max - step * py
        y_coord = PY + py
        px = 0
        while px < SAMP:
            zr = x_min + step * px
            zi = zi_row
            n = 0
            while n < max_iter and zr * zr + zi * zi < 4.0:
                zr, zi = zr * zr - zi * zi + c_re, 2.0 * zr * zi + c_im
                n += 1
            
            if n < max_iter:
                mod2 = zr * zr + zi * zi
                if mod2 < 1e-30: mod2 = 1e-30
                ratio = (n + 1.0 - log(log(mod2) / log2) / log2) / max_iter
                if ratio > 1.0: ratio = 1.0
                elif ratio < 0.0: ratio = 0.0
                
                sp(px, y_coord, colour_lut[int(ratio * 255.0)])
            else:
                sp(px, y_coord, (0, 0, 0))
            px += 1
        ss()
        py += 1

    leg_den = LEG_H - 1 if LEG_H > 1 else 1
    ly = 0
    while ly < LEG_H:
        t_row = 1.0 - ly / leg_den
        col = colour_lut[int(t_row * 255.0)]
        y_coord = PY + ly
        
        dx = 0
        while dx < LEG_W:
            sp(LEG_X + dx, y_coord, col)
            dx += 1
            
        if ly in (0, LEG_H - 1):
            dx = 0
            while dx < LEG_W:
                sp(LEG_X + dx, y_coord, (0, 0, 0))
                dx += 1
                
        sp(LEG_X, y_coord, (0, 0, 0))
        sp(LEG_X + LEG_W - 1, y_coord, (0, 0, 0))
        ss()
        ly += 1

    i = 0
    while i < 5:
        t = i * 0.25
        ty = PY + int((1.0 - t) * leg_den)
        
        dx = 0
        while dx < 3:
            sp(LEG_X + LEG_W + dx, ty, (0, 0, 0))
            dx += 1
            
        t_row = 1.0 - (ty - PY) / leg_den
        if t_row < 0.0: t_row = 0.0
        
        lbl = "%d [iters]" % int(t_row * max_iter)
        draw_string(LEG_LABEL_X, max(PY, min(PY + LEG_H - 8, ty - 4)), lbl, (0, 0, 0), "small")
        ss()
        i += 1
        
    wait_for_exit()

main()