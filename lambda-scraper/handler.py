import json
import os

from scraper import Scraper


def scrape(event, context):
    driver = Scraper()
    page = driver.scrape_page('https://waitbutwhy.com/')

    # Business logic for specific scrape job
    post = page.find("div", {"class": "mainPost"})
    header = post.find("h1")
    link = header.find('a', href=True)

    if link:
        data = {
            "success": "true",
            "result": {
                "message": "Congrats!! Your Headless Chrome initialized and we found the top story on Wait But Why",
                "topStoryLink": link['href']
            }
        }
    else :
        data = {
            "success": "false",
            "result": {
                "message": "Oops, something went wrong"
            }
        }

    driver.close();
    driver.quit();

    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response
