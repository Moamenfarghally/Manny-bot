# debug_pinterest.py
import aiohttp, asyncio, re, sys, html

SEARCH = "cat"   # change to test other queries

async def main():
    url = f"https://www.pinterest.com/search/pins/?q={SEARCH.replace(' ', '%20')}"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=15) as resp:
                status = resp.status
                text = await resp.text()
        except Exception as e:
            print("REQUEST ERROR:", e)
            return

    print("STATUS:", status)
    print("LENGTH OF HTML:", len(text))
    print("FIRST 1000 CHARS:\n", text[:1000].replace("\n"," ") )
    # save to file to open in browser
    with open("pinterest_debug.html", "w", encoding="utf-8") as f:
        f.write(text)
    print("\nSaved full HTML to pinterest_debug.html")

    # find pinimg urls
    pinimgs = re.findall(r'https://i\.pinimg\.com/[^\"\'\s<>]+', text)
    base64s = re.findall(r'data:image/[a-zA-Z0-9]+;base64,([^\"\'\s<>]+)', text)
    print("Found pinimg count:", len(pinimgs))
    print("Found base64 images count:", len(base64s))
    if pinimgs:
        print("Sample pinimg urls (first 5):")
        for u in pinimgs[:5]:
            print(" ", u)

if __name__ == "__main__":
    asyncio.run(main())
