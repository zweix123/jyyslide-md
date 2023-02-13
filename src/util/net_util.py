import requests


def down_image(img_url, save_file_path):
    resp = requests.get(img_url)
    with open(save_file_path, "wb") as f:
        f.write(resp.content)
