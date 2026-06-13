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

    try:
        async with httpx.AsyncClient(timeout=20, headers=HEADERS) as client:
            response = await client.get(NOMINATIM_URL, params=params)
            response.raise_for_status()
            results = response.json()
            print(f"Nominatim success, results found: {len(results)}")
    except Exception as e:
        print(f"Nominatim error: {type(e).__name__}: {e!r}")
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
