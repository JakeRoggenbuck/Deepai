import requests
from tqdm import tqdm
import argparse
import yaml


class Config:
    def __init__(self, path: str = "./config.yml"):
        self.path = path
        self.config = self.get_config()

    def get_config(self):
        config_file = open(self.path)
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config


class DeepImage:
    def __init__(self, style_name: str, input_file: str, output_file: str, style_image: str):
        self.input_file = input_file
        self.output_file = output_file
        self.style_name = style_name
        self.style_image = style_image
        self.config = Config()

    def read_image(self, image):
        return open(image, "rb")

    def get_url_by_style_name(self):
        for url_group in self.config.config["urls"]:
            if (url := url_group.get(self.style_name)):
                return url
        else:
            raise Exception("Choose one of these: ",
                            [[key for key in keys.keys()] for keys in self.config.config["urls"]])

    def request(self):
        if self.style_image is None:
            files = {"image": self.read_image(self.input_file)}
        else:
            files = {"content": self.read_image(self.input_file),
                     "style": self.read_image(self.style_image)}

        headers = {'api-key': self.config.config["key"]}
        response = requests.post(self.get_url_by_style_name(), files=files, headers=headers)
        return response

    def get_new_url(self):
        response = self.request()
        image_json = response.json()
        return image_json["output_url"], image_json["id"]

    def download(self):
        url, name = self.get_new_url()
        if self.output_file is not None:
            name = self.output_file
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(name, "wb+") as f:
                for chunk in tqdm(r.iter_content(chunk_size=8192)):
                    if chunk:
                        f.write(chunk)


def parser():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", help="Input file name")
    parse.add_argument("-o", help="Output file name")
    parse.add_argument("-s", help="Style Image")
    parse.add_argument("-n", help="Style name")
    return parse.parse_args()


if __name__ == "__main__":
    args = parser()
    deep = DeepImage(args.n, args.i, args.o, args.s)
    deep.download()
