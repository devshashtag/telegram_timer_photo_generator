# telegram api
from telethon.sync import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateProfileRequest
# image edit
from PIL import Image, ImageFont, ImageDraw
# datetime by timezone
from pytz import timezone
from datetime import datetime

import time
import os

import config


def main():
    with TelegramClient(config.session_name,
                        config.api_id,
                        config.api_hash,
                        proxy=config.proxy) as client:
        # default images before screen runs on you'r account
        profile_images_length = len(client.get_profile_photos('me'))
        print("default images: ", profile_images_length)

        while True:
            #print(get_second())
            # each 0 second upload new time image to profile and
            # remove old generated timer images
            if get_second() == 0:
                # get current time Asia/Tehran
                time_now = get_current_time()
                # count length profile images
                profile_images_current_length = len(client.get_profile_photos('me'))
                # delete all timer images
                while profile_images_length < profile_images_current_length:
                    print(f'image {profile_images_current_length} deleted .')
                    # delete last profile image
                    client(DeletePhotosRequest([client.get_profile_photos('me')[0]]))
                    # count length profile images
                    profile_images_current_length = len(client.get_profile_photos('me'))

                # set image to profile
                print(f"image set at: {time_now}")
                # generate profile image with time
                profile_img_generator(time_now)
                # upload image to telegram
                image = client.upload_file(config.image_filename)
                # set to profile image
                client(UploadProfilePhotoRequest(image))

                # delete local image after set
                delete_timer()
            # 1 second wait
            time.sleep(1)

def profile_img_generator(time):
    """ generate profile image with time """
    image = Image.open(config.photo_filename)
    W, H = image.size
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font=config.font, size=config.font_size)
    w, h = draw.textsize(time, font=font)

    draw.text(((W - w) /2, (H - h)/2), time, font=font, fill=config.image_text_color)

    image.save(config.image_filename)

def delete_timer():
    """ remove generated profile image from disk"""
    os.remove(config.image_filename)

def get_current_time():
    """ get timezone Asia/Tehran hour:minute """
    return datetime.now(timezone('Asia/Tehran')).strftime('%H:%M')

def get_second():
    """ get timezone Asia/Tehran second """
    return datetime.now(timezone('Asia/Tehran')).second

if __name__ == '__main__':
    main()
