import httpx

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (HealthChatbot/1.0; contact: your-email@example.com)",
    "Accept": "*/*",
}


async def get_nearby_hospitals(latitude: float, longitude: float, radius: int = 10000):
    """
    Fetch nearby hospitals using OpenStreetMap's Overpass API (free, no API key required).
    Tries multiple Overpass mirrors as fallback.
    """

    query = (
        f"[out:json][timeout:25];"
        f"("
        f'node["amenity"="hospital"](around:{radius},{latitude},{longitude});'
        f'way["amenity"="hospital"](around:{radius},{latitude},{longitude});'
        f'relation["amenity"="hospital"](around:{radius},{latitude},{longitude});'
        f");"
        f"out center 5;"
    )

    data = None

    for url in OVERPASS_URLS:
        try:
            async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
                response = await client.post(url, content=f"data={query}")
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
        return []

    hospitals = []

    for element in data.get("elements", [])[:5]:
        tags = element.get("tags", {})
        name = tags.get("name", "Unnamed Hospital")

        address_parts = [
            tags.get("addr:housenumber"),
            tags.get("addr:street"),
            tags.get("addr:city"),
        ]
        address = ", ".join([p for p in address_parts if p]) or "Address not available"

        if element["type"] == "node":
            lat = element.get("lat")
            lon = element.get("lon")
        else:
            center = element.get("center", {})
            lat = center.get("lat")
            lon = center.get("lon")

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
