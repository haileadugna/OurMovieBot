import requests

def get_movies_by_genre(genre):
    url = "https://moviesdatabase.p.rapidapi.com/titles"

    headers = {
        'X-RapidAPI-Key': "97bdb1c7camsh51235664bc07f3cp1021b1jsn519721a3a96b",
        'X-RapidAPI-Host': "moviesdatabase.p.rapidapi.com"
    }

    params = {
        "genre": genre,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None



