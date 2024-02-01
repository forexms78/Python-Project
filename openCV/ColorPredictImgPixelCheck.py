import pandas as pd
import os
import cv2
import numpy as np

from config import HSV_lower_color_dic, HSV_upper_color_dic, percent_color_dic, HSV_mapping, HSV_gray_lower_color_dic, \
    HSV_gray_upper_color_dic
import colorsys


def predict_color_by_cv2():
    threshold = 1
    src_path = '../../../../PycharmProjects/pythonProject2/img2/10000img'
    file_name = '4020230173973.jpg'

    pixel_top = 1000



    is_threshold = False
    is_grey = True

    pixel_dic = {}

    extra_value = 5

    img = cv2.imdecode(np.fromfile(os.path.join(src_path, file_name), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    for color, values in HSV_lower_color_dic.items():

        if img is not None:

            lower_color = np.array(values)
            upper_color = np.array(HSV_upper_color_dic[color])

            mask_range = cv2.inRange(img_hsv, lower_color, upper_color)

            num_color_pixels = np.count_nonzero(mask_range)
            num_pixels = img.shape[0] * img.shape[1]
            selected_color_percentage = (num_color_pixels / num_pixels) * 100

            if is_threshold:
                if selected_color_percentage >= threshold:
                    pixel_dic[color] = selected_color_percentage
            else:
                pixel_dic[color] = selected_color_percentage

    if pixel_dic == {}:
        print('pixel_dic is empty')
    else:
        sorted_items = sorted(pixel_dic.items(), key=lambda x: x[1], reverse=True)
        primary_color = sorted_items[0][0]
        primary_color_value = sorted_items[0][1]
        secondary_color = sorted_items[1][0]
        secondary_color_value = sorted_items[1][1]

        if primary_color in HSV_mapping:
            primary_color = HSV_mapping[primary_color]
            if secondary_color in HSV_mapping:
                secondary_color = HSV_mapping[secondary_color]
                if primary_color == secondary_color:
                    primary_color_value += secondary_color_value
                    secondary_color = sorted_items[2][0]
                    secondary_color_value = pixel_dic[secondary_color]

        if secondary_color in HSV_mapping:
            secondary_color = HSV_mapping[secondary_color]

    print(pixel_dic)

    flattened_img_hsv = img_hsv.reshape((-1, 3))

    if not is_grey:
        filtered_hsv = flattened_img_hsv[(flattened_img_hsv[:, 1] >= 20) & (flattened_img_hsv[:, 2] >= 20)]
        unique_hsv, counts_hsv = np.unique(filtered_hsv, axis=0, return_counts=True)
    else:
        unique_hsv, counts_hsv = np.unique(flattened_img_hsv, axis=0, return_counts=True)

    hsv_count_pairs = list(zip(unique_hsv, counts_hsv))
    sorted_hsv_count_pairs = sorted(hsv_count_pairs, key=lambda x: x[1], reverse=True)

    for i, (hsv, count) in enumerate(sorted_hsv_count_pairs[:pixel_top]):
        pixel_color = 0
        (H, S, V) = hsv
        (H2, S2, V2) = (H * 2, round(S * 3.92 / 10), round(V * 3.92 / 10))
        (H, S, V) = (H / 179.0, S / 255.0, V / 255.0)
        (r, g, b) = colorsys.hsv_to_rgb(H, S, V)
        (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))

        for color, value in HSV_lower_color_dic.items():
            lower_color = np.array(values)
            upper_color = np.array(HSV_upper_color_dic[color])
            if value[0] <= hsv[0] <= upper_color[0] and value[1] <= hsv[1] <= upper_color[1] and value[
                2] <= hsv[2] <= \
                    upper_color[2]:
                pixel_color = color
                break


        for color, value in HSV_gray_lower_color_dic.items():
            lower_color = np.array(values)
            upper_color = np.array(HSV_gray_upper_color_dic[color])
            if value[0] <= hsv[0] <= upper_color[0] and value[1] <= hsv[1] <= upper_color[1] and value[
                2] <= hsv[2] <= \
                    upper_color[2]:
                pixel_color = color
                break

        if pixel_color == 0:
            print(
                f"Top {i + 1} HSV Value: {hsv} RGB Value: [{r}, {g}, {b}] HSV 100% Value: [{H2}, {S2}, {V2}] , Count: {count}")
            pixel_color = 0

        else:
            print(
                f"Top {i + 1} HSV Value: {hsv} RGB Value: [{r}, {g}, {b}] HSV 100% Value: [{H2}, {S2}, {V2}] , Count: {count} color: [{pixel_color}]")
            pixel_color = 0


# 색상 추가하는거까지

    print(
        f'출원번호 : {file_name} / 예측된 색상 : {primary_color} / 예측된 색상의 유사도 : {primary_color_value:.2f} / 다음 예측된 색상 : {secondary_color} / 다음 예측된 색상의 유사도 : {secondary_color_value:.2f}')

# predicted_color #예측된 색상카테고리
predict_color_by_cv2()
