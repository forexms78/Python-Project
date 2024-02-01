from config import HSV_mapping


def extract_2_similar_colors(pixel_dic):
    if pixel_dic == {}:
        print('pixel_dic is empty')
        primary_color = '그 외'
        primary_color_value = 0
        secondary_color = '그 외'
        secondary_color_value = 0
        sorted_items = []
        return primary_color, primary_color_value, secondary_color, secondary_color_value, sorted_items
    else:
        sorted_items = sorted(pixel_dic.items(), key=lambda x: x[1], reverse=True)
        primary_color = sorted_items[0][0]
        primary_color_value = sorted_items[0][1]
        secondary_color = sorted_items[1][0]
        secondary_color_value = sorted_items[1][1]

        if primary_color in HSV_mapping:
            primary_color = HSV_mapping[primary_color]
            cnt = 2
            while True:
                if secondary_color in HSV_mapping:
                    secondary_color = HSV_mapping[secondary_color]
                    if primary_color == secondary_color:
                        primary_color_value += secondary_color_value
                        secondary_color = sorted_items[cnt][0]
                        secondary_color_value = pixel_dic[secondary_color]
                        cnt += 1
                    else:
                        break
                else:
                    break



        if secondary_color in HSV_mapping:
            secondary_color = HSV_mapping[secondary_color]
        return primary_color, primary_color_value, secondary_color, secondary_color_value, sorted_items
