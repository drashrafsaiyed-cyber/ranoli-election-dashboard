"""
Surname to Jaati (Caste) Classification Mapping
================================================
For Vadodara/Ranoli area in Gujarat.
Based on common surname-caste associations in this region.

This is an initial mapping that will be refined by the user.
"""

# Primary jaati categories with their common surnames
# Format: 'Surname (Gujarati)': 'Jaati category'

SURNAME_JAATI_MAP = {
    # === PATEL (Patidar) ===
    'પટેલ': 'પટેલ',
    'પતેલ': 'પટેલ',  # OCR variant

    # === THAKOR (Rajput / Kshatriya) ===
    'ઠાકોર': 'ઠાકોર',
    'ઠાકુર': 'ઠાકોર',
    'ઠાકરે': 'ઠાકોર',

    # === GOHIL (Rajput) ===
    'ગોહિલ': 'રાજપૂત',
    'ગોહેલ': 'રાજપૂત',

    # === CHAUHAN (Rajput) ===
    'ચૌહાણ': 'રાજપૂત',
    'ચાવડા': 'રાજપૂત',
    'ચચહાણ': 'રાજપૂત',  # OCR variant
    'ચવહાણ': 'રાજપૂત',  # OCR variant

    # === SOLANKI (Rajput) ===
    'સોલંકી': 'રાજપૂત',

    # === PARMAR (Rajput) ===
    'પરમાર': 'રાજપૂત',

    # === RATHOD (Rajput) ===
    'રાઠોડ': 'રાજપૂત',
    'રાઠોડી': 'રાજપૂત',

    # === VAGHELA (Rajput) ===
    'વાઘેલા': 'રાજપૂત',

    # === PADHIYAR (Rajput) ===
    'પઢિયાર': 'રાજપૂત',
    'પડિયાર': 'રાજપૂત',
    'પઢીયાર': 'રાજપૂત',

    # === JADEJA (Rajput) ===
    'જાડેજા': 'રાજપૂત',

    # === ZALA (Rajput) ===
    'ઝાલા': 'રાજપૂત',

    # === MAKWANA (Rajput) ===
    'મકવાણા': 'રાજપૂત',

    # === SISODIYA (Rajput) ===
    'સિસોદિયા': 'રાજપૂત',

    # === BRAHMIN ===
    'પંડ્યા': 'બ્રાહ્મણ',
    'દવે': 'બ્રાહ્મણ',
    'જોશી': 'બ્રાહ્મણ',
    'શુક્લ': 'બ્રાહ્મણ',
    'ત્રિવેદી': 'બ્રાહ્મણ',
    'ચતુર્વેદી': 'બ્રાહ્મણ',
    'વ્યાસ': 'બ્રાહ્મણ',
    'ઉપાધ્યાય': 'બ્રાહ્મણ',
    'પાઠક': 'બ્રાહ્મણ',
    'શાસ્ત્રી': 'બ્રાહ્મણ',
    'મહેતા': 'બ્રાહ્મણ',
    'પુરોહિત': 'બ્રાહ્મણ',
    'ભટ્ટ': 'બ્રાહ્મણ',
    'રાવલ': 'બ્રાહ્મણ',
    'દીક્ષિત': 'બ્રાહ્મણ',
    'નાગર': 'બ્રાહ્મણ',
    'ગોર': 'બ્રાહ્મણ',

    # === PRAJAPATI (OBC) ===
    'પ્રજાપતિ': 'પ્રજાપતિ',
    'કુંભાર': 'પ્રજાપતિ',

    # === VANKAR (SC) ===
    'વણકર': 'વણકર',
    'રોહિત': 'વણકર',

    # === CHAMAR (SC) ===
    'ચમાર': 'ચમાર',

    # === VALMIKI (SC) ===
    'વાલ્મીકી': 'વાલ્મીકી',
    'મેહતર': 'વાલ્મીકી',

    # === RABARI / DESAI ===
    'રબારી': 'રબારી',
    'દેસાઈ': 'રબારી',

    # === BHARWAD (OBC) ===
    'ભરવાડ': 'ભરવાડ',

    # === DARBAR / DARJI ===
    'દરબાર': 'દરબાર',
    'દરજી': 'દરજી',

    # === MUSLIM ===
    'ખાન': 'મુસ્લિમ',
    'શેખ': 'મુસ્લિમ',
    'સૈયદ': 'મુસ્લિમ',
    'પઠાણ': 'મુસ્લિમ',
    'મલેક': 'મુસ્લિમ',
    'મલિક': 'મુસ્લિમ',
    'મન્સૂરી': 'મુસ્લિમ',
    'વહોરા': 'મુસ્લિમ',
    'મોમીન': 'મુસ્લિમ',
    'કુરેશી': 'મુસ્લિમ',
    'અન્સારી': 'મુસ્લિમ',
    'રાજપુત': 'મુસ્લિમ',  # Muslim Rajput (context dependent)
    'મિર્ઝા': 'મુસ્લિમ',
    'મુલ્લા': 'મુસ્લિમ',
    'ગિલાની': 'મુસ્લિમ',

    # === CHRISTIAN ===
    'ક્રિશ્ચિયન': 'ખ્રિસ્તી',

    # === SINDHI ===
    'ચાવલા': 'સિંધી',
    'લાલવાણી': 'સિંધી',

    # === VASAVA (ST - Adivasi) ===
    'વસાવા': 'આદિવાસી',
    'ભીલ': 'આદિવાસી',
    'ભીલબારીયા': 'આદિવાસી',
    'તડવી': 'આદિવાસી',
    'નાયકા': 'આદિવાસી',
    'રાઠવા': 'આદિવાસી',
    'ડામોર': 'આદિવાસી',
    'બારીયા': 'આદિવાસી',

    # === SUTHAR (OBC) ===
    'સુથાર': 'સુથાર',

    # === SONI (OBC) ===
    'સોની': 'સોની',

    # === LUHAR (OBC) ===
    'લુહાર': 'લુહાર',
    'લોહાર': 'લુહાર',

    # === KOLI (OBC) ===
    'કોળી': 'કોળી',
    'કોલી': 'કોળી',

    # === MALI (OBC) ===
    'માળી': 'માળી',

    # === NAIR ===
    'નાયર': 'નાયર',

    # === HARIJAN (SC - general) ===
    'હરિજન': 'હરિજન',

    # === THAKKAR ===
    'ઠક્કર': 'ઠક્કર',

    # === SONI ===
    'સોની': 'સોની',

    # === SAMATYANI / SAMANI ===
    'સામત્યાની': 'અન્ય',

    # === PRASAD ===
    'પ્રસાદ': 'અન્ય',

    # === RAOUT ===
    'રાઉત': 'અન્ય',

    # === BENARJI ===
    'બેનરજી': 'બ્રાહ્મણ',

    # === YADAV ===
    'યાદવ': 'યાદવ',

    # === BARBER ===
    'વાળંદ': 'વાળંદ',
    'નાઈ': 'નાઈ',

    # === KUMHAR ===
    'કુંભાર': 'પ્રજાપતિ',

    # === MODI ===
    'મોદી': 'વાણિયા',

    # === SHAH ===
    'શાહ': 'વાણિયા',

    # === VAISHNAV / BANIA ===
    'વૈષ્ણવ': 'વાણિયા',

    # === MAJHI ===
    'માઝી': 'અન્ય',
    'મોજ': 'અન્ય',

    # === GAHLOT ===
    'ગહલોત': 'રાજપૂત',

    # === PAHADIYA ===
    'પહાડિયા': 'અન્ય',

    # === POLLY ===
    'પોલ્લી': 'અન્ય',
    'પોલી': 'અન્ય',

    # === DAMAPURA / local surnames ===
    'દામાપુરા': 'અન્ય',

    # === SENMA (OBC) ===
    'સેનમા': 'OBC',

    # === EXPANDED MAPPINGS (from actual voter data analysis) ===

    # Rajput / Kshatriya (OCR variants + additional surnames)
    'ગોહીલ': 'રાજપૂત',  # OCR variant of ગોહિલ
    'પવાર': 'રાજપૂત',
    'રાણા': 'રાજપૂત',
    'મહિડા': 'રાજપૂત',
    'ચૌધરી': 'રાજપૂત',
    'ચૌધર': 'રાજપૂત',  # OCR truncated
    'સિંહ': 'રાજપૂત',
    'ડાભ': 'રાજપૂત',
    'ડાભી': 'રાજપૂત',
    'ગિરી': 'રાજપૂત',
    'ગિર': 'રાજપૂત',  # OCR truncated
    'સરવૈયા': 'રાજપૂત',

    # Brahmin (expanded)
    'શર્મા': 'બ્રાહ્મણ',
    'પાંડે': 'બ્રાહ્મણ',
    'પંડે': 'બ્રાહ્મણ',
    'મિશ્રા': 'બ્રાહ્મણ',
    'તિવારી': 'બ્રાહ્મણ',
    'તિવાર': 'બ્રાહ્મણ',  # OCR truncated
    'ભટ્ટ': 'બ્રાહ્મણ',
    'ભટૃ': 'બ્રાહ્મણ',  # OCR variant
    'પારેખ': 'બ્રાહ્મણ',
    'જોશી': 'બ્રાહ્મણ',
    'જોષ': 'બ્રાહ્મણ',  # OCR truncated
    'રાવળ': 'બ્રાહ્મણ',
    'રાવલ': 'બ્રાહ્મણ',
    'ગુપ્તા': 'વાણિયા',

    # Prajapati / Kumhar
    'પંચાલ': 'પ્રજાપતિ',

    # Barber
    'નાયી': 'નાઈ',
    'નાય': 'નાઈ',  # OCR truncated

    # Soni
    'સોન': 'સોની',  # OCR truncated
    'સોનાર': 'સોની',

    # Darji
    'દર': 'દરજી',  # OCR truncated - context dependent but most common
    'ટેલર': 'દરજી',

    # Vankar / SC
    'વાદ': 'વણકર',  # OCR truncated variant
    'વણઝારા': 'વણઝારા',

    # Baroti / Charan
    'બારોટ': 'બારોટ',

    # Harijan (OCR variant)
    'હરીજન': 'હરિજન',

    # Yadav (OCR variant)
    'જાદવ': 'યાદવ',

    # Adivasi / ST (expanded)
    'તડવ': 'આદિવાસી',  # OCR truncated of તડવી
    'બારિયા': 'આદિવાસી',
    'ખંડવ': 'આદિવાસી',  # OCR truncated

    # Mali
    'માળ': 'માળી',  # OCR truncated
    'માલ': 'માળી',  # OCR truncated

    # Patanvadiya (OBC)
    'પાટણવાડિયા': 'પાટણવાડિયા',
    'પાટણવાડીયા': 'પાટણવાડિયા',

    # Patil
    'પાટીલ': 'પટેલ',

    # Agrawal / Marwadi
    'અગ્રવાલ': 'વાણિયા',
    'અગરવાલ': 'વાણિયા',

    # Verma
    'વર્મા': 'OBC',

    # Dangri
    'ડાંગર': 'ડાંગર',

    # Mistri
    'મિસ્ત્રી': 'મિસ્ત્રી',
    'મિસ્ત્ર': 'મિસ્ત્રી',  # OCR truncated

    # Prasad
    'પ્રસાદ': 'OBC',

    # Karnakal
    'કરણકાળ': 'અન્ય',

    # === MORE EXPANDED (from voter data round 2) ===

    # Vaniya
    'વાણિયા': 'વાણિયા',

    # Rajput variants
    'વાધેલા': 'રાજપૂત',  # OCR variant of વાઘેલા
    'સિંગ': 'રાજપૂત',  # variant of સિંહ
    'જાટ': 'રાજપૂત',

    # Brahmin variants
    'ગોસ્વામી': 'બ્રાહ્મણ',
    'ગોસ્વા': 'બ્રાહ્મણ',  # OCR truncated
    'ભટ': 'બ્રાહ્મણ',  # OCR truncated of ભટ્ટ

    # SC surnames
    'ધોબી': 'SC',
    'ધોબ': 'SC',  # OCR truncated

    # OBC
    'પાલ': 'OBC',
    'સરો': 'OBC',  # might be સરોજ or similar
    'ઘાંચી': 'OBC',
    'ઘાંચ': 'OBC',  # OCR truncated

    # === THAKOR (OBC - Thakor community) ===
    # Note: Thakor can be OBC or Rajput depending on community
}

# Jaati categories with display names and rough proportions
JAATI_CATEGORIES = {
    'પટેલ': {'english': 'Patel (Patidar)', 'color': '#4CAF50'},
    'રાજપૂત': {'english': 'Rajput (Kshatriya)', 'color': '#2196F3'},
    'બ્રાહ્મણ': {'english': 'Brahmin', 'color': '#FF9800'},
    'પ્રજાપતિ': {'english': 'Prajapati (OBC)', 'color': '#9C27B0'},
    'વણકર': {'english': 'Vankar (SC)', 'color': '#F44336'},
    'ચમાર': {'english': 'Chamar (SC)', 'color': '#E91E63'},
    'વાલ્મીકી': {'english': 'Valmiki (SC)', 'color': '#795548'},
    'રબારી': {'english': 'Rabari', 'color': '#607D8B'},
    'ભરવાડ': {'english': 'Bharwad', 'color': '#00BCD4'},
    'આદિવાસી': {'english': 'Adivasi (ST)', 'color': '#8BC34A'},
    'મુસ્લિમ': {'english': 'Muslim', 'color': '#009688'},
    'ખ્રિસ્તી': {'english': 'Christian', 'color': '#3F51B5'},
    'સિંધી': {'english': 'Sindhi', 'color': '#CDDC39'},
    'વાણિયા': {'english': 'Vania (Vaishya)', 'color': '#FFC107'},
    'સોની': {'english': 'Soni', 'color': '#FF5722'},
    'સુથાર': {'english': 'Suthar', 'color': '#673AB7'},
    'લુહાર': {'english': 'Luhar', 'color': '#03A9F4'},
    'કોળી': {'english': 'Koli', 'color': '#FFEB3B'},
    'દરજી': {'english': 'Darji', 'color': '#4DB6AC'},
    'દરબાર': {'english': 'Darbar', 'color': '#7986CB'},
    'ઠાકોર': {'english': 'Thakor', 'color': '#A1887F'},
    'ઠક્કર': {'english': 'Thakkar', 'color': '#90A4AE'},
    'માળી': {'english': 'Mali', 'color': '#AED581'},
    'હરિજન': {'english': 'Harijan (SC)', 'color': '#CE93D8'},
    'યાદવ': {'english': 'Yadav', 'color': '#80CBC4'},
    'વાળંદ': {'english': 'Valand (Barber)', 'color': '#BCAAA4'},
    'નાઈ': {'english': 'Nai', 'color': '#B0BEC5'},
    'વણઝારા': {'english': 'Vanzara', 'color': '#EF5350'},
    'બારોટ': {'english': 'Barot (Charan)', 'color': '#AB47BC'},
    'પાટણવાડિયા': {'english': 'Patanvadiya', 'color': '#5C6BC0'},
    'ડાંગર': {'english': 'Dangar', 'color': '#26A69A'},
    'મિસ્ત્રી': {'english': 'Mistri', 'color': '#8D6E63'},
    'SC': {'english': 'SC (Other)', 'color': '#D32F2F'},
    'OBC': {'english': 'OBC (Other)', 'color': '#78909C'},
    'અન્ય': {'english': 'Other', 'color': '#9E9E9E'},
}


def classify_surname(surname):
    """
    Classify a surname into a jaati category.
    Returns jaati name in Gujarati, or 'અન્ય' (Other) if not found.
    """
    if not surname:
        return 'અન્ય'

    surname = surname.strip()

    # Skip OCR noise (single chars, symbols, punctuation)
    if len(surname) <= 1 or all(c in '—-:|;,./\\"\'()[]{}0123456789 ' for c in surname):
        return 'અન્ય'

    # Direct match
    if surname in SURNAME_JAATI_MAP:
        return SURNAME_JAATI_MAP[surname]

    # Try fuzzy match on first 3-4 chars for OCR truncation
    if len(surname) >= 3:
        for key, val in SURNAME_JAATI_MAP.items():
            if len(key) >= 3:
                # Match if surname starts with key or key starts with surname
                if len(surname) >= 4 and len(key) >= 4 and surname[:4] == key[:4]:
                    return val
                elif len(surname) == 3 and surname[:3] == key[:3]:
                    return val

    return 'અન્ય'


def get_jaati_english(jaati_gujarati):
    """Get English name for a jaati category."""
    if jaati_gujarati in JAATI_CATEGORIES:
        return JAATI_CATEGORIES[jaati_gujarati]['english']
    return 'Other'


def get_jaati_color(jaati_gujarati):
    """Get display color for a jaati category."""
    if jaati_gujarati in JAATI_CATEGORIES:
        return JAATI_CATEGORIES[jaati_gujarati]['color']
    return '#9E9E9E'
