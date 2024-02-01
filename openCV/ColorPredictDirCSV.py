from config import HSV_lower_color_dic, HSV_upper_color_dic, HSV_gray_lower_color_dic, \
    HSV_gray_upper_color_dic
from datetime import datetime
from FindColorInAnImage import find_color_in_an_image
from Extract2SimilarColors import extract_2_similar_colors

import pandas as pd
import os


def color_prediction_for_folders():
    src_path = '../../../../PycharmProjects/pythonProject2/img2/10000img'
    file_list = os.listdir(src_path)

    is_threshold = True
    threshold = 0.01

    maximum_value = 90

    csv_file = []
    cnt = 0

    number_of_image_files = 0

    if number_of_image_files == 0:
        number_of_image_files = len(file_list)

    for img_file in file_list[:number_of_image_files]:
        cnt += 1
        print(f' [{cnt}/{number_of_image_files}] img_file: {img_file}')
        if img_file == '.DS_Store':
            os.remove(src_path + '/' + img_file)
            continue
        else:
            pixel_dic = {}

            find_color_in_an_image(lower_dic=HSV_lower_color_dic, upper_dic=HSV_upper_color_dic, src_path=src_path,
                                   img_file=img_file, pixel_dic=pixel_dic)
            primary_color, primary_color_value, secondary_color, secondary_color_value, sorted_items = extract_2_similar_colors(
                pixel_dic=pixel_dic)

            if primary_color_value <= threshold:

                keep_primary_color, keep_primary_value = primary_color, primary_color_value

                find_color_in_an_image(lower_dic=HSV_gray_lower_color_dic, upper_dic=HSV_gray_upper_color_dic,
                                       src_path=src_path, img_file=img_file, pixel_dic=pixel_dic)

                primary_color, primary_color_value, secondary_color, secondary_color_value, sorted_items = extract_2_similar_colors(
                    pixel_dic=pixel_dic)

                if primary_color_value > keep_primary_value:
                    secondary_color, secondary_color_value = keep_primary_color, keep_primary_value

            if primary_color_value < threshold and secondary_color_value < threshold:
                find_color_in_an_image(lower_dic=HSV_gray_lower_color_dic, upper_dic=HSV_gray_upper_color_dic,
                                       src_path=src_path, img_file=img_file, pixel_dic=pixel_dic)

                primary_color, primary_color_value, secondary_color, secondary_color_value, sorted_items = extract_2_similar_colors(
                    pixel_dic=pixel_dic)

            if primary_color_value > maximum_value and primary_color == '검정':
                primary_color = secondary_color
                primary_color_value = secondary_color_value

                if not sorted_items:
                    continue
                else:
                    secondary_color = sorted_items[2][0]
                    secondary_color_value = sorted_items[2][1]

            if is_threshold:
                if secondary_color_value < threshold:
                    secondary_color = '그 외'
                    secondary_color_value = 0

                if primary_color_value < threshold:
                    primary_color = '그 외'
                    primary_color_value = 0
                    secondary_color = '그 외'
                    secondary_color_value = 0

            csv_file.append([img_file, primary_color, f'{primary_color_value:.2f}', secondary_color,
                             f'{secondary_color_value:.2f}'])

    columns = ['img_file', 'primary_color', 'primary_color_value', 'secondary_color', 'secondary_color_value']

    sorted_csv_file = sorted(csv_file, key=lambda x: x[0])

    df = pd.DataFrame(sorted_csv_file, columns=columns)
    df.to_csv(f'csv/{datetime.today()}${number_of_image_files}.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    # predicted_color #예측된 색상카테고리
    color_prediction_for_folders()
