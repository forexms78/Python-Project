1. 색상 데이터 추출
   1. 파일명 : ColorExtract.ipynb
   2. 함수명: : all_copy_with_sub_folder
   3. 파라미터 설명:
      - color_data_path : 추출된 색상이미지들이 저장될 폴더경로 
      - src_dir : 추출한 이미지원본 파일들의 폴더경로
      - EACH_VIENNA_MAX : 추출할 이미지들 최대수량
      - thresohold: 추출할 색상의 비율이 몇%까지인지 지정
      - match_category: 추출할 색상카테고리 지정
   4. 함수 호출
      ``` python
      def all_copy_with_sub_folder(color_data_path = 'COLOR_TRAIN', 
             src_dir = '/Users/bhpark/Documents/dev/git/public/[원천]상표이미지_train',
             EACH_VIENNA_MAX = 10000,
             threshold = 10,  
             match_category = '초록',      
             ): 
      ```
      
2. 색상 예측
   1. 파일명: ColorPredict_ipynb
   2. 함수명: predict_color_by_cv2
   3. 파리미터 설명
      - src_path: 예측할 이미지 샘플경로
      - file: 예측할 이미지샘플명
      - return값:
       ``` python
      predicted_color #예측된 색상카테고리
       ```
      
   4. 함수 호출:
      ``` python
      predict_color_by_cv2(
      src_path = 'sample_total_41893',
      file = '010102 4020170002140 모던 단순 빨강 빨강.jpg')
      ```
      
3. yolo 학습 데이타 추출 및 학습
   1. vaild txt make:
      1. 파일명:1,2.ipynb
      2. 함수명: make_yolo_format_by_json_information
      3. 파라미터 설명
         - src_path: 카테고별 json 라벨 파일폴더 경로
         - IMR_DIR: 카테고리별 이미지 파일폴더 경로
         - dst_path: box정보 txt 파일폴더 경로
         - mapping_path: 맵핑 txt파일 경로
         - is_subfolder_exist: src_path 폴더에 sub폴더들이 있는지 여부
         - MAX_CATEGORY_COUNT: 각 카테고리별 샘플추출 수량 최대치
         - value_key_reverseL value, key를 서로 변경할지 여부
      4. 함수호출:
      ``` python
        def make_yolo_format_by_json_information(src_path = '[라벨]상표이미지_valid',
                                 IMG_DIR = '[원천]상표이미지_valid',
                                 dst_path='valid',
                                 mapping_path = 'mapping.txt',
                                 is_subfolder_exist = True,
                                 MAX_CATEGORY_COUNT = 5000, #샘플수량 <= each_category_count
                                 value_key_reverse = True):
                     
         ```
      2. train txt make:
         - 1. 과 동일한 함수 호출 파라미터 값만 변경
      ``` python
        def make_yolo_format_by_json_information(src_path = '[라벨]상표이미지_train',
                                 IMG_DIR = '[원천]상표이미지_train',
                                 dst_path='train',
                                 mapping_path = 'mapping.txt',
                                 is_subfolder_exist = True,
                                 MAX_CATEGORY_COUNT = 25000, #샘플수량 <= each_category_count
                                 value_key_reverse = True):
      ```
      3. vaild 브랜빕샘플 겹치는 txt 삭제
         1. 파일명: 3,4.ipynb
         2. 함수명: make_yolo_format_by_json_information
         3. 파라미터 설명
            - src_path: 브랜빕샘플(41893) 폴더 경로
            - compare_path: 비교할 폴더가 train 인지 vaild 인지 설정
            - output_file: 브랜빕샘플리스트 txt 파일저장경로
            - output_file2: 브랜빕샘플과 중복되는 샘플리스트 txt 파일저장경로
         4. 함수호출:
            ``` python
            get_branvip_sample_name_list_and_remove_overlaped_list(
               src_path = 'sample_total_41893',
               compare_path = 'vaild',
               output_file = '브랜빕샘플리스트.txt',
               output_file2 = '브랜빕샘플중복리시트_valid.txt'
            )
            ```
      4. train 브랜빕 샘플 겹치는 txt 삭제
         - 3. 과 동일한 함수호출 파라미터 값만 변경
           ```python
           get_branvip_sample_name_list_and_remove_overlaped_list(
               src_path = 'sample_total_41893',
               compare_path = 'train'
               output_file = '브랜빕샘플리스트.txt',
               output_file = '브랜빕샘플중복리스트_train.txt'
           )
           ```
           
      5. vaild image make
      
         5-1) 파일명: 5,6.ipynb
         5-2) 함수명: yolo_copy_jph_by_txt
         5-3) 파라미터 설명
            - src_path: 카테고리별 박스정보 txt파일의 원본이미지가 있는 폴더경로
            - dst_path: 카테고리별 박스정보 txt파일의 원본이미지를 저장할 폴더경로
         4) 함수호출:
         ```python
         yolo_copy_jpg_by_txt(
            src_path = '[원천]상표이미지.vaild',
            dst_path = 'valid'
         )
         ```
         
         6) train image make
            - 5) 와 동일한 함수호출 파라미터값만 변경
            ```python
            yolo_copy_jpg_by_txt(
                src_path = '[원천]상표이미지_train',
                dst_path = 'train'
            )
            ```
            
         7) vaild 중복 image 삭제
            7-1) 파일명: 7,9.ipynb
            7-2) 함수명: yolo_overlapped_image_remove
            7-3) 파라미터 설명
               - image_folder: 중복이미지 제거할 폴더경로
               - overlapped_txt_path: 중복 이미지 리스트 txt 파일 저장경로
         - 
            7-4) 함수호출 :
            
         ```python
            yolo_overlapped_image_remove(image_folder = 'valid',
                            overlapped_txt_path = 
         'overlappedlist_valid.txt')
         ```
         