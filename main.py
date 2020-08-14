import requests
from tqdm import tqdm
import config
import argparse


class Deep:
    def __init__(self, key: str, url: str, image: int, path="./"):
        self.key = key
        self.url = url
        self.image = image
        self.fileext = image.split('.')[-1]
        self.path = path

    def get_image(self):
        image = open(self.image, 'rb')
        return image

    def request(self):
        r = requests.post(self.url,
                          files={'image': self.get_image()},
                          headers={'api-key': self.key})
        return r

    def get_url(self):
        r = self.request()
        image_json = r.json()
        return image_json["output_url"], image_json["id"]

    def download(self):
        json = self.get_url()
        url = json[0]
        name = json[1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f"{self.path}{name}.{self.fileext}", "wb+") as f:
                for chunk in tqdm(r.iter_content(chunk_size=8192)):
                    if chunk:
                        f.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="File name")
    args = parser.parse_args()
    if args.f is not None:
        IMAGE = args.f
        deep = Deep(config.KEY, config.URL, IMAGE, 'images/')
        deep.download()
