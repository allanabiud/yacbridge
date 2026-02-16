from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()
YAC_URL = "http://localhost:8080"


def parse_yac_metadata(raw_text: str):
    """Parses YACReader's custom key:value text format into a dictionary."""
    metadata = {}
    lines = raw_text.strip().split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


@router.get("/api/comic_info")
def get_comic_info(path: str):
    """
    Fetches detailed metadata for a specific comic.
    Example path: /library/1/comic/2/remote
    """
    try:
        response = requests.get(f"{YAC_URL}{path}")
        response.raise_for_status()

        raw_data = response.text
        comic_data = parse_yac_metadata(raw_data)

        # Convert comma-separated string fields into actual JSON lists
        list_fields = [
            "characters",
            "teams",
            "locations",
            "coverArtist",
            "penciller",
            "inker",
            "editor",
        ]
        for field in list_fields:
            if field in comic_data and comic_data[field]:
                comic_data[field] = [
                    item.strip() for item in comic_data[field].split(",")
                ]

        return comic_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
