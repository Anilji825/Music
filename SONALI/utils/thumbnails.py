from config import YOUTUBE_IMG_URL
from youtubesearchpython.__future__ import VideosSearch
async def get_qthumb(vidid):
    try:
        query = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception as e:
        return YOUTUBE_IMG_URL
        async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_v4.png"):
        return f"cache/{videoid}_v4.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)

    try:
        for result in (await results.next())["result"]:
            try:
                title = result.get("title", "Unsupported Title")
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"

            duration = result.get("duration", "Unknown Mins")
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")

            if "thumbnails" in result and len(result["thumbnails"]) > 0:
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            else:
                raise ValueError("Thumbnail not found in search results")

            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                            await f.write(await resp.read())

            youtube = Image.open(f"cache/thumb{videoid}.png")
            image1 = changeImageSize(1280, 720, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(20))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)
            draw = ImageDraw.Draw(background)
            arial = ImageFont.truetype("TanuMusic/assets/font2.ttf", 30)
            font = ImageFont.truetype("TanuMusic/assets/font.ttf", 30)
            title_font = ImageFont.truetype("TanuMusic/assets/font3.ttf", 45)

            circle_thumbnail = crop_center_circle(youtube, 400, 20)
            circle_thumbnail = circle_thumbnail.resize((400, 400))
            circle_position = (120, 160)
            background.paste(circle_thumbnail, circle_position, circle_thumbnail)

            text_x_position = 565

            title1 = truncate(title)
            draw.text((text_x_position, 180), title1[0], fill=(255, 255, 255), font=title_font)
            draw.text((text_x_position, 230), title1[1], fill=(255, 255, 255), font=title_font)
            draw.text((text_x_position, 320), f"{channel}  |  {views[:23]}", (255, 255, 255), font=arial)
            draw.text((10, 10), f"ʀᴀᴊᴀ ʙᴀʙᴜ", fill="BLUE", font=font)

            line_length = 580
            red_length = int(line_length * 0.6)
            white_length = line_length - red_length

            start_point_red = (text_x_position, 380)
            end_point_red = (text_x_position + red_length, 380)
            draw.line([start_point_red, end_point_red], fill="red", width=9)

            start_point_white = (text_x_position + red_length, 380)
            end_point_white = (text_x_position + line_length, 380)
            draw.line([start_point_white, end_point_white], fill="white", width=8)

            circle_radius = 10
            circle_position = (end_point_red[0], end_point_red[1])
            draw.ellipse([circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                          circle_position[0] + circle_radius, circle_position[1] + circle_radius], fill="red")
            draw.text((text_x_position, 400), "00:00", (255, 255, 255), font=arial)
            draw.text((1080, 400), duration, (255, 255, 255), font=arial)

            play_icons = Image.open("TanuMusic/assets/play_icons.png")
            play_icons = play_icons.resize((580, 62))
            background.paste(play_icons, (text_x_position, 450), play_icons)

            try:
                os.remove(f"cache/thumb{videoid}.png")
            except:
                pass
            background.save(f"cache/{videoid}_v4.png")
            return f"cache/{videoid}_v4.png"

    except Exception as e:
        print(f"Error in get_thumb: {e}")
        raise
        
