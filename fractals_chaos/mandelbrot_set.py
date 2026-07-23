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
    read_float,
    read_int,
    wait_for_exit,
    generate_color_lut,
)

max_iter = read_int("max_iter (32-256, default=64): ", min_value=32, max_value=256, default=64)
param_cr = read_float("cr (default=-0.75): ", default=-0.75)
param_ci = read_float("ci (default=0.0): ", default=0.0)
R = read_float("R (0=auto, default=2.0): ", min_value=0.0, default=2.0)

print("Colour Maps:")
for idx, entry in CMAP_REGISTRY.items():
    print("%s: %s" % (idx, entry[0]))
cm_choice = read_int("Map (1-8, default=6): ", min_value=1, max_value=8, default=6)

colour_lut, cm_str = generate_color_lut(cm_choice, CMAP_REGISTRY)

samp_den = SAMP - 1 if SAMP > 1 else 1
step = 2.0 * R / samp_den

def main():
    clear_screen()

    hdr = "max_iter=%d R=%.1f c=(%.2f,%.2f) %s" % (max_iter, R, param_cr, param_ci, cm_str)
    draw_string(0, 0, hdr, (0, 0, 160), "small")

    sp, ss = set_pixel, show_screen
    log2 = log(2.0)

    for sy in range(SAMP):
        current_ci = param_ci + R - step * sy
        for sx in range(SAMP):
            current_cr = param_cr - R + step * sx
            zr, zi, n = 0.0, 0.0, 0
            while n < max_iter and zr * zr + zi * zi < 4.0:
                zr, zi = zr * zr - zi * zi + current_cr, 2.0 * zr * zi + current_ci
                n += 1
            
            if n < max_iter:
                mod2 = zr * zr + zi * zi
                if mod2 < 1e-30: mod2 = 1e-30
                ratio = (n + 1.0 - log(log(mod2) / log2) / log2) / max_iter
                if ratio > 1.0: ratio = 1.0
                elif ratio < 0.0: ratio = 0.0
                
                lut_idx = int(ratio * 255.0)
                sp(sx, PY + sy, colour_lut[lut_idx])
            else:
                sp(sx, PY + sy, (0, 0, 0))
        ss()

    leg_den = LEG_H - 1 if LEG_H > 1 else 1
    for py in range(LEG_H):
        t_row = 1.0 - py / leg_den
        col = colour_lut[int(t_row * 255.0)]
        for dx in range(LEG_W):
            sp(LEG_X + dx, PY + py, col)
        if py in (0, LEG_H - 1):
            for dx in range(LEG_W):
                sp(LEG_X + dx, PY + py, (0, 0, 0))
        sp(LEG_X, PY + py, (0, 0, 0))
        sp(LEG_X + LEG_W - 1, PY + py, (0, 0, 0))
        ss()

    for i in range(5):
        t = i / 4.0
        ty = PY + int((1.0 - t) * leg_den)
        for dx in range(3):
            sp(LEG_X + LEG_W + dx, ty, (0, 0, 0))
            
        t_row = 1.0 - (ty - PY) / leg_den
        if t_row < 0.0: t_row = 0.0
        
        tick_val = int(t_row * max_iter)
        lbl = "%d [iters]" % tick_val
        draw_string(LEG_LABEL_X, max(PY, min(PY + LEG_H - 8, ty - 4)), lbl, (0, 0, 0), "small")
        ss()

    wait_for_exit()

main()