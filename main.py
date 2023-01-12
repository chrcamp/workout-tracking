import auth
import requests
from datetime import datetime

today_date = datetime.now().strftime('%m/%d/%Y')
now_time = datetime.now().strftime('%X')

APP_ID = auth.nix_appid
APP_KEY = auth.nix_key
GENDER = auth.gender
WEIGHT = auth.weight
HEIGHT = auth.height
AGE = auth.age

nix_headers = {
    'x-app-id': APP_ID,
    'x-app-key': APP_KEY
}

nix_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
workout_endpoint = auth.workout_endpoint
workout_header = {'Authorization': f'Bearer {auth.workout_auth}'}

exercise_input = input("Tell me what exercises you did: ")

parameters = {
    'query': exercise_input,
    'gender': GENDER,
    'weight_kg': WEIGHT,
    'height_cm': HEIGHT,
    'age': AGE
}

response = requests.post(url=nix_endpoint, json=parameters, headers=nix_headers)
response.raise_for_status()
data = response.json()

for exercise in data['exercises']:
    sheet_inputs = {
        'workout': {
            'date': today_date,
            'time': now_time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }
    sheet_response = requests.post(workout_endpoint, json=sheet_inputs, headers=workout_header)

    print(sheet_response.text)
