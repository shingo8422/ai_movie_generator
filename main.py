from openai_generator import story_generator, image_generator
from did_generator import create_talk, get_talk
from merge_img_and_subtitle_to_movie import add_subtitles_and_images
import random
import time
import os
import requests
import json


def download_file(url, file_name):
    directory = os.path.dirname(file_name)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully: {file_name}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def save_json_data(data: dict, file_name):
    directory = os.path.dirname(file_name)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    context_id = str(random.randint(0, 99999999999))

    metadata = story_generator(context_id=context_id)

    chapter_1_image_download_url = image_generator(
        metadata["chapter_1_image_prompt"], context_id=context_id
    )
    chapter_2_image_download_url = image_generator(
        metadata["chapter_2_image_prompt"], context_id=context_id
    )
    chapter_3_image_download_url = image_generator(
        metadata["chapter_3_image_prompt"], context_id=context_id
    )

    input = metadata["title"] + "。"

    input = input + metadata["chapter_1"]
    input = input + metadata["chapter_2"]
    input = input + metadata["chapter_3"]

    create_talk_response = create_talk(input=input, name=metadata["title"])

    while True:
        talk = get_talk(create_talk_response["id"])
        if talk["status"] == "done":
            print(talk)
            break
        time.sleep(5)

    download_file(talk["result_url"], f"./movies/{context_id}/did_movie.mp4")

    download_file(
        chapter_1_image_download_url, f"./movies/{context_id}/chapter_1_image.png"
    )
    download_file(
        chapter_2_image_download_url, f"./movies/{context_id}/chapter_2_image.png"
    )
    download_file(
        chapter_3_image_download_url, f"./movies/{context_id}/chapter_3_image.png"
    )

    save_json_data(metadata, f"./movies/{context_id}/story_metadata.json")

    add_subtitles_and_images(context_id, font_path="./fonts/NotoSansJP-Bold.ttf")
