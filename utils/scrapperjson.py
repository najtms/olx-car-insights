import requests


def olxScraper(search_query: str, total_results: int):
    url = "https://olx.ba/api/search"  # Link for API Json Files
    headers = {"User-Agent": "Mozilla/5.0"}
    per_page = 300
    records = []

    num_pages = (total_results // per_page) + (1 if total_results % per_page else 0)
    print(f"total_results: {total_results}, per_page: {per_page}, num_pages: {num_pages}")
    for page in range(1, num_pages + 1):
        if page == num_pages and total_results % per_page != 0:
            current_per_page = total_results % per_page
        else:
            current_per_page = per_page
        print(f"Requesting page {page} with current_per_page {current_per_page}")

        params = {
            "q": search_query,
            "category_id": 1,
            "per_page": current_per_page,
            "page": page
        }

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
            data = res.json()
        except requests.RequestException as e:
            print("Issue with fetching Data", e)
            continue

        for item in data.get("data", []):
            price = item.get("display_price", "N/A")
            # Convert price to integer if possible
            price_value = item.get("price", None)

            fuel = kms = year = city = None
            for label in item.get("special_labels") or []:
                if label.get("label") == "Gorivo":
                    fuel = label.get("value")
                elif label.get("label") == "Kilometraža":
                    try:
                        kms = int(label.get("value").replace(".", "").strip())
                    except:
                        kms = None
                elif label.get("label") == "Godište":
                    year = int(label.get("value"))
            if kms is not None and (kms > 750_000 or kms < 5_000):
                continue
            if price_value < 200:
                continue

            city = item.get("city_id", None)

            records.append({  # Add to Records Obj
                "Title": item.get("title", ""),
                "Price": price_value,
                "Fuel": fuel,
                "KM": kms,
                "Year": year,
                "City": city,
                "Link": f"https://olx.ba/artikal/{item['id']}"
            })

    return records