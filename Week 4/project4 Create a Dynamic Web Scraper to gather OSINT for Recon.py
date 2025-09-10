import requests
from bs4 import BeautifulSoup
import csv

class GeneralWebScraper:
    def print_website_content_csv(self, url, output_file="Project_4_CIS226.csv"):
        
        if not url.startswith(("http://", "https://")):
            url = "http://" + url   # site uses http

        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            page = requests.get(url, headers=headers)
            page.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return

        soup = BeautifulSoup(page.content, "html.parser")

        # Extract name
        name_tag = soup.find("h2")
        name = name_tag.get_text().split(":")[1].strip() if name_tag else "N/A"

        # Find profile details by searching for text strings
        def get_value(label):
            element = soup.find(string=lambda text: text and label in text)
            if element:
                return element.split(":")[1].strip()
            return "N/A"

        favorite_animal = get_value("Favorite animal")
        favorite_color = get_value("Favorite color")
        hometown = get_value("Hometown")

        # Save to CSV with semicolon delimiter (Excel-friendly for your locale)
        with open(output_file, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Name", "Favorite Animal", "Favorite Color", "Hometown"])
            writer.writerow([name, favorite_animal, favorite_color, hometown])

        print(f"Profile data saved to {output_file}")

if __name__ == "__main__":
    #url = input("Enter the URL to scrape (leave blank for default page): ").strip()
    #if not url:
    url = "http://olympus.realpython.org/profiles/aphrodite"

    scraper = GeneralWebScraper()
    scraper.print_website_content_csv(url, output_file="Project_4_CIS226.csv")

