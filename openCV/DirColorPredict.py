import pandas as pd
from datetime import datetime

from config import lower_color_dic, upper_color_dic, percent_color_dic, color_mapping


def predict_color_by_cv2():
    import os
    import cv2
    import numpy as np

    threshold = 0
    src_path = '/Users/bhpark/PycharmProjects/pythonProject2/img2/010102_TOTAL'

    file_list = os.listdir(src_path)

    csv_file = []
    cnt = 0
    is_threshold = False

    # If number_of_image_files is set to 0, all files in the directory will be rotated by that number.
    number_of_image_files = 200

    if number_of_image_files == 0:
        number_of_image_files = len(file_list)

    for img_file in file_list[:number_of_image_files]:
        cnt += 1
        print(img_file)
        if img_file == '.DS_Store':
            continue
        else:
            pixel_dic = {}
            predicted_color = '그 외'
            next_predicted_color = '그 외'

            for color, values in lower_color_dic.items():
                img = cv2.imdecode(np.fromfile(os.path.join(src_path, img_file), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

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

            print(f'[{cnt}/{number_of_image_files}]')

            if pixel_dic == {}:
                print('pixel_dic is empty')
                continue
            else:
                max_key = max(pixel_dic, key=pixel_dic.get)
                max_value = max(pixel_dic.values())


            if max_key in color_mapping:
                if percent_color_dic[max_key] <= max_value:
                    predicted_color = color_mapping[max_key]
            else:
                if percent_color_dic[max_key] <= max_value:
                    predicted_color = max_key

            next_max_key = max(pixel_dic, key=lambda k: pixel_dic[k] if k != max_key else -1)
            next_max_value = pixel_dic[next_max_key]

            if next_max_key in color_mapping:
                if (percent_color_dic[next_max_key] / 3) <= next_max_value:
                    next_predicted_color = color_mapping[next_max_key]
            elif (percent_color_dic[next_max_key] / 3) <= next_max_value: \
                    next_predicted_color = next_max_key

            if percent_color_dic == next_predicted_color:
                max_value += next_max_value
                next_max_key = max(pixel_dic, key=lambda k: pixel_dic[k] if k != max_key and k != next_max_key else -1)
                next_max_value = pixel_dic[next_max_key]

                if next_max_key in color_mapping:
                    if (percent_color_dic[next_max_key] / 3) <= next_max_value:
                        next_predicted_color = color_mapping[next_max_key]
                elif (percent_color_dic[next_max_key] / 3) <= next_max_value: \
                        next_predicted_color = next_max_key

                next_max_key = max(pixel_dic, key=lambda k: pixel_dic[k] if k != max_key and k != next_max_key else -1)
                next_max_value = pixel_dic[next_max_key]

            csv_file.append(
                [img_file, predicted_color, f'{max_value:.2f}', next_predicted_color, f'{next_max_value:.2f}'])

    columns = ['출원 번호', '색상1', '색상1 유사값', '색상2',
               '색상2 유사값']

    df = pd.DataFrame(csv_file, columns=columns)
    df.to_csv(f'csv/{datetime.today()}${number_of_image_files}.csv', index=False)


# predicted_color #예측된 색상카테고리
predict_color_by_cv2()
