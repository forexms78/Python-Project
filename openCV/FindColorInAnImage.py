import cv2
import numpy as np
import os

def find_color_in_an_image(lower_dic, upper_dic, src_path, img_file, pixel_dic):
    for color, values in lower_dic.items():
        img = cv2.imdecode(np.fromfile(os.path.join(src_path, img_file), dtype=np.uint8),
                           cv2.IMREAD_UNCHANGED)

        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

            lower_color = np.array(values)
            upper_color = np.array(upper_dic[color])

            mask_range = cv2.inRange(img_hsv, lower_color, upper_color)

            num_color_pixels = np.count_nonzero(mask_range)
            num_pixels = img.shape[0] * img.shape[1]
            selected_color_percentage = (num_color_pixels / num_pixels) * 100
            pixel_dic[color] = selected_color_percentage

    return pixel_dic
