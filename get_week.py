from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.kalx.berkeley.edu/on-the-air/schedule/")

    # Find the iframe
    frames = page.frames
    for frame in frames:
        print(f"FRAME: {frame.url}")
    iframe = next(f for f in frames if "spinitron" in f.url)

    # ✅ Wait for day headers inside iframe
    print("Waiting for .fc-day-header in iframe...")
    iframe.wait_for_selector(".fc-day-header")
    headers = iframe.query_selector_all(".fc-day-header")

    # Map day/date labels to x-coordinates
    day_columns = {}
    for header in headers:
        text = header.inner_text().strip()
        box = header.bounding_box()
        if box:
            day_columns[text] = box["x"]

    print("\n📅 Day columns with x positions:")
    for label, x in day_columns.items():
        print(f"  {label}: x={x:.1f}")

    # ✅ Also fetch show blocks as a test
    print("\nLooking for all .fc-content blocks...")
    blocks = iframe.query_selector_all(".fc-content")
    print(f"Found {len(blocks)} blocks.\n")

    for i, block in enumerate(blocks, 1):
        box = block.bounding_box()
        time_range = block.query_selector(".fc-time") or block.query_selector(".fc-title")
        title = block.query_selector(".fc-title")
        start_end = time_range.inner_text().strip() if time_range else "?"
        show = title.inner_text().strip() if title else "?"
        print(f"#{i:02d} ▶ ({box['x']:.1f}, {box['y']:.1f}) w={box['width']:.1f} h={box['height']:.1f} | {start_end} | {show}")

    # Sort day labels by x position (left to right)
    sorted_days = sorted(day_columns.items(), key=lambda x: x[1])

    # Prepare structure to group shows by day
    shows_by_day = {label: [] for label, _ in sorted_days}

    # Assign each show block to the nearest day column
    for block in blocks:
        box = block.bounding_box()
        if not box:
            continue

        x = box["x"]
        time_el = block.query_selector(".fc-time")
        title_el = block.query_selector(".fc-title")
        time_range = time_el.inner_text().strip() if time_el else "?"
        title = title_el.inner_text().strip() if title_el else "?"

        # Find the nearest column (x distance)
        closest_day = min(sorted_days, key=lambda item: abs(item[1] - x))[0]
        shows_by_day[closest_day].append((box["y"], time_range, title))

    # ✅ Print shows grouped by day
    print("\n📆 Schedule grouped by day:\n")
    for day, shows in shows_by_day.items():
        print(f"--- {day} ---")
        shows_sorted = sorted(shows, key=lambda s: s[0])  # Sort by vertical position (time)
        for _, time_range, title in shows_sorted:
            print(f" {time_range:<15} {title}")
        print()

    input("\nPress Enter to close browser...")
    browser.close()