# routes/missions.py
from flask import Blueprint, request, jsonify
from models.db import get_db_connection

missions_bp = Blueprint('missions_bp', __name__)

@missions_bp.route('/missions', methods=['GET'])
def get_missions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM missions")
    missions = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(missions)

@missions_bp.route('/missions/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM missions WHERE mission_id = %s", (mission_id,))
    mission = cursor.fetchone()
    cursor.close()
    conn.close()
    if mission:
        return jsonify(mission)
    return jsonify({'error': 'Mission not found'}), 404

@missions_bp.route('/missions', methods=['POST'])
def add_mission():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO missions (mission_id, name, agency_id, spacecraft_id, destination_id, launch_date, mission_type, mission_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['mission_id'], data['name'], data['agency_id'], data['spacecraft_id'],
        data['destination_id'], data['launch_date'], data['mission_type'], data['mission_status']
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Mission added successfully"})

@missions_bp.route('/missions/<int:mission_id>', methods=['PUT'])
def update_mission(mission_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE missions
        SET name=%s, agency_id=%s, spacecraft_id=%s, destination_id=%s, launch_date=%s, mission_type=%s, mission_status=%s
        WHERE mission_id=%s
    """, (
        data['name'], data['agency_id'], data['spacecraft_id'], data['destination_id'],
        data['launch_date'], data['mission_type'], data['mission_status'], mission_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Mission updated successfully"})

@missions_bp.route('/missions/<int:mission_id>', methods=['DELETE'])
def delete_mission(mission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE mission_id=%s", (mission_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Mission deleted successfully"})

@missions_bp.route('/missions/search', methods=['GET'])
def search_missions():
    keyword = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM missions WHERE name LIKE %s", (f'%{keyword}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)
