# routes/spacecrafts.py

from flask import Blueprint, request, jsonify
from models.db import get_db_connection

spacecrafts_bp = Blueprint('spacecrafts_bp', __name__)

@spacecrafts_bp.route('/spacecrafts', methods=['GET'])
def get_all_spacecrafts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spacecrafts")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

@spacecrafts_bp.route('/spacecrafts/<int:spacecraft_id>', methods=['GET'])
def get_spacecraft(spacecraft_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spacecrafts WHERE spacecraft_id = %s", (spacecraft_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return jsonify(record)
    return jsonify({'error': 'Spacecraft not found'}), 404

@spacecrafts_bp.route('/spacecrafts', methods=['POST'])
def add_spacecraft():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO spacecrafts (name, type, manufacturer, first_flight, capacity)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['name'], data['type'], data['manufacturer'],
        data['first_flight'], data['capacity']
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Spacecraft added successfully'})

@spacecrafts_bp.route('/spacecrafts/<int:spacecraft_id>', methods=['PUT'])
def update_spacecraft(spacecraft_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE spacecrafts
        SET name = %s, type = %s, manufacturer = %s, first_flight = %s, capacity = %s
        WHERE spacecraft_id = %s
    """, (
        data['name'], data['type'], data['manufacturer'],
        data['first_flight'], data['capacity'], spacecraft_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Spacecraft updated successfully'})

@spacecrafts_bp.route('/spacecrafts/<int:spacecraft_id>', methods=['DELETE'])
def delete_spacecraft(spacecraft_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spacecrafts WHERE spacecraft_id = %s", (spacecraft_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Spacecraft deleted successfully'})

@spacecrafts_bp.route('/spacecrafts/search', methods=['GET'])
def search_spacecrafts():
    keyword = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spacecrafts WHERE name LIKE %s", (f'%{keyword}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)
