import asyncio
from playwright.async_api import async_playwright
import time
import os

async def capture_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Configure viewport to 3:2 ratio (1500 x 1000) for Devpost
        context = await browser.new_context(
            viewport={"width": 1500, "height": 1000}
        )
        page = await context.new_page()
        
        print("Navigating to SuperApp for screenshots...")
        await page.goto("http://127.0.0.1:8000")
        
        # 1. Capture Nominal State
        print("Letting chart populate (5s)...")
        await asyncio.sleep(5)
        print("Capturing Nominal State...")
        path1 = os.path.join("docs", "gallery_1_nominal.png")
        await page.screenshot(path=path1)
        print(f"Saved {path1}")
        
        # 2. Trigger Simulation
        print("Clicking simulate button...")
        await page.click("#btn-simulate")
        
        # 3. Capture AI Reasoning state mid-way
        await asyncio.sleep(4)
        print("Capturing AI Reasoning State...")
        path2 = os.path.join("docs", "gallery_2_ai_reasoning.png")
        await page.screenshot(path=path2)
        print(f"Saved {path2}")
        
        # 4. Capture Final Triggered State
        print("Waiting for final hospital reservation...")
        await asyncio.sleep(4)
        print("Capturing Final Orchestrated State...")
        path3 = os.path.join("docs", "gallery_3_orchestrated.png")
        await page.screenshot(path=path3)
        print(f"Saved {path3}")
        
        await context.close()
        await browser.close()
        print("All screenshots captured successfully in 3:2 ratio.")

if __name__ == "__main__":
    asyncio.run(capture_screenshots())
