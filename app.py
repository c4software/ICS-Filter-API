from flask import Flask, request, Response
from ics import Calendar
import requests
import base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def filter_ics():
    ics_url = request.args.get('url')
    filter_name = request.args.get('filter', 'Cours Annulé')  # Default to "Cours Annulé" if not provided

    if not ics_url:
        return {"error": "Please provide the 'url' query parameter."}, 400
    
    if ics_url.startswith("aH"):
        ics_url = base64.b64decode(ics_url).decode()

    try:
        ics_content = requests.get(ics_url).text
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

    calendar = Calendar(ics_content)

    # Filter out events that contain the specified name
    filtered_events = [event for event in calendar.events if filter_name.lower() not in event.name.lower()]

    new_calendar = Calendar(events=filtered_events)
    filtered_ics_content = new_calendar.serialize()

    return Response(filtered_ics_content, mimetype='text/calendar', headers={'Content-Disposition': 'attachment; filename=filtered.ics'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
