import requests
import json
import os

basic_token = os.environ.get("DID_BASIC_TOKEN")
eleven_labs_token = os.environ.get("ELEVEN_LABS_TOKEN")
eleven_labs_voice_id = os.environ.get("ELEVEN_LABS_VOICE_ID")
did_source_image_url = os.environ.get("DID_SOURCE_IMAGE_URL")


def get_talk(talk_id):
    url = f"https://api.d-id.com/talks/{talk_id}"

    headers = {"accept": "application/json", "authorization": f"Basic {basic_token}"}

    response = requests.get(url, headers=headers)

    return json.loads(response.text)


def create_talk(input, name):
    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "elevenlabs",
                "voice_id": eleven_labs_voice_id,
                "voice_config": {"stability": 1, "similarity_boost": 1},
            },
            "input": input,
        },
        "config": {"fluent": "false", "pad_audio": "0.0", "stitch": True},
        "source_url": did_source_image_url,
        "name": name,
    }
    headers = {
        "accept": "application/json",
        "x-api-key-external": '{"elevenlabs": "' + eleven_labs_token + '"}',
        "content-type": "application/json",
        "authorization": f"Basic {basic_token}",
    }

    response = requests.post(url, json=payload, headers=headers)

    data = json.loads(response.text)
    print(data)
    return data
