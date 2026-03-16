import os
import pickle
from mastodon import Mastodon
from random import shuffle
from dotenv import load_dotenv

initial = [
    'Nosferatu.jpg',
    'Nosferatu-2.jpg',
    'Rozz Williams.jpg',
    'She Past Away.jpg',
    'The Cure 1980.jpg',
    'The Vampire Lovers (1970).jpg',
    'The Vampire Lovers (1970)-2.jpg',
    'Vincent Price - The Raven.jpg'
]


def post(image):
    media_file = "./imgs/" + image
    print("posting " + image)
    media_ids = mastodon.media_post(
        media_file=media_file,
        mime_type="image/jpg"
    )
    mastodon.status_post(
        status=image + "\n" + "#goth",
        media_ids=media_ids,
    )


def save_last(img_list):
    last = open("last", "wb")
    pickle.dump(img_list, last)
    last.close()


def load_last():
    file = open("last", "rb")
    last = pickle.load(file)
    file.close()
    return last


def is_repeated(img):
    if not (os.path.isfile("last")):
        last = initial
    else:
        last = load_last()

    return img in last


def get_img():
    img_dir = "imgs/"
    img_list = os.listdir(img_dir)
    shuffle(img_list)
    while is_repeated(img_list[0]):
        shuffle(img_list)

    return img_list


def main():
    img_list = get_img()
    post(img_list[0])
    save_last(img_list)


if __name__ == "__main__":
    load_dotenv()
    mastodon = Mastodon(
        access_token=os.getenv("ACCESS_TOKEN"),
        api_base_url='https://mastodon.social'
    )
    main()
