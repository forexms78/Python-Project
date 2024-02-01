from config import lower_color_dic, upper_color_dic

def find_unmatched_ranges(lower_color_dic, upper_color_dic):
    unmatched_ranges = []
    for i in range(256):
        for j in range(256):
            for k in range(256):

                if len(unmatched_ranges) > 100:
                    return unmatched_ranges
                rgb_values = [i, j, k]
                for color, values in lower_color_dic.items():
                    lower_color = lower_color_dic[color]
                    upper_color = upper_color_dic[color]
                    if lower_color[0] <= rgb_values[0] <= upper_color[0] and lower_color[1] <= rgb_values[1] <= upper_color[1] and lower_color[2] <= rgb_values[2] <= upper_color[2]:
                        continue
                    else:
                        unmatched_ranges.append(rgb_values)

    return unmatched_ranges

unmatched_ranges = find_unmatched_ranges(lower_color_dic, upper_color_dic)

print(unmatched_ranges)