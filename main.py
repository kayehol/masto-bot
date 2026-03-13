import os
import pickle
from mastodon import Mastodon
from random import shuffle
from dotenv import load_dotenv


def post(image):
    media_file = "./imgs/" + image
    print("posting " + media_file)
    media_ids = mastodon.media_post(
        media_file=media_file,
        mime_type="image/jpg"
    )
    mastodon.status_post(
        status=image + "\n" + "#goth",
        media_ids=media_ids,
    )


def save_last(img):
    last = open("last", "wb")
    pickle.dump(img, last)
    last.close()


def load_last():
    file = open("last", "rb")
    last = pickle.load(file)
    file.close()
    return last


def is_repeated(img):
    if not (os.path.isfile("last")):
        return False

    last = load_last()
    if (type(last) is not str) or (type(img) is not str):
        print("last or current img is not a string")

    return img == last


def get_img():
    img_dir = "imgs/"
    img_list = os.listdir(img_dir)
    shuffle(img_list)
    if is_repeated(img_list[0]):
        shuffle(img_list)

    return img_list[0]


def main():
    img = get_img()
    post(img)
    save_last(img)


if __name__ == "__main__":
    load_dotenv()
    mastodon = Mastodon(
        access_token=os.getenv("ACCESS_TOKEN"),
        api_base_url='https://mastodon.social'
    )
    main()
