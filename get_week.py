from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.kalx.berkeley.edu/on-the-air/schedule/")

    # Wait for the iframe to load
    page.wait_for_selector("iframe")
    iframe_element = page.query_selector("iframe")
    iframe = iframe_element.content_frame()

    print("🔎 Looking for all .fc-content blocks...")
    blocks = iframe.query_selector_all(".fc-content")
    print(f"Found {len(blocks)} blocks.\n")

    for i, block in enumerate(blocks):
        time_el = block.query_selector(".fc-time")
        dj_el = block.query_selector(".fc-text")

        time_str = time_el.inner_text() if time_el else "??"
        dj_name = dj_el.inner_text() if dj_el else "??"

        box = block.bounding_box()
        if box:
            print(
                f"#{i + 1:02d} ▶ ({box['x']:.1f}, {box['y']:.1f}) w={box['width']:.1f} h={box['height']:.1f} | {time_str} | {dj_name}")
        else:
            print(f"#{i + 1:02d} ▶ No bounding box found | {time_str} | {dj_name}")

    input("\nPress Enter to close browser...")
    browser.close()