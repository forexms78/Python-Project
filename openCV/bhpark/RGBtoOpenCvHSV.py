import colorsys

while True:

    R, G, B = map(float, input().split())
    (R, G, B) = (R / 255.0, G / 255.0, B / 255.0)
    (h, s, v) = colorsys.rgb_to_hsv(R, G, B)
    (h, s, v) = (int(h * 179), int(s * 255), int(v * 255))
    print(f'[{h}, {s}, {v}],')


