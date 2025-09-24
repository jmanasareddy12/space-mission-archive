from flask import Blueprint, request, jsonify
from models.db import get_db_connection
import mysql.connector

mission_crew_bp = Blueprint('mission_crew_bp', __name__)

@mission_crew_bp.route('/mission_crew', methods=['GET'])
def get_all_mission_crew():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mission_crew")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

@mission_crew_bp.route('/mission_crew/<int:mission_id>/<int:astronaut_id>', methods=['GET'])
def get_mission_crew_member(mission_id, astronaut_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM mission_crew WHERE mission_id = %s AND astronaut_id = %s
    """, (mission_id, astronaut_id))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return jsonify(record)
    return jsonify({'error': 'Mission crew member not found'}), 404

@mission_crew_bp.route('/mission_crew', methods=['POST'])
def add_mission_crew_member():
    data = request.get_json()
    mission_id = data.get('mission_id')
    astronaut_id = data.get('astronaut_id')
    role = data.get('role')

    if not mission_id or not astronaut_id or not role:
        return jsonify({'error': 'mission_id, astronaut_id, and role are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO mission_crew (mission_id, astronaut_id, role)
            VALUES (%s, %s, %s)
        """, (mission_id, astronaut_id, role))
        conn.commit()
    except mysql.connector.IntegrityError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': 'Mission crew member added successfully'})

@mission_crew_bp.route('/mission_crew/<int:mission_id>/<int:astronaut_id>', methods=['PUT'])
def update_mission_crew_member(mission_id, astronaut_id):
    data = request.get_json()
    role = data.get('role')
    if not role:
        return jsonify({'error': 'role is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE mission_crew
        SET role = %s
        WHERE mission_id = %s AND astronaut_id = %s
    """, (role, mission_id, astronaut_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Mission crew member updated successfully'})

@mission_crew_bp.route('/mission_crew/<int:mission_id>/<int:astronaut_id>', methods=['DELETE'])
def delete_mission_crew_member(mission_id, astronaut_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM mission_crew WHERE mission_id = %s AND astronaut_id = %s
    """, (mission_id, astronaut_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Mission crew member deleted successfully'})

@mission_crew_bp.route('/mission_crew/search', methods=['GET'])
def search_mission_crew():
    keyword = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM mission_crew WHERE role LIKE %s
    """, (f'%{keyword}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)
