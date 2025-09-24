from flask import Blueprint, request, jsonify
from models.db import get_db_connection

destinations_bp = Blueprint('destinations_bp', __name__)

@destinations_bp.route('/destinations', methods=['GET'])
def get_all_destinations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM destinations")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

@destinations_bp.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM destinations WHERE destination_id = %s", (destination_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return jsonify(record)
    return jsonify({'error': 'Destination not found'}), 404

@destinations_bp.route('/destinations', methods=['POST'])
def add_destination():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO destinations (name, type, distance_from_earth_km)
        VALUES (%s, %s, %s)
    """, (
        data['name'], data.get('type'), data.get('distance_from_earth_km')
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Destination added successfully'})

@destinations_bp.route('/destinations/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE destinations
        SET name = %s, type = %s, distance_from_earth_km = %s
        WHERE destination_id = %s
    """, (
        data['name'], data.get('type'), data.get('distance_from_earth_km'), destination_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Destination updated successfully'})

@destinations_bp.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM destinations WHERE destination_id = %s", (destination_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Destination deleted successfully'})

@destinations_bp.route('/destinations/search', methods=['GET'])
def search_destinations():
    keyword = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM destinations WHERE name LIKE %s", (f'%{keyword}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)
