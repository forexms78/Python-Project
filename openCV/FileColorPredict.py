import pandas as pd
from datetime import datetime

from config import lower_color_dic, upper_color_dic, percent_color_dic, color_mapping


def predict_color_by_cv2():
    import os
    import cv2
    import numpy as np

    threshold = 0
    src_path = '../../../../PycharmProjects/pythonProject2/img2/010103_TOTAL'
    file_name = '4020230054828.jpg'

    is_threshold = False

    pixel_dic = {}
    predicted_color = '그 외'
    next_predicted_color = '그 외'

    for color, values in lower_color_dic.items():
        img = cv2.imdecode(np.fromfile(os.path.join(src_path, file_name), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

        if img is not None:

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            if color == '회색':
                mask2 = np.zeros(img.shape[:2], dtype=bool)
                mask2[(img[:, :, 0] == img[:, :, 1]) & (img[:, :, 0] == img[:, :, 2])] = True

                mask_img = img.copy()

                mask_img[~mask2] = 0
            elif color == '검정':
                threshold_diff = 10
                black_pixels = np.where(
                    (img[:, :, 0] <= upper_color[0]) &
                    (img[:, :, 1] <= upper_color[1]) &
                    (img[:, :, 2] <= upper_color[2]) &

                    (np.max(img, axis=2) - np.min(img, axis=2) < threshold_diff))

                percentage = len(black_pixels[0]) * 100.0 / num_pixels

                if percentage >= threshold:
                    pass
                else:
                    continue
                other_pixels = np.where(
                    ((img[:, :, 0] > 60) |
                     (img[:, :, 1] > 60) |
                     (img[:, :, 2] > 54)) &
                    ~(((img[:, :, 0] <= 230) & (img[:, :, 0] <= 255)) &
                      ((img[:, :, 1] <= 230) & (img[:, :, 1] <= 255)) &
                      ((img[:, :, 2] <= 230) & (img[:, :, 2] <= 255))) &
                    ~((img[:, :, 0] == img[:, :, 1]) & (img[:, :, 0] == img[:, :, 2])))

                other_percent = len(other_pixels[0]) * 100.0 / num_pixels

                other_color_threshold = 1

                if other_percent >= other_color_threshold:
                    continue
            elif color == '청록':

                color_range_mask = cv2.inRange(img, lower_color, upper_color)
                b_ge_g_mask = (img[:, :, 2] >= img[:, :, 1]).astype(np.uint8)
                b_g_diff_mask = (np.abs(img[:, :, 2] - img[:, :, 1]) <= 20).astype(np.uint8)
                gb_condition_mask = cv2.bitwise_and(b_ge_g_mask, b_g_diff_mask)
                mask_range = cv2.bitwise_and(color_range_mask, gb_condition_mask)

            lower_color = np.array(values)
            upper_color = np.array(upper_color_dic[color])
            mask_range = cv2.inRange(img, lower_color, upper_color)

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
        primary_color = max(pixel_dic, key=pixel_dic.get)
        primary_color_value = max(pixel_dic.values())

    if primary_color in color_mapping:
        if percent_color_dic[primary_color] <= primary_color_value:
            predicted_color = color_mapping[primary_color]
    else:
        if percent_color_dic[primary_color] <= primary_color_value:
            predicted_color = primary_color

    secondary_color = max(pixel_dic, key=lambda k: pixel_dic[k] if k != primary_color else -1)
    secondary_color_value = pixel_dic[secondary_color]

    if secondary_color in color_mapping:
        if (percent_color_dic[secondary_color] / 3) <= secondary_color_value:
            next_predicted_color = color_mapping[secondary_color]
    elif (percent_color_dic[secondary_color] / 3) <= secondary_color_value: \
            next_predicted_color = secondary_color

    if percent_color_dic == next_predicted_color:
        primary_color_value += secondary_color_value
        secondary_color = max(pixel_dic, key=lambda k: pixel_dic[k] if k != primary_color and k != secondary_color else -1)
        secondary_color_value = pixel_dic[secondary_color]

        if secondary_color in color_mapping:
            if (percent_color_dic[secondary_color] / 3) <= secondary_color_value:
                next_predicted_color = color_mapping[secondary_color]
        elif (percent_color_dic[secondary_color] / 3) <= secondary_color_value: \
                next_predicted_color = secondary_color

        secondary_color = max(pixel_dic, key=lambda k: pixel_dic[k] if k != primary_color and k != secondary_color else -1)
        secondary_color_value = pixel_dic[secondary_color]

    flattened_img = img.reshape((-1, 3))

    # Exclude the specified RGB range (250 250 250 to 255 255 255)
    excluded_range = np.all((flattened_img >= [250, 250, 250]) & (flattened_img <= [255, 255, 255]), axis=1)
    flattened_img = flattened_img[~excluded_range]

    # Calculate the unique RGB values and their counts
    unique_colors, counts = np.unique(flattened_img, axis=0, return_counts=True)

    # Combine the unique colors and their counts into a list of tuples
    color_count_pairs = list(zip(unique_colors, counts))

    # Sort the list based on the counts in descending order
    sorted_color_count_pairs = sorted(color_count_pairs, key=lambda x: x[1], reverse=True)

    # Select the top 5 RGB values
    top_5_colors = sorted_color_count_pairs[:40]

    # Print the top 5 RGB values
    for i, (color, count) in enumerate(top_5_colors):
        print(f"Top {i + 1} RGB Value: {color}, Count: {count}")

    print(
        f'출원번호 : {file_name} / 예측된 색상 : {predicted_color} / 예측된 색상의 유사도 : {primary_color_value:.2f} / 다음 예측된 색상 : {next_predicted_color} / 다음 예측된 색상의 유사도 : {secondary_color_value:.2f}')


# predicted_color #예측된 색상카테고리
predict_color_by_cv2()
