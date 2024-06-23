import json
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
from PIL import Image, ImageDraw, ImageFont
import textwrap


def create_text_clip(
    text,
    font_path,
    fontsize,
    color,
    size,
    duration,
    start_time,
    outline_color="white",
    outline_width=3,
):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, fontsize)

    lines = textwrap.wrap(text, width=20)
    y_text = 0
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((size[0] - text_width) // 2, y_text)

        for adj in range(outline_width):
            draw.text(
                (text_position[0] - adj, text_position[1]),
                line,
                font=font,
                fill=outline_color,
            )
            draw.text(
                (text_position[0] + adj, text_position[1]),
                line,
                font=font,
                fill=outline_color,
            )
            draw.text(
                (text_position[0], text_position[1] - adj),
                line,
                font=font,
                fill=outline_color,
            )
            draw.text(
                (text_position[0], text_position[1] + adj),
                line,
                font=font,
                fill=outline_color,
            )

        draw.text(text_position, line, font=font, fill=color)
        y_text += text_height

    img.save("temp_text.png")

    text_clip = (
        ImageClip("temp_text.png")
        .set_duration(duration)
        .set_position(("center", 300))
        .set_start(start_time)
    )
    return text_clip


def resize_image(image_path, new_width, new_height):
    with Image.open(image_path) as img:
        resized_image = img.resize((new_width, new_height))
        resized_image.save(image_path)


def add_subtitles_and_images(context_id, font_path):
    # ファイルパスの設定
    video_path = f"./movies/{context_id}/did_movie.mp4"
    metadata_path = f"./movies/{context_id}/story_metadata.json"
    output_path = f"./movies/{context_id}/output_movie.mp4"

    # 字幕データの読み込み
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    title = metadata["title"]
    chapters = [
        {
            "text": metadata["chapter_1"],
            "image": f"./movies/{context_id}/chapter_1_image.png",
        },
        {
            "text": metadata["chapter_2"],
            "image": f"./movies/{context_id}/chapter_2_image.png",
        },
        {
            "text": metadata["chapter_3"],
            "image": f"./movies/{context_id}/chapter_3_image.png",
        },
    ]

    # 動画の読み込み
    video = VideoFileClip(video_path)
    video_duration = video.duration
    chapter_duration = (video_duration - 2) / 3

    # 画像のリサイズと配置
    for chapter in chapters:
        resize_image(chapter["image"], 512, 400)

    clips = []

    # 元動画を下部に移動
    video = video.set_position(("center", "bottom"))
    clips.append(video)

    # タイトルの追加
    title_clip = create_text_clip(
        title,
        font_path,
        fontsize=28,
        color="black",
        size=(512, 400),
        duration=2,
        start_time=2,
    )
    clips.append(title_clip.set_start(0))

    # 各チャプターの画像とテキストの追加
    for i, chapter in enumerate(chapters):
        start_time = 2 + i * chapter_duration

        image_clip = (
            ImageClip(chapter["image"])
            .set_duration(chapter_duration)
            .set_position(("center", "top"))
            .set_start(start_time)
        )

        text_clip = create_text_clip(
            chapter["text"],
            font_path,
            fontsize=24,
            color="black",
            size=(512, 400),
            duration=chapter_duration,
            start_time=start_time,
        )

        clips.append(image_clip)
        clips.append(text_clip)

    # 新しい解像度に合わせてコンポジット
    final_clip = CompositeVideoClip(clips, size=(512, 1024))
    final_clip.write_videofile(output_path, codec="libx264", fps=24)
