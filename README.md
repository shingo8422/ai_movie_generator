## What's ai_movie_generator ??

The ai_movie_generator is a program that automatically generates short movies of about 30 seconds using the following three services:

- [OpenAI GPT-4](https://openai.com/index/hello-gpt-4o/)
- [OpenAI Dall-E 3](https://openai.com/index/dall-e-3/)
- [Eleven Labs](https://elevenlabs.io/)
- [D-ID](https://www.d-id.com/)

and the [moviepy](https://github.com/Zulko/moviepy) library.

## How to Use

```
# step 1
cp env.example cp

# step 2
# set variables to env
# OPENAI_API_KEY=<can use gpt-4o api key>
# DID_BASIC_TOKEN=read page -> https://docs.d-id.com/reference/basic-authentication#%EF%B8%8F-generating-your-api-key
# DID_SOURCE_IMAGE_URL=<your avator image url>
# ELEVEN_LABS_TOKEN=<eleven labs api key>
# ELEVEN_LABS_VOICE_ID=<eleven labs custom voice id>


# step 3
docker compose up -d

# step 4
docker compose exec app /bin/bash

# step 5
python main.py

# Movie generated to ./movies direcotory.
```

## Prompt Customize

Please edit openai_generator.py.  

## Sample Generated Movies

- [エッフェル塔の知られざる歴史](https://www.youtube.com/shorts/U_12sopVNIY)
- [スマートフォンの進化](https://www.youtube.com/shorts/gsL_66MWPpU)
