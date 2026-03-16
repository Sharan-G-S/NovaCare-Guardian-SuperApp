import asyncio
from playwright.async_api import async_playwright
import os

async def generate_pdf():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Determine strict absolute path for HTML file
        base_path = os.path.dirname(os.path.abspath(__file__))
        html_path = f"file://{os.path.join(base_path, 'docs/submission_document.html')}"
        
        print(f"Loading document: {html_path}")
        await page.goto(html_path, wait_until="networkidle")
        
        # Save as PDF
        pdf_path = os.path.join(base_path, 'docs/NovaCare_Guardian_Project.pdf')
        print("Generating Professional PDF...")
        await page.pdf(
            path=pdf_path,
            format="Letter",
            print_background=True, # crucial for gradients and colors
            margin={"top": "0in", "right": "0in", "bottom": "0in", "left": "0in"}
        )
        
        await browser.close()
        print(f"PDF successfully saved to: {pdf_path}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
