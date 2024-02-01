import colorsys

while True:
    H, S, V = map(float, input().split())
    (H, S, V) = (H / 179.0, S / 255.0, V / 255.0)
    (r, g, b) = colorsys.hsv_to_rgb(H, S, V)
    (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
    print(f'[{r}, {g}, {b}],')
