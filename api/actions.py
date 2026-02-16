from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()
YAC_URL = "http://localhost:8080"


@router.post("/api/sync_progress")
def sync_progress(library_id: int, comic_id: int, page: int):
    """
    Updates the reading progress on the YACReader server using the V1/V2 update route.
    """
    try:
        # Based on the C++ source: /library/ID/comic/ID/update
        # Note: We use V1 or V2 depending on your server version
        target_url = f"{YAC_URL}/library/{library_id}/comic/{comic_id}/update"

        # The C++ code splits postData by newlines and looks for 'currentPage'
        # We mimic the exact format YACReader expects
        payload = f"currentPage:{page}\nread:0"

        response = requests.post(target_url, data=payload)

        if response.status_code == 200:
            return {"status": "success", "synced_page": page}
        else:
            raise HTTPException(
                status_code=response.status_code, detail="Server rejected update"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/get_download_link")
def get_download_link(library_id: int, comic_id: int):
    """
    Returns the direct link to the comic file for 'Importing'.
    """
    # Based on: /library/ID/comic/ID/
    return {"download_url": f"{YAC_URL}/library/{library_id}/comic/{comic_id}/file"}
