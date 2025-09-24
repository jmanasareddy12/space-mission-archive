from flask import Blueprint, request, jsonify
from models.db import get_db_connection

agencies_bp = Blueprint('agencies_bp', __name__)

@agencies_bp.route('/agencies', methods=['GET'])
def get_agencies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agencies")
    agencies = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(agencies)

@agencies_bp.route('/agencies/<int:agency_id>', methods=['GET'])
def get_agency(agency_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agencies WHERE agency_id = %s", (agency_id,))
    agency = cursor.fetchone()
    cursor.close()
    conn.close()
    if agency:
        return jsonify(agency)
    else:
        return jsonify({'error': 'Agency not found'}), 404

@agencies_bp.route('/agencies', methods=['POST'])
def add_agency():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agencies (name, country, founded_year, headquarters, website)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data.get('name'),
        data.get('country'),
        data.get('founded_year'),
        data.get('headquarters'),
        data.get('website')
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Agency added successfully"})

@agencies_bp.route('/agencies/<int:agency_id>', methods=['PUT'])
def update_agency(agency_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agencies SET name=%s, country=%s, founded_year=%s, headquarters=%s, website=%s
        WHERE agency_id=%s
    """, (
        data.get('name'),
        data.get('country'),
        data.get('founded_year'),
        data.get('headquarters'),
        data.get('website'),
        agency_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Agency updated successfully"})

@agencies_bp.route('/agencies/<int:agency_id>', methods=['DELETE'])
def delete_agency(agency_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agencies WHERE agency_id=%s", (agency_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Agency deleted successfully"})

@agencies_bp.route('/agencies/search', methods=['GET'])
def search_agencies():
    keyword = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agencies WHERE name LIKE %s", (f'%{keyword}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@agencies_bp.route('/agencies/aggregate', methods=['GET'])
def aggregate_agencies():
    agg_type = request.args.get('type')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if agg_type == 'count':
        cursor.execute("SELECT COUNT(*) AS total FROM agencies")
        result = cursor.fetchone()

    elif agg_type == 'avg_year':
        cursor.execute("SELECT AVG(founded_year) AS average FROM agencies")
        result = cursor.fetchone()

    elif agg_type == 'oldest':
        cursor.execute("SELECT name, founded_year FROM agencies ORDER BY founded_year ASC LIMIT 1")
        result = cursor.fetchone()

    elif agg_type == 'newest':
        cursor.execute("SELECT name, founded_year FROM agencies ORDER BY founded_year DESC LIMIT 1")
        result = cursor.fetchone()

    elif agg_type == 'country_count':
        cursor.execute("SELECT country, COUNT(*) AS total FROM agencies GROUP BY country")
        result = cursor.fetchall()
    else:
        result = {'error': 'Invalid aggregate type'}

    cursor.close()
    conn.close()
    return jsonify(result)
