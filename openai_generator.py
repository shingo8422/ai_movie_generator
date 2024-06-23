from openai import OpenAI
import random
import json
import os


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def story_generator(context_id):

    topics = [
        "科学の不思議",
        "歴史の面白い事実",
        "世界の珍しい食べ物",
        "動物の驚くべき習性",
        "宇宙の謎",
        "技術の進化",
        "日常生活の裏技",
        "世界の奇妙な風習",
        "有名人の意外な一面",
        "スポーツの歴史と記録",
        "健康とフィットネスの豆知識",
        "言葉の由来",
        "世界の名所・観光地",
        "音楽の歴史とトリビア",
        "映画の裏話",
        "アートとデザインの豆知識",
        "経済とビジネスの基礎知識",
        "心理学の面白い事実",
        "テクノロジーのトリビア",
    ]

    random_topic = random.choice(topics)
    content = f"""
    Youtubeで役立つ豆知識や雑学を解説するYoutubeショートムービーを作成しようと思っています。

    そのための台本を作成してください。
    言語は日本語でお願いします。
    
    豆知識、雑学のジャンルは、「{random_topic}」でお願いします。

    Storyは１つだけピックアップし、Chapterを３つに分けて解説してください。
    Chapterを３つに分ける理由は、章ごとにふさわしい画像を用意するためです。

    画像は、生成AIで作成するので、
    生成AIで作成するためのプロンプトも一緒に出力してください。

    image_promptは英語でお願いします。

    titleにジャンルを使わないでください。
    titleには、Storyの内容を簡潔に表すテキストを格納してください。

    出力の形式は、Jsonで
    ```
    {{
        "title": "xxx",
        "chapter_1": "yyyy",
        "chapter_1_image_prompt": "xxx yyy zzz aaaa",
        "chapter_2": "yyyy",
        "chapter_2_image_prompt": "xxx yyy zzz aaaa",
        "chapter_3": "yyyy",
        "chapter_3_image_prompt": "xxx yyy zzz aaaa"
    }}
    ```

    という形式で出力してください。

    それぞれのchapterは１０秒程度で話せる量にしてください。
    chapter_1,chapter_2,chapter_3には、それぞれのチャプターのタイトルではなく、
    解説自体を入れてください。
    """

    print(f"topic: {random_topic}, context_id: {context_id}")

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {"role": "user", "content": content},
        ],
    )

    story_metadata = json.loads(response.choices[0].message.content)
    print(f"metadata: {str(story_metadata)}, context_id: {context_id}")
    return story_metadata


def image_generator(prompt, context_id):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    download_url = response.data[0].url
    print(f"image: {download_url}, prompt: {prompt}, context_id: {context_id}")
    return download_url
