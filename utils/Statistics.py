import pandas as pd
import csv

def check_car(records: list, startingDate: int, endingDate: int, search_query: str):
    if not records:
        print("⚠️ No records to process.")
        return

    df = pd.DataFrame(records)
    
    # Check that necessary columns exist
    for col in ["Year", "Price", "KM"]:
        if col not in df.columns:
            df[col] = None
    
    # Filter year and price
    auto = df[(df["Year"] >= startingDate) & (df["Year"] <= endingDate)]
    auto = auto[auto["Price"].notna() & (df["Price"] != 0)].copy()
    
    if not auto.empty:
        print(f"{search_query} ({startingDate}-{endingDate})")
        print("Count:", len(auto))
        print("Min Price (KM):", auto["Price"].min())
        print("Max Price (KM):", auto["Price"].max())
        print("Avg Price (KM):", int(auto["Price"].mean()))

        # 1000KM
        auto["Price_per_k_km"] = auto.apply(
            lambda row: row["Price"] / (row["KM"] / 1000) if row["KM"] and row["KM"] != 0 else None,
            axis=1
        )

        sorted_auto = auto.sort_values("Price_per_k_km", na_position='last')[
            ["Title", "Year", "KM", "Price", "Price_per_k_km", "Link"]
        ]

        #CSV
        output_file = search_query.lower().replace(" ", "-") + "-auto.csv"
        sorted_auto.to_csv(output_file, index=False, encoding="utf-8")
        print(f"✅ Results saved to {output_file}")

    else:
        print(f"⚠️ No cars found for {search_query} in the specified range.")
