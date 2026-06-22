from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from io import BytesIO

app = Flask(__name__)

# Mock prospecting data (expandable with real BC data)
MOCK_DATA = {
    "princeton": {
        "indicators": ["Quartz veins", "Black sands (magnetite/ilmenite)", "Red garnets", "Pyrite/arsenopyrite"],
        "tips": "Focus on Tulameen River bends and bedrock cracks. Check claims in MTO.",
        "lat": 49.46, "lon": -120.51
    },
    "oliver": {
        "indicators": ["Sedimentary contacts", "Heavy mineral concentrates", "Rusty staining"],
        "tips": "South Okanagan placer potential. Use iMapBC geology layers.",
        "lat": 49.18, "lon": -119.55
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/search', methods=['POST'])
def search():
    location = request.form.get('location', 'Princeton BC').lower()
    data = MOCK_DATA.get(location.split()[0], {
        "indicators": ["Quartz veins", "Black sands", "Garnet"],
        "tips": "General BC prospecting: Use iMapBC + Avenza offline.",
        "lat": 49.5, "lon": -120.0
    })
    return jsonify({
        "location": location.title(),
        "indicators": data["indicators"],
        "tips": data["tips"],
        "coords": [data["lat"], data["lon"]]
    })

@app.route('/download_map', methods=['POST'])
def download_map():
    location = request.form.get('location', 'Princeton')
    content = f"Offline Map Package for {location}\n\nIndicators: Quartz veins, Black sands, Garnets\n\nImport into Avenza Maps or QGIS.\n\nTips: Focus on river bends and altered zones."
    buffer = BytesIO(content.encode('utf-8'))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{location}_prospect_map.txt",
        mimetype='text/plain'
    )

@app.route('/upload_notes', methods=['POST'])
def upload_notes():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    return jsonify({
        "message": f"Uploaded {file.filename} successfully! Waypoints added to your offline map.",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)