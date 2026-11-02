from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


RSS_URL = "https://feeds.skynews.com/feeds/rss/uk.xml"

FALLBACK_NEWS = [
    {
        "title": "News temporarily unavailable"
    },
    {
        "title": "Please check the internet connection"
    },
    {
        "title": "Dashboard is still working normally"
    }
]


def get_news():
    """Return the latest three headlines from Sky News UK RSS."""

    try:
        request = Request(
            RSS_URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urlopen(request, timeout=10) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        news = []

        for item in root.findall(".//item"):
            title_element = item.find("title")

            if title_element is None:
                continue

            title = title_element.text

            if not title:
                continue

            title = title.strip()

            news.append({
                "title": title
            })

            if len(news) >= 3:
                break

        if news:
            return news

        return FALLBACK_NEWS

    except Exception as error:
        print("News download failed:", error)
        return FALLBACK_NEWS


if __name__ == "__main__":
    for item in get_news():
        print(item)