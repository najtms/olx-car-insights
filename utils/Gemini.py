# -- Google Gemini -- #
from google import genai
from dotenv import load_dotenv

load_dotenv()  # Loads API Key

client = genai.Client()

def askGemini(search_query: str, car_years: int):
    question = (
        "What is the production year range for a {car_years} {car_model}? Give the answer in the format YYYY-YYYY. Nothing else."
    )
    question_fix = question.format(car_model=search_query, car_years=car_years)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question_fix
    )
    print(response.text)
    model_year = response.text.split('-')
    if not model_year[0].isdigit():
            model_year[0] = 1886
    else:
        model_year[0] = int(model_year[0])

    if not model_year[1].isdigit():
        from datetime import datetime
        model_year[1] = datetime.now().year  # Current year
    else:
        model_year[1] = int(model_year[1])

    return model_year[0], model_year[1]

def askGeminiWithoutModelYear(search_query: str):
    question = (
        "What is the production year range for a {car_model}? Give the answer in the format YYYY-YYYY. Nothing else."
    )
    question_fix = question.format(car_model=search_query)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question_fix
    )
    print(response.text)
    model_year = response.text.split('-')
    if not model_year[0].isdigit():
            model_year[0] = 1886
    else:
        model_year[0] = int(model_year[0])

    if not model_year[1].isdigit():
        from datetime import datetime
        model_year[1] = datetime.now().year  # Current year
    else:
        model_year[1] = int(model_year[1])

    return model_year[0], model_year[1]


