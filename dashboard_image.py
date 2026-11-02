from pydoc import text

from PIL import Image, ImageDraw, ImageFont

from dashboard import get_dashboard_data, get_selected_date

WIDTH = 600
HEIGHT = 448

OUTPUT_FILE = "dashboard.png"

CLOUD_FILE = "weather_icons/cloud.jpg"
RAIN_HEAVY_FILE = "weather_icons/rain_heavy.jpg"
RAIN_LIGHT_FILE = "weather_icons/rain_light.jpg"
RAIN_SUN_FILE = "weather_icons/rain_sun.jpg"
SUN_FILE = "weather_icons/sun.jpg"
NIGHT_FILE = "weather_icons/night.jpg"
NIGHT_RAIN_FILE = "weather_icons/night_rain.jpg"

def load_font(size, bold=False):
    if bold:
        font_paths = [
            "arialbd.ttf",
            "segoeuib.ttf",
            "DejaVuSans-Bold.ttf",
            "FreeSansBold.ttf",
            "LiberationSans-Bold.ttf",
            "NotoSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        ]
    else:
        font_paths = [
            "arial.ttf",
            "segoeui.ttf",
            "DejaVuSans.ttf",
            "FreeSans.ttf",
            "LiberationSans-Regular.ttf",
            "NotoSans-Regular.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        ]

    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue

    raise RuntimeError(
        "No scalable TTF font found. Install DejaVu, FreeFont, Liberation, or Noto fonts."
    )


def wrap_text_to_width(draw, text, font, max_width):
    wrapped_lines = []

    for paragraph in text.splitlines() or [text]:
        words = paragraph.split()

        if not words:
            wrapped_lines.append("")
            continue

        current_line = words[0]

        for word in words[1:]:
            candidate = "{} {}".format(current_line, word)
            candidate_bbox = draw.textbbox((0, 0), candidate, font=font)
            candidate_width = candidate_bbox[2] - candidate_bbox[0]

            if candidate_width <= max_width:
                current_line = candidate
            else:
                wrapped_lines.append(current_line)
                current_line = word

        wrapped_lines.append(current_line)

    return "\n".join(wrapped_lines)

def get_weather_icon(condition, time, sunrise, sunset):
    """Return the appropriate weather icon based on actual sunrise/sunset."""

    current_minutes = (
        int(time.split(":")[0]) * 60
        + int(time.split(":")[1])
    )

    sunrise_minutes = (
        int(sunrise.split(":")[0]) * 60
        + int(sunrise.split(":")[1])
    )

    sunset_minutes = (
        int(sunset.split(":")[0]) * 60
        + int(sunset.split(":")[1])
    )

    is_night = (
        current_minutes < sunrise_minutes
        or current_minutes > sunset_minutes
    )

    rain_conditions = (
        "Light drizzle",
        "Drizzle",
        "Heavy drizzle",
        "Light rain",
        "Rain",
        "Heavy rain",
        "Light showers",
        "Showers",
        "Heavy showers",
    )

    # Night-time weather
    if is_night:
        if condition in rain_conditions:
            return NIGHT_RAIN_FILE

        return NIGHT_FILE

    # Day-time weather
    if condition in ("Clear sky", "Mainly clear"):
        return SUN_FILE

    if condition == "Partly cloudy":
        return RAIN_SUN_FILE

    if condition == "Overcast":
        return CLOUD_FILE

    if condition in (
        "Light drizzle",
        "Drizzle",
        "Light rain",
    ):
        return RAIN_LIGHT_FILE

    if condition in (
        "Heavy drizzle",
        "Rain",
        "Heavy rain",
        "Light showers",
        "Showers",
        "Heavy showers",
    ):
        return RAIN_HEAVY_FILE

    return CLOUD_FILE

def create_dashboard_image(data):
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    # title_font = load_font(28)
    # heading_font = load_font(22)
    normal_font = load_font(18)
    mid_x = WIDTH // 2

    # Vertical divider between left and right halves.
    draw.line((mid_x, 0, mid_x, HEIGHT), fill="red", width=2)

    # News
    news_font = load_font(14, bold=False)
    news_x = 20
    news_y = 20

    for news_item in data["news"]:
        news_text = wrap_text_to_width(
            draw,
            news_item["title"],
            news_font,
            270
        )

        draw.multiline_text(
            (news_x, news_y),
            news_text,
            fill="black",
            font=news_font,
            spacing=3
        )

        news_y += 58



    # Day of the year
    day_of_year_text = str(int(data["date"].split("-")[-2]))

    draw.text(
        (316, 22),
        "{} day".format(
            day_of_year_text
        ),
        fill="black",
        font=load_font(18)
    )

    # Year
    year_text = str(int(data["date"].split("-")[-3]))

    draw.text(
        (544, 22),
        "{}".format(
            year_text
        ),
        fill="black",
        font=load_font(18)
    )
    sunset_time = data["weather"][0]["sunset"]
    sunrise_time = data["weather"][0]["sunrise"]

    #  Sunset and sunrise times
    draw.text(
        (316, 54),
        "Sunrise: {}".format(
            sunrise_time
        ),
        fill="black",
        font=load_font(14)
    )
    draw.text(
        (498, 54),
        "Sunset: {}".format(
            sunset_time
        ),
        fill="black",
        font=load_font(14)
    )

    right_half_center_x = mid_x + (WIDTH - mid_x) // 2

    # Month
    month_text = data["month"].upper()

    month_font = load_font(22)
    month_bbox = draw.textbbox((0, 0), month_text, font=month_font)
    month_width = month_bbox[2] - month_bbox[0]
    month_x = right_half_center_x - month_width // 2

    draw.text(
        (month_x, 20),
        "{}".format(
            month_text
        ),
        fill="black",
        font=load_font(22, bold=True)
    )

    # Day of month
    day_text = str(int(data["date"].split("-")[-1]))

    day_font = load_font(118, bold=True)
    day_bbox = draw.textbbox((0, 0), day_text, font=day_font)
    day_width = day_bbox[2] - day_bbox[0]
    day_x = right_half_center_x - day_width // 2

    day_color = "red" if data["weekday"].upper() == "SUNDAY" else "black"

    draw.text(
        (day_x, 105),
        day_text,
        fill=day_color,
        font=day_font
    )

    # Weekday
    weekday_text = data["weekday"].upper()

    weekday_font = load_font(22)
    weekday_bbox = draw.textbbox((0, 0), weekday_text, font=weekday_font)
    weekday_width = weekday_bbox[2] - weekday_bbox[0]
    weekday_x = right_half_center_x - weekday_width // 2

    draw.text(
        (weekday_x, 230),
        "{}".format(
            weekday_text
        ),
        fill="black",
        font=load_font(22, bold=True)
    )

    # Imieniny
    imieniny_text = data["imieniny"]
    imieniny_font = load_font(18, bold=True)
    imieniny_bbox = draw.textbbox((0, 0), imieniny_text, font=imieniny_font)
    imieniny_width = imieniny_bbox[2] - imieniny_bbox[0]
    imieniny_x = right_half_center_x - imieniny_width // 2

    draw.text(
        (imieniny_x, 265),
        imieniny_text,
        fill="black",
        font=imieniny_font
    )

    # Advice
    draw.text(
        (460, 410),
        "Advice of the day",
        fill="black",
        font=load_font(14)
    )

    advice_font = load_font(14)

    draw.multiline_text(
        (mid_x + 40, 350),
        wrap_text_to_width(draw, data["advice"], advice_font, 230),
        fill="black",
        font=advice_font,
        spacing=4
    )

    x = 20
    y = 260

    counter = 0;



    for weather in data["weather"]:

        # Weather illustration
        weather_image = Image.open(
            get_weather_icon(
                weather["condition"],
                weather["time"],
                weather["sunrise"],
                weather["sunset"]
            )
        ).convert("RGBA")


        text_time = "{}".format(
            weather["time"],
        )

        text_degrees = "{}°C".format(
            round(weather["temperature"]),
        )

        if counter > 4:
            y += 100
            x = 20
            counter = 0

        # Draw time
        draw.text(
            (x, y),
            text_time,
            fill="black",
            font=normal_font
        )

        # draw icon
        image.paste(weather_image, (x, y + 20), weather_image)

        # Draw degrees
        draw.text(
            (x, y + 60),
            text_degrees,
            fill="black",
            font=normal_font
        )


        x +=50
        counter += 1

    return image


if __name__ == "__main__":
    selected_date = get_selected_date()
    data = get_dashboard_data(selected_date)

    image = create_dashboard_image(data)
    image.save(OUTPUT_FILE)

    print("Dashboard image created:", OUTPUT_FILE)
