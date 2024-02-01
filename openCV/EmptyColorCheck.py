from config import lower_color_dic, upper_color_dic

def find_unmatched_ranges(lower_color_dic, upper_color_dic):
    unmatched_ranges = []
    for color, lower_color in lower_color_dic.items():
        upper_color = upper_color_dic[color]
        for i in range(3):  # Iterate over RGB channels
            if lower_color[i] > upper_color[i]:
                # Swap values if lower bound is greater than upper bound
                lower_color[i], upper_color[i] = upper_color[i], lower_color[i]
            if lower_color[i] != 0 or upper_color[i] != 255:
                # Add the non-default range to the list
                unmatched_ranges.append(([lower_color[i], upper_color[i], i]))

    return unmatched_ranges

def format_ranges(ranges):
    formatted_ranges = []
    for r, channel in ranges:
        formatted_ranges.append(f"{channel}: [{r[0]}, {r[1]}]")
    return formatted_ranges

unmatched_ranges = find_unmatched_ranges(lower_color_dic, upper_color_dic)

if unmatched_ranges:
    print("잡히지 않는 범위:")
    formatted_ranges = format_ranges(unmatched_ranges)
    print(" ~ ".join(formatted_ranges))
else:
    print("모든 범위가 설정되었습니다.")