# 🚗 OLX Car Tracker

**OLX Car Tracker** is a Streamlit web app for searching, analyzing, and visualizing car listings from [OLX.ba](https://www.olx.ba).  
Instantly estimate your car’s value, find the best deals, and explore listings on an interactive map.  

This project is **for personal learning and educational purposes only**. It is **not intended for commercial use**.  

---

## ✨ Features

- 📡 **Real-time OLX.ba data** via custom Python scrapers  
- 🤖 **AI-powered car price estimation** (Google Gemini API)  
- 🔎 **Search & filter** by model, fuel type, and more  
- 💰 **Best bang for the buck finder** (price-to-performance deals)  
- 🗺️ **Interactive map** of listings (PyDeck)  
- 📊 **Data visualizations** (Altair scatter plots & charts)  
- 📱 **Mobile responsive UI** (Streamlit + custom CSS)  

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) – Web app framework  
- [PyDeck](https://deckgl.readthedocs.io/en/latest/) – Interactive maps  
- [Altair](https://altair-viz.github.io/) – Data visualization  
- [Google Gemini API](https://ai.google.dev/) – AI-powered price estimation  
- **Custom Python scrapers** – OLX.ba data collection  
- ❤️ Built by **Muhamad Assaad**  

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/najtms/olx-car-tracker.git
   cd olx-car-tracker
2. **Install Dependecies**
    pip install -r requirements.txt
3. **Setup AI**
    GEMINI_API_KEY=your_api_key_here

**You are down now its time to run!**
```py -m streamlit run app.py


## Project Structure
olx-car-tracker/
│── app.py               # Main Streamlit app
│── requirements.txt     # Python dependencies
│── utils/               # Scrapers, data filters, helpers
│── static/              # Images, icons, assets
│── README.md            # Project documentation
│── .env                 # API keys (ignored in Git)
