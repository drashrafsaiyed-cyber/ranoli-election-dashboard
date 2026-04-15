"""
Election Dashboard - Ranoli Jilla Panchayat 2026
================================================
Web application for Girirajsingh Gohil's BJP campaign.

Features:
- Voter search by EPIC, name, surname
- Booth-wise clickable views with voter lists
- Jaati-wise classification from surnames
- Worker distribution for ~300 karyakartas
- Area-wise summary, Age-wise breakdown, Gender-wise stats
- Booth location/area/society names
- Telegram bot integration for field reporting
- Excel backup export
"""

import os, sys, json, sqlite3, io
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from collections import Counter, defaultdict

# Use relative paths so it works both locally and on deployment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from jaati_mapping import classify_surname, get_jaati_english, get_jaati_color, JAATI_CATEGORIES
from corrected_locations import CORRECTED as CORRECTED_LOCATIONS

app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'),
            static_folder=str(BASE_DIR / 'static'))

DB_PATH = BASE_DIR / "voters.db"

# ============================================================
# Database helpers
# ============================================================

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


# ============================================================
# Booth location data
# ============================================================

AREA_MAP = {
    '3-Bajava': '3-Bajava',
    '16-Nandesari': '16-Nandesari',
    '18-Ranoli-1': '18-Ranoli-1',
    '19-Ranoli-2': '19-Ranoli-2',
}

def get_booth_location(area, bhag_no):
    """Get corrected location for a booth."""
    # Map area names to corrected_locations keys
    area_key_map = {
        '3-Bajava': '3-Bajava',
        '16-Nandesari': '16-Nandesari',
        '18-Ranoli-1': '18-Ranoli-1',
        '19-Ranoli-2': '19-Ranoli-2',
    }
    key = (area_key_map.get(area, area), bhag_no)
    if key in CORRECTED_LOCATIONS:
        return CORRECTED_LOCATIONS[key]
    return {'gujarati': '', 'english': '', 'village': ''}


# ============================================================
# Routes
# ============================================================

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/overview')
def api_overview():
    """Get overall election overview stats."""
    conn = get_db()

    # Total voters
    total = conn.execute("SELECT COUNT(*) FROM voters").fetchone()[0]

    # By area
    areas = conn.execute("""
        SELECT area, COUNT(*) as count,
               SUM(CASE WHEN gender='M' THEN 1 ELSE 0 END) as male,
               SUM(CASE WHEN gender='F' THEN 1 ELSE 0 END) as female
        FROM voters GROUP BY area ORDER BY area
    """).fetchall()

    # Gender overall
    gender = conn.execute("""
        SELECT gender, COUNT(*) as count FROM voters
        WHERE gender IN ('M', 'F') GROUP BY gender
    """).fetchall()

    # Age groups
    age_groups = conn.execute("""
        SELECT
            CASE
                WHEN age BETWEEN 18 AND 25 THEN '18-25'
                WHEN age BETWEEN 26 AND 35 THEN '26-35'
                WHEN age BETWEEN 36 AND 45 THEN '36-45'
                WHEN age BETWEEN 46 AND 55 THEN '46-55'
                WHEN age BETWEEN 56 AND 65 THEN '56-65'
                WHEN age > 65 THEN '65+'
                ELSE 'Unknown'
            END as age_group,
            COUNT(*) as count
        FROM voters WHERE age > 0 GROUP BY age_group
    """).fetchall()

    conn.close()

    return jsonify({
        'total_voters': total,
        'winning_target': int(total * 0.55),
        'areas': [dict(a) for a in areas],
        'gender': {g['gender']: g['count'] for g in gender},
        'age_groups': {a['age_group']: a['count'] for a in age_groups},
        'total_booths': 36,
    })


@app.route('/api/booths')
def api_booths():
    """Get all booth data with stats."""
    conn = get_db()

    booths = conn.execute("""
        SELECT area, bhag_no, COUNT(*) as total,
               SUM(CASE WHEN gender='M' THEN 1 ELSE 0 END) as male,
               SUM(CASE WHEN gender='F' THEN 1 ELSE 0 END) as female
        FROM voters GROUP BY area, bhag_no ORDER BY area, bhag_no
    """).fetchall()

    result = []
    for b in booths:
        loc = get_booth_location(b['area'], b['bhag_no'])
        result.append({
            'area': b['area'],
            'bhag_no': b['bhag_no'],
            'total': b['total'],
            'male': b['male'],
            'female': b['female'],
            'location_gujarati': loc['gujarati'],
            'location_english': loc['english'],
            'village': loc['village'],
        })

    conn.close()
    return jsonify(result)


@app.route('/api/booth/<area>/<int:bhag_no>')
def api_booth_detail(area, bhag_no):
    """Get detailed voter list for a specific booth."""
    conn = get_db()

    voters = conn.execute("""
        SELECT serial_no, epic, name_ocr, surname_ocr, relation_name_ocr,
               relation_type, house_no, age, gender, section_garbled
        FROM voters WHERE area=? AND bhag_no=?
        ORDER BY serial_no
    """, (area, bhag_no)).fetchall()

    loc = get_booth_location(area, bhag_no)

    # Jaati breakdown for this booth
    jaati_counts = Counter()
    voter_list = []
    for v in voters:
        surname = v['surname_ocr'] or ''
        jaati = classify_surname(surname)
        jaati_counts[jaati] += 1
        voter_list.append({
            'serial_no': v['serial_no'],
            'epic': v['epic'],
            'name': v['name_ocr'] or '(OCR pending)',
            'surname': surname,
            'relation_name': v['relation_name_ocr'] or '',
            'relation_type': v['relation_type'] or '',
            'house_no': v['house_no'] or '',
            'age': v['age'],
            'gender': v['gender'],
            'jaati': jaati,
            'jaati_english': get_jaati_english(jaati),
        })

    # Age breakdown
    age_groups = Counter()
    for v in voters:
        age = v['age']
        if 18 <= age <= 25: age_groups['18-25'] += 1
        elif 26 <= age <= 35: age_groups['26-35'] += 1
        elif 36 <= age <= 45: age_groups['36-45'] += 1
        elif 46 <= age <= 55: age_groups['46-55'] += 1
        elif 56 <= age <= 65: age_groups['56-65'] += 1
        elif age > 65: age_groups['65+'] += 1

    conn.close()

    jaati_data = [{'jaati': k, 'english': get_jaati_english(k), 'count': c,
                   'color': get_jaati_color(k)} for k, c in jaati_counts.most_common()]

    return jsonify({
        'area': area,
        'bhag_no': bhag_no,
        'location': loc,
        'total': len(voter_list),
        'voters': voter_list,
        'jaati_breakdown': jaati_data,
        'age_groups': dict(age_groups),
        'male': sum(1 for v in voter_list if v['gender'] == 'M'),
        'female': sum(1 for v in voter_list if v['gender'] == 'F'),
    })


@app.route('/api/search')
def api_search():
    """Search voters by EPIC, name, or surname."""
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])

    conn = get_db()

    # Try EPIC search first
    if q.upper().startswith(('SIS', 'KJR', 'GJ/')):
        voters = conn.execute("""
            SELECT serial_no, epic, name_ocr, surname_ocr, area, bhag_no,
                   age, gender, house_no, relation_name_ocr, relation_type
            FROM voters WHERE epic LIKE ? LIMIT 50
        """, (f'%{q.upper()}%',)).fetchall()
    else:
        # Name/surname search
        voters = conn.execute("""
            SELECT serial_no, epic, name_ocr, surname_ocr, area, bhag_no,
                   age, gender, house_no, relation_name_ocr, relation_type
            FROM voters WHERE name_ocr LIKE ? OR surname_ocr LIKE ? LIMIT 100
        """, (f'%{q}%', f'%{q}%')).fetchall()

    result = []
    for v in voters:
        surname = v['surname_ocr'] or ''
        jaati = classify_surname(surname)
        result.append({
            'serial_no': v['serial_no'],
            'epic': v['epic'],
            'name': v['name_ocr'] or '(OCR pending)',
            'surname': surname,
            'area': v['area'],
            'bhag_no': v['bhag_no'],
            'age': v['age'],
            'gender': v['gender'],
            'house_no': v['house_no'] or '',
            'relation_name': v['relation_name_ocr'] or '',
            'relation_type': v['relation_type'] or '',
            'jaati': jaati,
            'jaati_english': get_jaati_english(jaati),
        })

    conn.close()
    return jsonify(result)


@app.route('/api/jaati_summary')
def api_jaati_summary():
    """Get jaati-wise breakdown across all booths."""
    conn = get_db()

    voters = conn.execute("SELECT surname_ocr, area, bhag_no FROM voters").fetchall()
    conn.close()

    overall = Counter()
    by_area = defaultdict(Counter)
    by_booth = defaultdict(Counter)

    for v in voters:
        surname = v['surname_ocr'] or ''
        jaati = classify_surname(surname)
        overall[jaati] += 1
        by_area[v['area']][jaati] += 1
        by_booth[(v['area'], v['bhag_no'])][jaati] += 1

    result = {
        'overall': [{'jaati': k, 'english': get_jaati_english(k), 'count': c,
                      'color': get_jaati_color(k)} for k, c in overall.most_common()],
        'by_area': {},
        'by_booth': {},
    }

    for area, counts in sorted(by_area.items()):
        result['by_area'][area] = [{'jaati': k, 'english': get_jaati_english(k),
                                     'count': c, 'color': get_jaati_color(k)}
                                    for k, c in counts.most_common()]

    for (area, bhag), counts in sorted(by_booth.items()):
        key = f"{area}_{bhag}"
        result['by_booth'][key] = [{'jaati': k, 'english': get_jaati_english(k),
                                     'count': c, 'color': get_jaati_color(k)}
                                    for k, c in counts.most_common()]

    return jsonify(result)


@app.route('/api/age_breakdown')
def api_age_breakdown():
    """Get age-wise breakdown."""
    conn = get_db()

    data = conn.execute("""
        SELECT area, bhag_no, gender,
            SUM(CASE WHEN age BETWEEN 18 AND 25 THEN 1 ELSE 0 END) as g18_25,
            SUM(CASE WHEN age BETWEEN 26 AND 35 THEN 1 ELSE 0 END) as g26_35,
            SUM(CASE WHEN age BETWEEN 36 AND 45 THEN 1 ELSE 0 END) as g36_45,
            SUM(CASE WHEN age BETWEEN 46 AND 55 THEN 1 ELSE 0 END) as g46_55,
            SUM(CASE WHEN age BETWEEN 56 AND 65 THEN 1 ELSE 0 END) as g56_65,
            SUM(CASE WHEN age > 65 THEN 1 ELSE 0 END) as g65plus
        FROM voters WHERE age > 0
        GROUP BY area, bhag_no, gender
    """).fetchall()

    conn.close()
    return jsonify([dict(d) for d in data])


@app.route('/api/worker_distribution')
def api_worker_distribution():
    """Get suggested worker distribution for ~300 karyakartas."""
    total_workers = int(request.args.get('workers', 300))

    conn = get_db()
    booths = conn.execute("""
        SELECT area, bhag_no, COUNT(*) as total FROM voters
        GROUP BY area, bhag_no ORDER BY area, bhag_no
    """).fetchall()

    total_voters = sum(b['total'] for b in booths)

    result = []
    assigned = 0
    for b in booths:
        # Proportional allocation
        workers = max(1, round(b['total'] / total_voters * total_workers))
        assigned += workers

        # Get jaati breakdown for this booth
        voters = conn.execute("""
            SELECT surname_ocr FROM voters WHERE area=? AND bhag_no=?
        """, (b['area'], b['bhag_no'])).fetchall()

        jaati_counts = Counter()
        for v in voters:
            jaati = classify_surname(v['surname_ocr'] or '')
            jaati_counts[jaati] += 1

        loc = get_booth_location(b['area'], b['bhag_no'])

        result.append({
            'area': b['area'],
            'bhag_no': b['bhag_no'],
            'total_voters': b['total'],
            'workers_assigned': workers,
            'voters_per_worker': round(b['total'] / workers) if workers > 0 else b['total'],
            'location': loc['english'],
            'top_jaatis': [{'jaati': k, 'english': get_jaati_english(k), 'count': c}
                          for k, c in jaati_counts.most_common(5)],
        })

    # Adjust if total doesn't match
    diff = total_workers - assigned
    if diff != 0 and result:
        # Add/remove from largest booth
        result.sort(key=lambda x: x['total_voters'], reverse=True)
        result[0]['workers_assigned'] += diff
        result[0]['voters_per_worker'] = round(result[0]['total_voters'] / result[0]['workers_assigned'])
        result.sort(key=lambda x: (x['area'], x['bhag_no']))

    conn.close()
    return jsonify({
        'total_workers': total_workers,
        'distribution': result,
    })


@app.route('/api/export_excel')
def api_export_excel():
    """Export all voter data as Excel file."""
    try:
        import openpyxl
    except ImportError:
        return jsonify({'error': 'openpyxl not installed'}), 500

    conn = get_db()
    voters = conn.execute("""
        SELECT * FROM voters ORDER BY area, bhag_no, serial_no
    """).fetchall()
    conn.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "All Voters"

    # Headers
    headers = ['Area', 'Booth', 'Serial', 'EPIC', 'Name', 'Surname', 'Jaati',
               'Father/Husband', 'Relation Type', 'House No', 'Age', 'Gender']
    ws.append(headers)

    for v in voters:
        surname = v['surname_ocr'] or ''
        jaati = classify_surname(surname)
        ws.append([
            v['area'], v['bhag_no'], v['serial_no'], v['epic'],
            v['name_ocr'] or '', surname, get_jaati_english(jaati),
            v['relation_name_ocr'] or '', v['relation_type'] or '',
            v['house_no'] or '', v['age'], v['gender']
        ])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name='Ranoli_Voters_Export.xlsx')


# ============================================================
# Telegram Integration (graceful - works without write access)
# ============================================================
try:
    from telegram_bot import register_telegram_routes, start_telegram_bot, init_reports_db
    register_telegram_routes(app)
    try:
        init_reports_db()
    except Exception:
        pass  # Read-only filesystem on Vercel is OK
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print(f"Starting Election Dashboard...")
    print(f"Database: {DB_PATH}")

    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'

    if debug:
        print(f"Open http://localhost:{port} in your browser")

    # Start Telegram bot if configured
    if TELEGRAM_AVAILABLE:
        if start_telegram_bot():
            print(f"Telegram bot is running!")
        else:
            print(f"Telegram bot not configured. Go to Settings tab to set up.")

    app.run(debug=debug, host='0.0.0.0', port=port)
