from playwright.sync_api import sync_playwright
import time
import logging
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

# ----- CONFIG -----
TELEGRAM_TOKEN = "8228282267:AAGIE8REqpab6oCH0fCyoAkIy4KbyN6y8us"
TELEGRAM_CHAT_ID = 1651045216   # Your numeric Telegram user ID here!
FIRSTCRY_URL = "https://www.firstcry.com/hotwheels/5/0/113?sort=popularity&q=ard-hot%20wheels&ref2=q_ard_hot%20wheels&asid=53241#sale=5&brandid=113&searchstring=brand@@@@1@0@20@@@@@@@@@@@@@@@@@@@@@&rating=&sort=Rating&&vi=four&pmonths=&cgen=&skills=&measurement=&material=&curatedcollections=&Color=&Age=&gender=&ser=&premium=&deliverytype=&PageNo=1&scrollPos=0&pview=&tc=30"
CHECK_INTERVAL = 120  # seconds
DB_PATH = "hotwheels_db.json"
MAX_PAGES = 50        # Safety net: Stop if more than 50 pages

# ----- LOGGING -----
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ----- DB -----
db = TinyDB(DB_PATH)
Product = Query()

def send_telegram_message(product):
    text = (
        f"*{product['name']}*\n"
        f"Price: ₹{product['price']}\n"
        f"[View Product]({product['url']})"
    )
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": text,
            "photo": product['image'],
            "parse_mode": "Markdown"
        }
        resp = requests.post(url, data=data)
        if resp.ok:
            logging.info(f"Sent new product alert: {product['name']}")
        else:
            logging.error(f"Failed to send Telegram message: {resp.text}")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

def fetch_products():
    try:
        all_products = []
        seen_ids = set()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page_num = 1
            while page_num <= MAX_PAGES:
                page_url = FIRSTCRY_URL
                if "PageNo=" in page_url:
                    page_url = page_url.replace(
                        f"PageNo=1", f"PageNo={page_num}"
                    )
                else:
                    page_url += f"&PageNo={page_num}"
                page.goto(page_url, timeout=60000)
                page.wait_for_selector('div.list_block', timeout=20000)
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                items = soup.select('div.list_block')
                print(f"[Page {page_num}] Found {len(items)} product containers")

                page_products = []
                page_ids = set()
                for item in items:
                    name_tag = (
                        item.select_one('.li_txt1 a') or
                        item.select_one('.li_txt1')
                    )
                    name = name_tag.get('title') if name_tag and name_tag.get('title') else (name_tag.get_text(strip=True) if name_tag else "N/A")
                    link_tag = item.select_one('.li_txt1 a')
                    link = link_tag.get('href') if link_tag else ""
                    url = link if link.startswith('http') else "https://www.firstcry.com" + link
                    price_tag = item.select_one('.club-block .r1 a') or item.select_one('.rupee .r1 a')
                    price = price_tag.get_text(strip=True) if price_tag else "N/A"
                    img_tag = item.select_one('.list_img img')
                    image = (
                        ("https:" + img_tag.get('src')) if img_tag and img_tag.get('src') else
                        ("https:" + img_tag.get('data-src')) if img_tag and img_tag.get('data-src') else ""
                    )
                    prod_id = item.get('data-pid') or url

                    # De-duplicate across all pages
                    if prod_id in seen_ids:
                        continue
                    page_products.append({
                        "id": prod_id,
                        "name": name,
                        "url": url,
                        "price": price,
                        "image": image
                    })
                    page_ids.add(prod_id)

                # If no new unique products, stop (infinite loop protection)
                if not page_products:
                    print("No new unique products on this page; ending pagination.")
                    break

                all_products.extend(page_products)
                seen_ids.update(page_ids)
                page_num += 1

            browser.close()
        print(f"Total unique products parsed: {len(all_products)}")
        return all_products
    except Exception as e:
        logging.error(f"PLAYWRIGHT fetch failed: {e}")
        return []

def is_new_product(product_id):
    return len(db.search(Product.id == product_id)) == 0

def save_product(product):
    db.insert({"id": product['id'], "name": product['name'], "url": product['url']})

# --- TEST ALERT ---
send_telegram_message({
    "id": "test123",
    "name": "🔥 TEST ALERT: This is a fake Hot Wheels product!",
    "price": "999",
    "url": "https://www.firstcry.com/",
    "image": "https://cdn.fcglcdn.com/brainbees/images/products/219x265/20290035a.webp"
})

def main():
    logging.info("Hot Wheels monitor bot started.")
    while True:
        products = fetch_products()
        new_products = [p for p in products if is_new_product(p['id'])]
        for product in new_products:
            send_telegram_message(product)
            save_product(product)
        logging.info(f"Checked. New products: {len(new_products)}. Total seen: {len(db)}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
