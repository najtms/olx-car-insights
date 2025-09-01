import pandas as pd

def filter_records(records, startingDate, endingDate):
    if not records:
        return []

    df = pd.DataFrame(records)
    
    for col in ["Year", "Price", "KM","City"]:
        if col not in df.columns:
            df[col] = None

    filtered = df[(df["Year"] >= startingDate) & (df["Year"] <= endingDate)]
    filtered = filtered[filtered["Price"].notna() & (filtered["Price"] != 0)].copy()

    if not filtered.empty:
        filtered["Price_per_k_km"] = filtered.apply(
            lambda row: row["Price"] / (row["KM"] / 1000) if row["KM"] else None,
            axis=1
        )
    return filtered.to_dict(orient="records")