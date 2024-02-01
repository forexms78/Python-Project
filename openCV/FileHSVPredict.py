import pandas as pd
import os
import cv2
import numpy as np

from config import HSV_lower_color_dic, HSV_upper_color_dic, percent_color_dic, HSV_mapping, HSV_dic_value


def predict_color_by_cv2():
    threshold = 1
    src_path = '../../../../PycharmProjects/pythonProject2/img2/010103_TOTAL'
    file_name = '4020220009088.jpg'

    is_threshold = False

    pixel_dic = {}
    predicted_color = '그 외'
    next_predicted_color = '그 외'

    extra_value = 5

    img = cv2.imdecode(np.fromfile(os.path.join(src_path, file_name), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    for color, values in HSV_dic_value.items():

        if img is not None:

            lower_values = [x - extra_value for x in values]
            upper_values = [x + extra_value for x in HSV_dic_value[color]]

            lower_color2 = np.array(lower_values)
            upper_color2 = np.array(upper_values)

            # lower_color = np.array(values)
            # upper_color = np.array(HSV_upper_color_dic[color])

            mask_range = cv2.inRange(img_hsv, lower_color2, upper_color2)

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
        max_key = sorted_items[0][0]
        max_value = sorted_items[0][1]
        next_max_key = sorted_items[1][0]
        next_max_value = sorted_items[1][1]

        if max_key in HSV_mapping:
            max_key = HSV_mapping[max_key]
            if next_max_key in HSV_mapping:
                next_max_key = HSV_mapping[next_max_key]
                if max_key == next_max_key:
                    max_value += next_max_value
                    next_max_key = sorted_items[2][0]
                    next_max_value = pixel_dic[next_max_key]

        if next_max_key in HSV_mapping:
            next_max_key = HSV_mapping[next_max_key]


    print(pixel_dic)

    flattened_img_hsv = img_hsv.reshape((-1, 3))

    # Define the ranges to exclude
    # exclude_range_lower_1 = np.array([23, 250, 253])
    # exclude_range_upper_1 = np.array([24, 255, 255])
    #
    # exclude_range_lower_2 = np.array([0, 0, 0])
    # exclude_range_upper_2 = np.array([0, 0, 255])
    #
    # # Exclude values within the specified ranges
    # excluded_range_1 = np.all(
    #     (flattened_img_hsv >= exclude_range_lower_1) & (flattened_img_hsv <= exclude_range_upper_1), axis=1)
    # excluded_range_2 = np.all(
    #     (flattened_img_hsv >= exclude_range_lower_2) & (flattened_img_hsv <= exclude_range_upper_2), axis=1)
    # excluded_range = excluded_range_1 | excluded_range_2
    # flattened_img_hsv = flattened_img_hsv[~excluded_range]

    filtered_hsv = flattened_img_hsv[(flattened_img_hsv[:, 1] >= 100) & (flattened_img_hsv[:, 2] >= 100)]

    unique_hsv, counts_hsv = np.unique(filtered_hsv, axis=0, return_counts=True)

    hsv_count_pairs = list(zip(unique_hsv, counts_hsv))

    sorted_hsv_count_pairs = sorted(hsv_count_pairs, key=lambda x: x[1], reverse=True)

    for i, (hsv, count) in enumerate(sorted_hsv_count_pairs[:100]):
        print(f"Top {i + 1} HSV Value: {hsv}, Count: {count}")

    print(
        f'출원번호 : {file_name} / 예측된 색상 : {max_key} / 예측된 색상의 유사도 : {max_value:.2f} / 다음 예측된 색상 : {next_max_key} / 다음 예측된 색상의 유사도 : {next_max_value:.2f}')


# predicted_color #예측된 색상카테고리
predict_color_by_cv2()
