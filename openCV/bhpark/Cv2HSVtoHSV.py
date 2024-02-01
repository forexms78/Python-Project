import colorsys

while True:
    H, S, V = map(float, input().split())
    (H, S, V) = (H / 179.0, S / 255.0, V / 255.0)
    (r, g, b) = colorsys.hsv_to_rgb(H, S, V)
    (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
    (h, s, v) = (int(h * 360), int(s * 100), int(v * 100))
    print(f'# {h} {s} {v}')
