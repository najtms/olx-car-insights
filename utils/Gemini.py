import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()  # Loads API Key from .env
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def askGemini(search_query: str, car_years: int):
    question = (
        "What is the production year range for a {car_years} {car_model}? Give the answer in the format YYYY-YYYY. Nothing else."
    )
    question_fix = question.format(car_model=search_query, car_years=car_years)
    response = model.generate_content(question_fix)
    print(response.text)
    model_year = response.text.split('-')
    if not model_year[0].isdigit():
        model_year[0] = 1886
    else:
        model_year[0] = int(model_year[0])
    if not model_year[1].isdigit():
        from datetime import datetime
        model_year[1] = datetime.now().year
    else:
        model_year[1] = int(model_year[1])
    return model_year[0], model_year[1]

def askGeminiWithoutModelYear(search_query: str):
    question = (
        "What is the production year range for a {car_model}? Give the answer in the format YYYY-YYYY. Nothing else."
    )
    question_fix = question.format(car_model=search_query)
    response = model.generate_content(question_fix)
    print(response.text)
    model_year = response.text.split('-')
    if not model_year[0].isdigit():
        model_year[0] = 1886
    else:
        model_year[0] = int(model_year[0])
    if not model_year[1].isdigit():
        from datetime import datetime
        model_year[1] = datetime.now().year
    else:
        model_year[1] = int(model_year[1])
    return model_year[0], model_year[1]


