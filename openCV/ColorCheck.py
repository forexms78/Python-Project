import numpy as np
from config import lower_color_dic, upper_color_dic


def check_color_range(rgb_values, lower_color_dic, upper_color_dic):
    matching_colors = []
    for color, values in lower_color_dic.items():
        lower_color = np.array(lower_color_dic[color])
        upper_color = np.array(upper_color_dic[color])
        if np.all(rgb_values >= lower_color) and np.all(rgb_values <= upper_color):
            matching_colors.append(color)

    if matching_colors:
        print("겹치는 색상:", matching_colors)
        return matching_colors
    else:
        print("색상이 없습니다.")
        return None


RGB_values = list(map(int, input("Enter RGB values (e.g., 255 0 0): ").split()))

result = check_color_range(RGB_values, lower_color_dic, upper_color_dic)
