from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://www.kalx.berkeley.edu/on-the-air/schedule/")

    schedule_frame = next(
        frame for frame in page.frames if "spinitron" in frame.url
    )

    schedule_frame.wait_for_selector(".fc-content", timeout=10000)

    # Look for date headers (they may be in .fc-day-header)
    headers = schedule_frame.query_selector_all(".fc-day-header")

    print(f"Found {len(headers)} headers:")
    for h in headers:
        print(h.inner_text().strip())

    input("Press Enter to close browser...")
    browser.close()