from playwright.sync_api import sync_playwright

CINEMA_URL = (
    "https://in.bookmyshow.com/cinemas/"
    "hyderabad/prasads-multiplex-hyderabad/"
    "buytickets/PRHN/20260804"
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening page...")
    page.goto(CINEMA_URL, wait_until="networkidle")

    print("Waiting 10 seconds...")
    page.wait_for_timeout(10000)

    print("\n===== PAGE TITLE =====")
    print(page.title())

    html = page.content()

    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nSaved page.html ({len(html)} bytes)")

    print("\nSearching for keywords...")

    for keyword in [
        "Spider-Man",
        "The Odyssey",
        "showtime",
        "PRHN",
        "buytickets",
        "available",
    ]:
        print(f"{keyword}: {keyword.lower() in html.lower()}")

    input("\nPress Enter to close...")

    browser.close()