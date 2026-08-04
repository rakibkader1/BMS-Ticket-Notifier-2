import os

from bs4 import BeautifulSoup
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from models import Show
from url_parser import parse_cinema_url, theatre_name_from_slug


HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"


def fetch_html(url: str) -> str:
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=HEADLESS
        )

        page = browser.new_page()

        try:

            print("Opening page...")
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            print("Waiting for showtimes...")

            page.wait_for_selector(
                "div[role='gridcell']",
                timeout=15000,
            )

            html = page.content()

            browser.close()

            return html

        except PlaywrightTimeoutError:

            browser.close()

            print("Timed out waiting for BookMyShow.")

            return ""

        except Exception as e:

            browser.close()

            print(f"Playwright error: {e}")

            return ""


def fetch_shows(url: str):

    info = parse_cinema_url(url)

    theatre = theatre_name_from_slug(
        info["theatre_slug"]
    )

    date = info["date"]

    html = fetch_html(url)

    if not html:
        return []

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    cards = soup.select(
        "div[role='gridcell']"
    )

    shows = []

    for card in cards:

        title = card.select_one(
            "a.sc-1412vr2-2"
        )

        if not title:
            continue

        language = card.select_one(
            "a.sc-1412vr2-5"
        )

        fmt = card.select_one(
            "span.sc-1412vr2-6"
        )

        movie_name = title.get_text(
            strip=True
        )

        language_name = (
            language.get_text(strip=True)
            if language
            else ""
        )

        format_name = (
            fmt.get_text(strip=True)
            .replace(",", "")
            .strip()
            if fmt
            else ""
        )

        buttons = card.select(
            "div[aria-label^='Book']"
        )

        for button in buttons:

            time = button.select_one(
                "span.sc-yr56qh-1"
            )

            if not time:
                continue

            screen = button.select_one(
                "span.sc-yr56qh-2"
            )

            shows.append(
                Show(
                    movie=movie_name,
                    language=language_name,
                    format=format_name,
                    theatre=theatre,
                    screen=(
                        screen.get_text(strip=True)
                        if screen
                        else "Unknown"
                    ),
                    date=date,
                    time=time.get_text(strip=True),
                )
            )

    return shows


if __name__ == "__main__":

    from config import get_bms_url

    shows = fetch_shows(get_bms_url())

    print(f"\nFound {len(shows)} showtimes\n")

    for show in shows:
        print(show)