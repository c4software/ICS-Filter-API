# ICS Filter API

This project provides a RESTful API to filter out events from an ICS (iCalendar) feed based on a dynamic event name. The API is built with Flask and served using a production-grade WSGI server, Gunicorn. It is containerized using Docker for easy deployment.

## Features

Filter events from an ICS feed based on a specified event name. The API supports the following query parameters: 

- `url` (required): The URL of the ICS feed.
- `filter` (optional): The event name to filter out. Default is `"Cours Annulée"`.

## Requirements

- Python 3.9+

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/yourusername/ics-filter-api.git
cd ics-filter-api
```

### Setup for Local Development

1. **Create a Virtual Environment** (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install the Required Packages**:

```bash
pip install -r requirements.txt
```

3. **Run the Application**:

```bash
python3 app.py
```

The API will be available at `http://localhost:5000`.

### Running with Docker

1. **Build the Docker Image**:

```bash
docker build -t ics-filter-api .
```

2. **Run the Docker Container**:

```bash
docker run -d -p 5000:5000 ics-filter-api
```

The API will be available at `http://localhost:5000`.

## API Usage

### Query Parameters

- **`url`** (required): The URL of the ICS feed. This can be provided as a raw URL or as a base64-encoded string.
- **`filter`** (optional): The event name to filter out. Default is `"Cours Annulée"`.

### Using a Base64-Encoded URL

If your ICS feed URL contains special characters (e.g., `&`, `?`), you can encode the URL in base64 and pass it as the `url` parameter.

### Example Request

```bash
curl "http://localhost:5000/filter-ics?url=https://example.com/your-calendar.ics&filter=Holiday" -o filtered_calendar.ics
```

This request will filter out all events with "Holiday" in their name from the provided ICS feed.

### Example with Base64-Encoded URL

```bash
curl "http://localhost:5000/filter-ics?url=aHR0cHM6Ly9leGFtcGxlLmNvbS9nb29nbGUuY29tL3lvdXItY2FsZW5kYXIuaWNz&filter=Holiday" -o filtered_calendar.ics
```

This request will filter out all events with "Holiday" in their name from the provided ICS feed.

### Example Response

The response will be an ICS file containing the filtered events.

### Deployment without Docker

1. **Ensure Gunicorn is Installed**:

```bash
pip install gunicorn
```

2. **Run with Gunicorn**:

```bash
export PYTHONUNBUFFERED=1
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```