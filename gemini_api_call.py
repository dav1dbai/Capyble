
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env into the environment

def make_api_call():
    '''
    # Trial 1
    # Accessing the API key from an environment variable
    api_key = os.getenv('GEMINI_KEY')
    print(api_key)
    if not api_key:
        raise ValueError("API key not found. Please set the GEMINI_KEY environment variable.")

    # The API endpoint you're trying to access; replace this with the actual endpoint
    url = 'https://api.gemini.com/v1/symbols'

    # Including the API key in the request's header
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    # Making the GET request
    response = requests.get(url, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        # Processing the response
        print("working")
        data = response.json()
        print(data)
    else:
        print(f'Failed to retrieve data: {response.status_code}')

    
    #Trial 2
    symbols = ['btcusd', 'ethusd']  # Symbols for Bitcoin and Ethereum trading pairs
    for symbol in symbols:
        url = f'https://api.gemini.com/v1/pubticker/{symbol}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Symbol: {symbol.upper()}")
            print(f"Last trading price: {data['last']}")
            print(f"Volume: {data['volume'][symbol[:3].upper()]}")
            print("------")
        else:
            print(f'Failed to retrieve data for {symbol.upper()}: {response.status_code}')
    '''

if __name__ == '__main__':
    make_api_call()