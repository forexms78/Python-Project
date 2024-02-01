import requests
import xmltodict
import os

for page_number in range(55, 1500):
    # Create url (including input value and KEY value) with updated pageNo
    url4 = (
        "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch?"
        "applicationDate=20220101~20231231"
        "&application=true"
        "&registration=true"
        "&refused=true"
        "&expiration=true"
        "&withdrawal=true"
        "&publication=true"
        "&cancel=true"
        "&abandonment=true"
        "&character=false"
        "&figure=true"
        "&compositionCharacter=false"
        "&figureComposition=true"
        "&fragrance=false"
        "&sound=false"
        "&color=false"
        "&colorMixed=false"
        "&dimension=false"
        "&hologram=false"
        "&invisible=false"
        "&motion=false"
        "&visual=false"
        "&numOfRows=500"
        f"&pageNo={page_number}"
        "&ServiceKey=JRz2glirBuZs1jlxrcAuLeG6DXGsb8GeDb700KdBxSs="
    )

    # REST API call
    response = requests.get(url4)

    print(f"Processing page number: {page_number}")

    # Check the call result
    content = response.content

    # Change XML format to DICT (dictionary) format
    dict_type = xmltodict.parse(content)

    common_folder = 'logo'
    if not os.path.exists(common_folder):
        os.makedirs(common_folder)

    folder_path = os.path.join(common_folder, f'logoImage_{page_number}')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    items = dict_type.get('response', {}).get('body', {}).get('items', {}).get('item', [])

    for i, item in enumerate(items):
        logo_img_path = item.get('bigDrawing', '')
        logo_number = item.get('applicationNumber', '')

        if logo_img_path and logo_number:
            file_path = os.path.join(folder_path, f'{logo_number}.jpg')

            try:
                with open(file_path, 'wb') as f:
                    f.write(requests.get(logo_img_path).content)
                print(f"Downloaded image {i + 1}: {file_path}")
            except Exception as e:
                print(f"Error downloading image {i + 1}: {e}")