from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup

router = APIRouter()

YAC_URL = "http://localhost:8080"


def get_yac_items(path: str):
    """Parses a YACReader page and returns a structured list of items."""
    try:
        response = requests.get(f"{YAC_URL}{path}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        items = []
        container_items = soup.select("#itemContainer li")

        for li in container_items:
            title_div = li.select_one(".title p")
            title = title_div.text.strip() if title_div else "Unknown"

            browse_tag = li.select_one(".browseButton")
            read_tag = li.select_one(".readButton")

            if browse_tag:
                img_tag = li.select_one(".folder img")
                items.append(
                    {
                        "title": title,
                        "thumbnail": f"{YAC_URL}{img_tag['src']}" if img_tag else None,
                        "path": browse_tag["href"],
                        "type": "folder",
                    }
                )
            elif read_tag:
                img_tag = li.select_one(".cover img")
                pages = li.select_one(".numPages")
                size = li.select_one(".comicSize")
                items.append(
                    {
                        "title": title,
                        "thumbnail": f"{YAC_URL}{img_tag['src']}" if img_tag else None,
                        "path": read_tag["href"],
                        "type": "comic",
                        "metadata": {
                            "pages": pages.text.strip() if pages else None,
                            "size": size.text.strip() if size else None,
                        },
                    }
                )

        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/folders")
def folders(path: str):
    """Lists folders within a library or parent folder."""
    items = get_yac_items(path)
    return {"current_path": path, "items": items}


@router.get("/api/comics")
def comics(path: str):
    """Lists comics within a folder."""
    items = get_yac_items(path)
    return {"current_path": path, "items": items}
