from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from models import Show

WAIT_MS = 10000


def fetch_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        print("Opening page...")
        page.goto(url, wait_until="networkidle")

        print("Waiting...")
        page.wait_for_timeout(WAIT_MS)

        html = page.content()

        browser.close()

        return html


def fetch_shows(url: str):
    html = fetch_html(url)

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("div[role='gridcell']")

    shows = []

    for card in cards:

        title = card.select_one("a.sc-1412vr2-2")
        if not title:
            continue

        language = card.select_one("a.sc-1412vr2-5")
        fmt = card.select_one("span.sc-1412vr2-6")

        movie_name = title.get_text(strip=True)

        language_name = (
            language.get_text(strip=True)
            if language else ""
        )

        format_name = (
            fmt.get_text(strip=True)
            .replace(",", "")
            .strip()
            if fmt else ""
        )

        buttons = card.select("div[aria-label^='Book']")

        for button in buttons:

            time = button.select_one("span.sc-yr56qh-1")

            screen = button.select_one("span.sc-yr56qh-2")

            if not time:
                continue

            shows.append(
                Show(
                    movie=movie_name,
                    language=language_name,
                    format=format_name,
                    theatre="",
                    screen=screen.get_text(strip=True) if screen else "",
                    date="",
                    time=time.get_text(strip=True),
                )
            )

    return shows


def main():

    URL = (
        "https://in.bookmyshow.com/cinemas/"
        "hyderabad/prasads-multiplex-hyderabad/"
        "buytickets/PRHN/20260804"
    )

    shows = fetch_shows(URL)

    print(f"\nFound {len(shows)} showtimes\n")

    for show in shows:
        print(show)


if __name__ == "__main__":
    main()