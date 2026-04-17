import os
import pickle
from mastodon import Mastodon
from random import shuffle
from dotenv import load_dotenv

initial = [
    # initial filenames
]


def post(filename):
    media_file = "./imgs/" + filename
    media_ids = mastodon.media_post(
        media_file=media_file,
        mime_type="image/jpg"
    )
    tags = "#goth"
    image_name = filename.split('.')[0]
    print("posting " + image_name)
    mastodon.status_post(
        status=image_name + "\n" + tags,
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


def get_last():
    if not (os.path.isfile("last")):
        last = initial
    else:
        last = load_last()
    return last


def is_repeated(img):
    last = get_last()
    return img in last


def get_img():
    img_dir = "imgs/"
    img_list = os.listdir(img_dir)
    shuffle(img_list)
    while len(img_list) > 0 and is_repeated(img_list[0]):
        print("shuffling image list")
        shuffle(img_list)

    return img_list


def main():
    img_list = get_img()
    post(img_list[0])
    print('adding ' + img_list[0] + ' to posted list\n')
    last = get_last()
    last.append(img_list[0])
    print('posted list:' + ",".join(last))
    save_last(last)


if __name__ == "__main__":
    load_dotenv()
    mastodon = Mastodon(
        access_token=os.getenv("ACCESS_TOKEN"),
        api_base_url='https://mastodon.social'
    )
    main()
