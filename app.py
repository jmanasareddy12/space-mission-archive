from flask import Flask, render_template,Blueprint, request, jsonify,redirect,url_for,session
from flask_cors import CORS
from models.db import get_db_connection
from routes.missions import missions_bp  # ✅ import the blueprint
from routes.agencies import agencies_bp
from routes.spacecrafts import spacecrafts_bp
from routes.missions_crew import mission_crew_bp
from routes.astronauts import astronauts_bp
from routes.destinations import destinations_bp


app = Flask(__name__)
CORS(app)

# ✅ Register blueprints
app.register_blueprint(missions_bp)
app.register_blueprint(agencies_bp)
app.register_blueprint(spacecrafts_bp)
app.register_blueprint(mission_crew_bp)
app.register_blueprint(astronauts_bp, url_prefix='')
app.register_blueprint(destinations_bp, url_prefix='')
# -- HTML PAGE ROUTES -- #

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template('table_base.html', tables=tables)

@app.route('/dashboard')
def dashboard():
    records = get_all_missions()
    return render_template('dashboard.html', records=records)

@app.route('/missions-page')
def missions_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM missions")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('missions.html', table_name='Missions', records=records)

# ✅ Safer dynamic route
ALLOWED_TABLES = {'missions', 'agencies', 'spacecrafts', 'destinations', 'astronauts', 'mission_crew'}

@app.route('/table/<table_name>')
def show_table(table_name):
    if table_name not in ALLOWED_TABLES:
        return "Invalid table name", 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(f"{table_name}.html", records=records)

@app.route('/table/missions')
def show_missions_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM missions")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', records=records)

def get_all_missions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM missions")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records


#AGENCIESSSS

# -- AGENCIES ROUTES -- #

@app.route('/agencies', methods=['GET'])
def get_agencies():
    return jsonify(agencies_bp.get_all_agencies())

@app.route('/agencies/<int:agency_id>', methods=['GET'])
def get_agency(agency_id):
    agency = agencies_bp.get_agency_by_id(agency_id)
    if agency:
        return jsonify(agency)
    return jsonify({'error': 'Agency not found'}), 404

@app.route('/agencies', methods=['POST'])
def add_agency():
    data = request.get_json()
    agencies_bp.add_agency(data)
    return jsonify({"message": "Agency added successfully"})

@app.route('/agencies/<int:agency_id>', methods=['PUT'])
def update_agency(agency_id):
    data = request.get_json()
    agencies_bp.update_agency(agency_id, data)
    return jsonify({"message": "Agency updated successfully"})

@app.route('/agencies/<int:agency_id>', methods=['DELETE'])
def delete_agency(agency_id):
    agencies_bp.delete_agency(agency_id)
    return jsonify({"message": "Agency deleted successfully"})

@app.route('/agencies-page')
def agencies_page():
    return render_template('agencies.html')


@app.route('/spacecrafts-page')
def spacecrafts_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spacecrafts")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('spacecrafts.html', records=records)

@app.route('/astronauts-page')
def astronauts_page():
    return render_template('astronauts.html')

@app.route('/destinations-page')
def destinations_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM destinations")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('destinations.html')

@app.route('/destination-astronauts')
def destination_astronauts_page():
    return render_template('destination_astronauts.html')

@app.route('/crew-page')
def mission_crew_page():
    return render_template('mission_crew.html')

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
