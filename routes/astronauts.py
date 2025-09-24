from flask import Blueprint, request, jsonify
from models.db import get_db_connection

astronauts_bp = Blueprint('astronauts_bp', __name__)

@astronauts_bp.route('/astronauts', methods=['GET'])
def get_all_astronauts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM astronauts")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

@astronauts_bp.route('/astronauts/<int:astronaut_id>', methods=['GET'])
def get_astronaut(astronaut_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM astronauts WHERE astronaut_id = %s", (astronaut_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return jsonify(record)
    return jsonify({'error': 'Astronaut not found'}), 404

@astronauts_bp.route('/astronauts', methods=['POST'])
def add_astronaut():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO astronauts (name, nationality, date_of_birth, agency_id, number_of_missions)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['name'],
        data.get('nationality'),
        data.get('date_of_birth'),
        data.get('agency_id'),
        data.get('number_of_missions', 0)
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Astronaut added successfully'})

@astronauts_bp.route('/astronauts/<int:astronaut_id>', methods=['PUT'])
def update_astronaut(astronaut_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE astronauts
        SET name = %s,
            nationality = %s,
            date_of_birth = %s,
            agency_id = %s,
            number_of_missions = %s
        WHERE astronaut_id = %s
    """, (
        data['name'],
        data.get('nationality'),
        data.get('date_of_birth'),
        data.get('agency_id'),
        data.get('number_of_missions', 0),
        astronaut_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Astronaut updated successfully'})

@astronauts_bp.route('/astronauts/<int:astronaut_id>', methods=['DELETE'])
def delete_astronaut(astronaut_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM astronauts WHERE astronaut_id = %s", (astronaut_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Astronaut deleted successfully'})

@astronauts_bp.route('/astronauts/search', methods=['GET'])
def search_astronauts():
    keyword = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM astronauts WHERE name LIKE %s", (f'%{keyword}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@astronauts_bp.route('/astronauts/by-destination/<int:destination_id>', methods=['GET'])
def get_astronauts_by_destination(destination_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT DISTINCT a.*
    FROM astronauts a
    JOIN mission_crew ma ON a.astronaut_id = ma.astronaut_id
    JOIN missions m ON ma.mission_id = m.mission_id
    JOIN destinations d ON m.destination_id = d.destination_id
    WHERE d.destination_id = %s
    """
    cursor.execute(query, (destination_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@astronauts_bp.route('/astronauts/filter', methods=['GET'])
def filter_astronauts():
    name_query = request.args.get('q', '')
    destination_id = request.args.get('destination_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if destination_id and destination_id != 'all':
        query = """
            SELECT DISTINCT a.*
            FROM astronauts a
            JOIN mission_crew ma ON a.astronaut_id = ma.astronaut_id
            JOIN missions m ON ma.mission_id = m.mission_id
            WHERE m.destination_id = %s AND a.name LIKE %s
        """
        cursor.execute(query, (destination_id, f"%{name_query}%"))
    else:
        query = "SELECT * FROM astronauts WHERE name LIKE %s"
        cursor.execute(query, (f"%{name_query}%",))

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)