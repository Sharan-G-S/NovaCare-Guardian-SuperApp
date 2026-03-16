import asyncio
from playwright.async_api import async_playwright
import time
import os

async def record_demo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Configure video recording directory
        context = await browser.new_context(
            record_video_dir="docs/",
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        print("Navigating to SuperApp...")
        await page.goto("http://127.0.0.1:8000")
        
        # Initial state observation
        print("Recording baseline telemetry...")
        await page.mouse.move(300, 300) # Hover left
        await asyncio.sleep(5)
        await page.mouse.move(960, 540) # Hover center
        await asyncio.sleep(4)
        
        # Triggering the simulation
        print("Clicking simulate button...")
        await page.click("#btn-simulate")
        
        # Watching the system respond
        print("Recording AI response and hospital orchestration...")
        await page.mouse.move(1600, 500) # Hover right
        await asyncio.sleep(20) # Wait for all animations and logs to finish
        
        # Save video
        video = await page.video.path()
        await context.close()
        await browser.close()
        
        # Rename video to a friendly name
        final_path = os.path.join("docs", "novacare_superapp_demo.webm")
        if os.path.exists(final_path):
             os.remove(final_path)
        os.rename(video, final_path)
        print(f"Video saved successfully to {final_path}")

if __name__ == "__main__":
    asyncio.run(record_demo())
