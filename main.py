from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://www.kalx.berkeley.edu/on-the-air/schedule/")

    # Get the iframe with the schedule
    schedule_frame = next(
        frame for frame in page.frames if "spinitron" in frame.url
    )

    schedule_frame.wait_for_selector(".fc-content", timeout=10000)

    # Get all the program blocks
    program_blocks = schedule_frame.query_selector_all(".fc-content")

    print(f"Found {len(program_blocks)} program blocks.")

    # For each, print the time and program title
    for i, block in enumerate(program_blocks[:10]):  # limit to first 10 for now
        time_div = block.query_selector(".fc-time")
        title_div = block.query_selector(".fc-text")
        start_time = time_div.get_attribute("data-start") if time_div else "N/A"
        full_time = time_div.get_attribute("data-full") if time_div else "N/A"
        title = title_div.inner_text().strip() if title_div else "N/A"
        print(f"{i+1}: {start_time} | {full_time} | {title}")