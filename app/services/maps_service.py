import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "HealthChatbotApp/1.0",
}


async def get_nearby_hospitals(latitude: float, longitude: float, radius: int = 10000):
    """
    Fetch nearby hospitals using OpenStreetMap's Nominatim search API
    (free, no API key required).
    """

    # Build a bounding box around the user's location (~0.1 degrees ~ 10km)
    delta = 0.1
    left = longitude - delta
    right = longitude + delta
    top = latitude + delta
    bottom = latitude - delta

    params = {
        "q": "hospital",
        "format": "json",
        "limit": 5,
        "bounded": 1,
        "viewbox": f"{left},{top},{right},{bottom}",
        "addressdetails": 1,
    }

<<<<<<< HEAD
    for url in OVERPASS_URLS:
        try:
            async with httpx.AsyncClient(timeout=60, headers=HEADERS) as client:
                # Use data= (form-encoded dict) instead of content= so httpx
                # properly URL-encodes the query AND sets
                # Content-Type: application/x-www-form-urlencoded.
                # Sending raw content= without this header is what causes
                # the 406 Not Acceptable from overpass-api.de.
                response = await client.post(url, data={"data": query})
                response.raise_for_status()
                data = response.json()
                print(
                    f"Overpass success from {url}, elements found: {len(data.get('elements', []))}"
                )
                break  # success, stop trying other mirrors
        except Exception as e:
            print(f"Overpass error from {url}: {type(e).__name__}: {e!r}")
            continue

    if data is None:
=======
    try:
        async with httpx.AsyncClient(timeout=20, headers=HEADERS) as client:
            response = await client.get(NOMINATIM_URL, params=params)
            response.raise_for_status()
            results = response.json()
            print(f"Nominatim success, results found: {len(results)}")
    except Exception as e:
        print(f"Nominatim error: {type(e).__name__}: {e!r}")
>>>>>>> 4cc834047ebb76a3c2a8dce3baf7a79f83a3557b
        return []

    hospitals = []

    for place in results:
        name = place.get("display_name", "Unknown Hospital").split(",")[0]
        address = place.get("display_name", "Address not available")
        lat = place.get("lat")
        lon = place.get("lon")

        maps_url = (
            f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}"
        )

        hospitals.append(
            {
                "name": name,
                "address": address,
                "rating": None,
                "maps_url": maps_url,
            }
        )

    return hospitals