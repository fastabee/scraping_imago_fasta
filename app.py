import requests
from bs4 import BeautifulSoup
import csv

def scrape_detik(query, max_pages=3):
    base_url = "https://www.detik.com/search/searchall?query=politik"
    results = []

    for page in range(1, max_pages + 1):
        params = {"query": query, "sortby": "time", "page": page}
        try:
            response = requests.get(base_url, params=params, timeout=10)
            print(f"\n🔍 Fetching page {page} | URL: {response.url} | Status: {response.status_code}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

      
        articles = soup.select("article")
        print(f"👉 Jumlah article ketemu di page {page}: {len(articles)}")

        

        for idx, article in enumerate(articles, 1):
            try:
                title_tag = article.select_one(".media__title a")
                title = title_tag.get_text(strip=True) if title_tag else None
                link = title_tag["href"] if title_tag else None

                img_tag = article.select_one("img")
                image = img_tag["src"] if img_tag else None

                body_tag = article.select_one(".media__subtitle")
                body = body_tag.get_text(strip=True) if body_tag else None

                time_tag = article.select_one(".media__date")
                pub_time = time_tag.get_text(strip=True) if time_tag else None

                print(f"   {idx}. [DEBUG] title: {title}, link: {link}, image: {image}, time: {pub_time}")

                if title and link:
                    results.append({
                        "title": title,
                        "link": link,
                        "image": image,
                        "body": body,
                        "pub_time": pub_time
                    })
            except Exception as e:
                print(f"⚠️ Error parsing article: {e}")
                continue

    return results

if __name__ == "__main__":
    query = "politik"  
    data = scrape_detik(query)

    print("\n=== HASIL AKHIR ===")
    for i, d in enumerate(data, 1):
        print(f"{i}. {d['title']}")
        print(f"   📰 {d['body']}")
        print(f"   🕒 {d['pub_time']}")
        print(f"   📷 {d['image']}")
        print(f"   🔗 {d['link']}\n")

save_csv = input("simpan hasil ke CSV? (y/n): ").strip().lower()
if save_csv == "y":
        filename = f"hasil_scraping_{query}.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "body", "pub_time", "image", "link"])
            writer.writeheader()
            writer.writerows(data)
        print(f" Data berhasil disimpan ke {filename}")
