from flask import Flask, request, Response
from ics import Calendar
import requests
import base64
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def filter_ics():
    # Read env variables for url and filter
    if 'ICS_URL' in os.environ:
        ics_url = os.environ['ICS_URL']
    else:
        ics_url = request.args.get('url')
    
    if 'FILTER' in os.environ:
        filter_name = os.environ['FILTER']
    else:
        filter_name = request.args.get('filter', '') # Default to empty string, so that all events are returned

    if not ics_url:
        return {"error": "Please provide the 'url' query parameter."}, 400
    
    # If the ics_url is base64 encoded, decode it (aH prefix is because the encoding of htt… starts with aH)
    if ics_url.startswith("aH"):
        ics_url = base64.b64decode(ics_url).decode()

    try:
        ics_content = requests.get(ics_url).text
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

    calendar = Calendar(ics_content)

    filtered_events = [event for event in calendar.events if filter_name.lower() not in event.name.lower()]

    new_calendar = Calendar(events=filtered_events)
    filtered_ics_content = new_calendar.serialize()

    return Response(filtered_ics_content, mimetype='text/calendar', headers={'Content-Disposition': 'attachment; filename=filtered.ics'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
