import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import utils.Gemini as Gemini
import utils.Result_collecter as tr
import utils.scrapperjson as sj
import json
import utils.fr as fr  # filter_records module

# Remove old title and config (already set below)

# --- Page configuration ---
st.set_page_config(
    page_title="OLX Car Tracker",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Responsive CSS ---
st.markdown('''
<style>
@media (max-width: 600px) {
    .main-card, .feature-box, .footer {
        padding: 1rem !important;
        margin: 0.5rem auto !important;
        max-width: 98vw !important;
    }
    .landing-header { font-size: 2.1rem !important; }
    .landing-subheader { font-size: 1.1rem !important; }
    .feature-title { font-size: 1.05rem !important; }
    .feature-desc { font-size: 0.95rem !important; }
    .typing-bar { font-size: 0.95rem !important; }
    .footer { font-size: 0.85rem !important; }
}
.mode-btn-row {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin: 2.2rem 0 1.2rem 0;
}
.mode-btn {
    background: linear-gradient(90deg, #2D2D86 70%, #4e54c8 100%);
    color: #fff;
    border: none;
    border-radius: 2.2rem;
    font-size: 1.25rem;
    font-weight: 700;
    padding: 1.1rem 2.5rem;
    box-shadow: 0 2px 12px #e0e0e0;
    cursor: pointer;
    transition: background 0.18s, transform 0.12s;
    outline: none;
}
.mode-btn.selected, .mode-btn:active {
    background: linear-gradient(90deg, #4e54c8 60%, #2D2D86 100%);
    color: #fff;
    transform: scale(1.04);
    box-shadow: 0 4px 18px #bdbdbd;
}
</style>
''', unsafe_allow_html=True)



 # (Removed: Typing bar will be inside main-card)
st.markdown("""
<style>
.landing-header {
    font-size: 3.5rem;
    font-weight: 900;
    color: #2D2D86;
    text-align: center;
    margin-top: 1.5rem;
    letter-spacing: 2px;
    text-shadow: 1px 2px 8px #e0e0e0;
}
.landing-subheader {
    font-size: 1.5rem;
    color: #444;
    text-align: center;
    margin-bottom: 2rem;
    margin-top: 0.5rem;
}
.feature-box {
    background: linear-gradient(120deg, #f0f4ff 60%, #e6e6fa 100%);
    padding: 28px 18px 22px 18px;
    border-radius: 18px;
    text-align: center;
    margin: 12px;
    box-shadow: 0 2px 12px 0 #e0e0e0;
    transition: box-shadow 0.2s;
}
.feature-box:hover {
    box-shadow: 0 4px 24px 0 #bdbdbd;
}
.feature-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2D2D86;
    margin-bottom: 8px;
}
.feature-desc {
    font-size: 1.05rem;
    color: #333;
}
.footer {
    text-align: center;
    font-size: 1rem;
    color: #888;
    margin-top: 3rem;
    padding: 1.5rem;
}
.main-card {
    background: #fff;
    border-radius: 22px;
    box-shadow: 0 2px 16px 0 #e0e0e0;
    padding: 2rem 2rem 2rem 2rem;
    margin: 2rem auto 2rem auto;
    max-width: 900px;
}
.typing-bar {
    width: 120px;
    min-width: 100%;
    background: #181818;
    border-radius: 22px;
    color: #fff;
    font-family: 'Fira Mono', 'Consolas', monospace;
    font-size: 1.1rem;
    padding: 0.7rem 0 0.7rem 0;
    text-align: center;
    letter-spacing: 1px;
    border-bottom: 2px solid #2D2D86;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 100;
}
.typing-demo {
    display: inline-block;
    border-right: 1.5px solid #2D2D86;
    white-space: nowrap;
    overflow: hidden;
    font-family: 'Fira Mono', 'Consolas', monospace;
    font-size: 1.08rem;
    letter-spacing: 0.5px;
    animation: typing 3.2s steps(28, end), blink-caret 0.6s step-end infinite alternate;
    max-width: 100vw;
}
@keyframes typing {
    from { width: 0 }
    to { width: 22ch }
}
@keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: #2D2D86; }
}
</style>
""", unsafe_allow_html=True)


# -- # Landing Page # -- #
st.markdown('''
<div class="main-card">
<div class="typing-bar" style="position:relative; display:flex; align-items:center; justify-content:center;">
    <a href="https://github.com/najtms" target="_blank" style="position:absolute; left:18px; top:50%; transform:translateY(-50%); display:inline-flex; align-items:center; text-decoration:none;">
        <svg xmlns="http://www.w3.org/2000/svg" width="33" height="33" fill="#fff" viewBox="0 0 24 24" style="background:#2D2D86; border-radius:50%; padding:3px;"><path d="M21.707 20.293l-3.387-3.387A7.928 7.928 0 0 0 18 10a8 8 0 1 0-8 8 7.928 7.928 0 0 0 6.906-3.68l3.387 3.387a1 1 0 0 0 1.414-1.414zM4 10a6 6 0 1 1 6 6 6.006 6.006 0 0 1-6-6z"/></svg>
    </a>
    <span class="typing-demo" style="padding-left:2.5rem;">github.com/najtms</span>
</div>
    <div class="landing-header">OLX Car Tracker 🚗</div>
    <div class="landing-subheader">Find car listings, track prices, and explore trends easily!</div>
</div>
''', unsafe_allow_html=True)

# -- # Features # -- # 
st.markdown("""
<div style="margin-top:2rem; margin-bottom:1.5rem;">
    <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1.5rem;">
        <div class="feature-box" style="flex:1 1 220px; min-width:220px; max-width:270px;">
            <div class="feature-title">Real-Time Data</div>
            <div class="feature-desc">Get up-to-date listings from OLX automatically.</div>
        </div>
        <div class="feature-box" style="flex:1 1 220px; min-width:220px; max-width:270px;">
            <div class="feature-title">Smart Analysis</div>
            <div class="feature-desc">Analyze prices and trends to make informed decisions.</div>
        </div>
        <div class="feature-box" style="flex:1 1 220px; min-width:220px; max-width:270px;">
            <div class="feature-title">Easy to Use</div>
            <div class="feature-desc">Simple interface, just type a car model and start exploring.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)



st.markdown("""
<div style='text-align:center; margin-top:2.5rem; margin-bottom:2.5rem;'>
    <a href="#" style="background:#2D2D86; color:#fff; padding:0.85rem 2.2rem; border-radius:2rem; font-size:1.25rem; font-weight:600; text-decoration:none; box-shadow:0 2px 8px #e0e0e0; transition:background 0.2s;">Start Exploring Now</a>
</div>
""", unsafe_allow_html=True)


# -- # Usability # -- # 
col_guide, col_howmade = st.columns(2)
with col_guide:
    with st.expander("ℹ️ How to Use OLX Car Tracker", expanded=False):
        st.markdown("""
1. **Enter your desired car model** (e.g., Golf 4) and other details in the search fields below.
2. **Click 'Search'** to fetch the latest listings and price trends.
3. **View the interactive map** to see where cars are listed.
4. **Analyze price and mileage trends** with the scatter plot.
5. **Estimate your car's value** and compare with similar listings.
        """)
with col_howmade:
    with st.expander("🛠️ How This App Was Made", expanded=False):
        st.markdown("""
        - **Built with [Streamlit](https://streamlit.io/)** for rapid, interactive web apps in Python.
        - **Data scraped from OLX.ba** using custom Python scripts.
        - **City geolocation** from a curated JSON file for accurate mapping.
        - **Visualization** powered by PyDeck (interactive map) and Altair (scatter plot).
        - **AI-powered year range**: Uses Gemini API to estimate production years for your search.
        - **Smart filtering**: Only shows relevant, comparable listings for your car.
        - **Modern UI**: Custom CSS and layout for a clean, user-friendly experience.
        """)
# -- # Main App Logic: Mode Selector and Actions -- #
if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Check the price of my car'

# --- Custom Mode Buttons ---
st.markdown('<div class="mode-btn-row">', unsafe_allow_html=True)
col1, col2, _ = st.columns([1,1,0.2])
with col1:
    if st.button('Check the price of my car', key='btn_mode_price', use_container_width=True):
        st.session_state['mode'] = 'Check the price of my car'
with col2:
    if st.button('Search for a car', key='btn_mode_search', use_container_width=True):
        st.session_state['mode'] = 'Search for a car'
st.markdown('</div>', unsafe_allow_html=True)

# --- Highlight selected button ---

st.markdown(f"""
<style>
            #btn_mode_price {{
    {'background: linear-gradient(90deg, #4e54c8 60%, #2D2D86 100%) !important; color: #fff !important; transform: scale(1.04);' if st.session_state['mode']=='Check the price of my car' else ''}
    display: block;
    margin: 0 auto;
}}

        #btn_mode_search {{
    {'background: linear-gradient(90deg, #4e54c8 60%, #2D2D86 100%) !important; color: #fff !important; transform: scale(1.04);' if st.session_state['mode']=='Search for a car' else ''}
    display: block;
    margin: 0 auto;
}}
</style>
""", unsafe_allow_html=True)


mode = st.session_state['mode']

if mode == "Check the price of my car":
    car_model = st.text_input("Car Model", "Golf 4")
    car_year = st.number_input("Production Year", min_value=1980, max_value=2025, value=2003)
    car_kms = st.number_input("Kilometers Driven", min_value=1000, max_value=1_000_000, value=290_000, step=1000)
    fuel_type = st.text_input("Fuel Type", "Dizel")

    if st.button("Check Price", key="check_price_btn"):
        try:
            # -- # Getting Production Year via Gemini API # -- #
            startingDate, endingDate = Gemini.askGemini(car_model,car_year)
            startingDateInt, endingDateInt = int(startingDate), int(endingDate)

            # -- # Scraping OLX via requests # -- #
            total_results = tr.total_results(car_model)
            records = sj.olxScraper(car_model, total_results)
            filtered_records = fr.filter_records(records, startingDateInt, endingDateInt)

            if filtered_records:
                df = pd.DataFrame(filtered_records)
                df = df[df['Fuel'].str.lower() == fuel_type.lower()]
                # -- # Calculate price per 1000 KM # -- #
                df["Price_per_k_km"] = df.apply(
                    lambda row: row["Price"] / (row["KM"] / 1000) if row["KM"] else None,
                    axis=1
                )
                df = df.dropna(subset=["Price_per_k_km"])

                if not df.empty:
                    # -- # Summary Statistics # -- #
                    st.subheader("Summary Statistics")
                    st.write(f"Count: {len(df)}")
                    st.write(f"Min Price (KM): {df['Price'].min()}")
                    st.write(f"Max Price (KM): {df['Price'].max()}")
                    st.write(f"Average Price (KM): {int(df['Price'].mean())}")
                    # -- # City Mapping # -- #

                    with open("json/cities.json", encoding="utf-8") as f:
                        cities_json = json.load(f)
                    # If cities.json has a 'data' key, use it
                    if isinstance(cities_json, dict) and "data" in cities_json:
                        cities_data = cities_json["data"]
                    else:
                        cities_data = cities_json

                    # Build lookup dictionary, ensure keys are int
                    city_lookup = {
                        int(c["id"]): {
                            "name": c["name"],
                            "lat": float(c["location"]["lat"]),
                            "lon": float(c["location"]["lon"])
                        }
                        for c in cities_data if isinstance(c, dict) and "id" in c and "location" in c
                    }

                    # -- # City ID Mapping # -- #
                    df = pd.DataFrame(filtered_records)
                    df["City"] = pd.to_numeric(df["City"], errors="coerce")  # -- # Convert City to numeric # -- #

                    # -- # Check for missing City IDs # -- #
                    city_ids_in_df = set([int(x) for x in df["City"].dropna().unique()])
                    city_ids_in_lookup = set(city_lookup.keys())
                    missing_ids = sorted(list(city_ids_in_df - city_ids_in_lookup))
                    if missing_ids:
                        st.warning(f"City IDs in listings not found in City Lookup: {missing_ids}")
                    else:
                        st.info("All City IDs in listings are present in City Lookup.")

                    # -- # City Name Mapping # -- #
                    def get_city_val(x, key):
                        try:
                            if pd.notnull(x):
                                idx = int(x)
                                if idx in city_lookup:
                                    return city_lookup[idx][key]
                        except Exception:
                            pass
                        return None

                    df["lat"] = df["City"].map(lambda x: get_city_val(x, "lat"))
                    df["lon"] = df["City"].map(lambda x: get_city_val(x, "lon"))
                    df[""] = df["City"].map(lambda x: get_city_val(x, "name"))

                    # -- # Dropping Rows with Missing Coordinates # -- #
                    df_map = df.dropna(subset=["lat", "lon"])

                    if not df_map.empty:
                        # -- # Pydeck # -- #
                        st.subheader("Car Listings Map 📍")

                        df_map = df_map.copy()
                        df_map = df_map.rename(columns={'lat': 'latitude', 'lon': 'longitude'})

                        tooltip = {
                            "html": "<b>{Title}</b><br/>City: {}<br/>Year: {Year}<br/>KM: {KM}<br/>Price: {Price}",
                            "style": {"backgroundColor": "steelblue", "color": "white"}
                        }

                        layer = pdk.Layer(
                            "ScatterplotLayer",
                            data=df_map,
                            get_position='[longitude, latitude]',
                            get_radius=1750,
                            get_fill_color=[255, 0, 0, 160],
                            pickable=True,
                        )
                        view_state = pdk.ViewState(
                            latitude=df_map["latitude"].mean(),
                            longitude=df_map["longitude"].mean(),
                            zoom=7,
                            pitch=0
                        )

                        st.pydeck_chart(pdk.Deck(
                            layers=[layer],
                            initial_view_state=view_state,
                            tooltip=tooltip
                        ))
                    else:
                        st.warning("No listings have valid city coordinates!")
                    # -- # Scatter Plot # -- # Car Listings # -- #
                    st.subheader("Price vs Kilometers Scatter Plot")
                    scatter = alt.Chart(df).mark_circle(size=60).encode(
                        x='KM',
                        y='Price',
                        color='Year',
                        tooltip=['Title', 'Year', 'KM', 'Price', 'Fuel']
                    ).interactive()
                    st.altair_chart(scatter, use_container_width=True)

                    # -- # Estimated Price # -- #
                    st.subheader("Estimate My Car's Value 💰")

                    pool = df.dropna(subset=["Price", "KM"]).copy()
                    pool["km_diff"] = (pool["KM"] - car_kms).abs()
                    if "City_name" not in pool.columns:
                        pool["City_name"] = pool["City"].map(lambda x: get_city_val(x, "name"))
                    tight_band = pool[pool["km_diff"] <= 25_000]

                    comps = tight_band if len(tight_band) >= 8 else pool.nsmallest(12, "km_diff")
                    if "City_name" not in comps.columns:
                        comps["City_name"] = comps["City"].map(lambda x: get_city_val(x, "name"))

                    if not comps.empty:
                        est_med = int(comps["Price"].median())
                        est_lo  = int(comps["Price"].quantile(0.25))
                        est_hi  = int(comps["Price"].quantile(0.75))

                        st.success(
                            f"Estimated price: **{est_med} KM** "
                            f"(typical range: {est_lo}–{est_hi} KM) "
                            f"based on {len(comps)} comparable {fuel_type.lower()} listings near {car_kms:,} km."
                        )
                        st.subheader("Closest-mileage Comparables")
                        st.dataframe(
                            comps.sort_values("km_diff")[["Title","Year","KM","Fuel","Price","City_name","Link"]],
                            use_container_width=True
                        )
                    else:
                        st.warning("No comparable listings found with usable KM & price.")
                else:
                    st.warning("No comparable cars found with this fuel type!")
            else:
                st.warning("No listings found for this model!")
                   # --- Footer ---
    
        except Exception as e:


            st.error(f"Error: {e}")

# ...existing code...

elif mode == "Search for a car":
    search_model = st.text_input("Enter car model to search", "Golf 4", key="search_model_input")
    fuel_type_options = ["All", "Dizel", "Benzin", "Plin", "Hibrid", "Elektricni"]
    selected_fuel = st.selectbox("Fuel Type", fuel_type_options, index=0)
    if st.button("Search", key="search_btn"):
        try:
            total_results = tr.total_results(search_model)
            records = sj.olxScraper(search_model, total_results)
            start_year, end_year = Gemini.askGeminiWithoutModelYear(search_model)
            filtered_records = fr.filter_records(records, start_year, end_year)
            if records:
                df = pd.DataFrame(filtered_records)
                with open("json/cities.json", encoding="utf-8") as f:
                    cities_json = json.load(f)
                if isinstance(cities_json, dict) and "data" in cities_json:
                    cities_data = cities_json["data"]
                else:
                    cities_data = cities_json
                city_lookup = {int(c["id"]): c["name"] for c in cities_data if isinstance(c, dict) and "id" in c and "name" in c}
                df["City_name"] = pd.to_numeric(df["City"], errors="coerce").map(city_lookup)
                if selected_fuel != "All" and "Fuel" in df.columns:
                    df = df[df["Fuel"].str.lower() == selected_fuel.lower()]
                # Calculate price per 1000km for value summary
                if "Price" in df.columns and "KM" in df.columns:
                    df["Price_per_k_km"] = df.apply(
                        lambda row: row["Price"] / (row["KM"] / 1000) if row["KM"] else None,
                        axis=1
                    )
                    df = df.dropna(subset=["Price_per_k_km"])
                # -- # Summary Statistics # -- #
                    st.subheader("Summary Statistics")
                    st.write(f"Count: {len(df)}")
                    st.write(f"Min Price (KM): {df['Price'].min()}")
                    st.write(f"Max Price (KM): {df['Price'].max()}")
                    st.write(f"Average Price (KM): {int(df['Price'].mean())}")
                show_cols = [col for col in ["Title", "Year", "Price", "City_name", "Fuel", "KM", "Link"] if col in df.columns]
                st.subheader(f"Results for '{search_model}' ({len(df)} found)")
                st.dataframe(df[show_cols], use_container_width=True)

                # -- # Show Map # -- 3
                if "City" in df.columns:
                    city_latlon = {int(c["id"]): (float(c["location"]["lat"]), float(c["location"]["lon"])) for c in cities_data if isinstance(c, dict) and "id" in c and "location" in c}
                    df["lat"] = pd.to_numeric(df["City"], errors="coerce").map(lambda x: city_latlon.get(int(x), (None, None))[0] if pd.notnull(x) and int(x) in city_latlon else None)
                    df["lon"] = pd.to_numeric(df["City"], errors="coerce").map(lambda x: city_latlon.get(int(x), (None, None))[1] if pd.notnull(x) and int(x) in city_latlon else None)
                    df_map = df.dropna(subset=["lat", "lon"])
                    if not df_map.empty:
                        st.subheader("Car Listings Map 📍")
                        df_map = df_map.copy()
                        df_map = df_map.rename(columns={'lat': 'latitude', 'lon': 'longitude'})
                        tooltip = {
                            "html": "<b>{Title}</b><br/>City: {City_name}<br/>Year: {Year}<br/>KM: {KM}<br/>Price: {Price}",
                            "style": {"backgroundColor": "steelblue", "color": "white"}
                        }
                        layer = pdk.Layer(
                            "ScatterplotLayer",
                            data=df_map,
                            get_position='[longitude, latitude]',
                            get_radius=1750,
                            get_fill_color=[255, 0, 0, 160],
                            pickable=True,
                        )
                        view_state = pdk.ViewState(
                            latitude=df_map["latitude"].mean(),
                            longitude=df_map["longitude"].mean(),
                            zoom=7,
                            pitch=0
                        )
                        st.pydeck_chart(pdk.Deck(
                            layers=[layer],
                            initial_view_state=view_state,
                            tooltip=tooltip
                        ))
                    else:
                        st.info("No valid city coordinates for map visualization.")

                if not df.empty and "Price_per_k_km" in df.columns:
                    st.subheader("Best Bang for the Buck (Lowest Price per 1000 KM)")
                    best_value = df.nsmallest(5, "Price_per_k_km")
                    st.dataframe(best_value[show_cols + ["Price_per_k_km"]], use_container_width=True)
            else:
                st.warning("No listings found for this model!")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("""
    <div class='footer'>
        &copy; 2025 OLX Car Tracker &mdash; Built with ❤️ by <b>Muhamad Assaad</b> using Streamlit<br>
        <span style='font-size:0.95em;'>Data sourced from OLX.ba | For educational and personal use only</span>
    </div>
    """, unsafe_allow_html=True)