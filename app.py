from flask import Flask, render_template, request
import random
import requests

app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    api_url = f"https://script.google.com/macros/s/AKfycby44G47rIm2eTMooqC4aHyJUgRwHLoHrgjDDeEOrn6bCCsm4C2gZAlvgqmoiwiGZyBaMg/exec"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        events = response.json().get('results', [])
        # recent_events = events[:5]
        recent_events = random.sample(events, 5)
    else:
        recent_events = []

    return render_template('index.html', recent_events=recent_events)

# Define a route for handling the search
@app.route('/search', methods=['POST'])
def search():
    query = str(request.form['query']).lower()
    api_url = f"https://script.google.com/macros/s/AKfycby44G47rIm2eTMooqC4aHyJUgRwHLoHrgjDDeEOrn6bCCsm4C2gZAlvgqmoiwiGZyBaMg/exec"

    # Make the API request
    response = requests.get(api_url)

    # Handle API response
    if response.status_code == 200:
        events = response.json().get('results', [])

        filtered_events = []
        for event in events:
            print(event)
            # Check if the 'Event' or 'Description' contains the query (case-insensitive)
            if query in event['Event'].lower() or query in event.get('Description', '').lower():
                filtered_events.append(event)
        
        # Sort filtered events based on how well they match the query (priority to earlier matches)
        filtered_events.sort(key=lambda e: e['Event'].lower().index(query) if query in e['Event'].lower() else float('inf'))
    else:
        filtered_events = []

    return render_template('results.html', query=query, events=filtered_events)

if __name__ == '__main__':
    app.run(debug=True)

