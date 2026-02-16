from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup

router = APIRouter()

YAC_URL = "http://localhost:8080"


@router.get("/api/libraries")
def get_libraries():
    try:
        response = requests.get(YAC_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        libraries = []
        items = soup.select("#librariesList li")

        for item in items:
            name_element = item.find("div", class_="library-link")
            if not name_element:
                continue  # Skip this item if name isn't found

            name = name_element.text.strip()

            link_element = item.find("a")
            if not link_element or not link_element.has_attr("href"):
                continue  # Skip this item if link isn't found

            link = link_element["href"]

            libraries.append(
                {
                    "name": name,
                    "api_path": link,
                }
            )

        return {"libraries": libraries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
