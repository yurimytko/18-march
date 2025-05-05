from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def setup_browser():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(options=options)

def close_popups(browser):
    try:
        close_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label, 'Закрити') or contains(@aria-label, 'Close')]"))
        )
        close_btn.click()
        time.sleep(2)
    except:
        pass 

def scroll_page(browser, scroll_times=3, delay=3):
    for _ in range(scroll_times):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

def extract_posts_data(browser, max_posts=5):
    posts_data = []
    post_blocks = browser.find_elements(By.XPATH, "//div[contains(@class, 'x1yztbdb')]")

    for post in post_blocks[:max_posts]:
        post_info = {
            "post_url": None,
            "content": None,
            "date": None
        }

        try:
            link = post.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]")
            post_info["post_url"] = link.get_attribute("href").split('?')[0]
        except:
            pass

        try:
            text_div = post.find_element(By.XPATH, ".//div[@data-ad-comet-preview='message']//div[@dir='auto']")
            post_info["content"] = text_div.text.strip()
        except:
            pass

        try:
            date_span = post.find_element(By.XPATH, ".//span[contains(@class, 'x4k7w5x')]")
            post_info["date"] = date_span.text.strip()
        except:
            pass

        posts_data.append(post_info)

    return posts_data

def save_as_jsonl(data, filename="facebook_posts.jsonl"):
    with open(filename, "w", encoding="utf-8") as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write("\n")
def run_parser(page_url, limit=5):
    browser = setup_browser()
    try:
        browser.get(page_url)
        time.sleep(5)
        close_popups(browser)
        scroll_page(browser, scroll_times=4)
        posts = extract_posts_data(browser, max_posts=limit)
        save_as_jsonl(posts)
        print(f"Успішно збережено {len(posts)} постів у JSONL.")
    finally:
        browser.quit()

if __name__ == "__main__":
    run_parser("https://www.facebook.com/providentrealestateuz", limit=5)
