from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# قائمة الولايات الـ 58 الكاملة مدمجة في السيرفر
ALGERIA_STATES = [
    {"id": "01", "ar": "أدرار", "fr": "Adrar"}, {"id": "02", "ar": "الشلف", "fr": "Chlef"},
    {"id": "03", "ar": "الأغواط", "fr": "Laghouat"}, {"id": "04", "ar": "أم البواقي", "fr": "Oum El Bouaghi"},
    {"id": "05", "ar": "باتنة", "fr": "Batna"}, {"id": "06", "ar": "بجاية", "fr": "Béjaïa"},
    {"id": "07", "ar": "بسكرة", "fr": "Biskra"}, {"id": "08", "ar": "بشار", "fr": "Béchar"},
    {"id": "09", "ar": "البليدة", "fr": "Blida"}, {"id": "10", "ar": "البويرة", "fr": "Bouira"},
    {"id": "11", "ar": "تمنراست", "fr": "Tamanrasset"}, {"id": "12", "ar": "تبسة", "fr": "Tébessa"},
    {"id": "13", "ar": "تلمسان", "fr": "Tlemcen"}, {"id": "14", "ar": "تيارت", "fr": "Tiaret"},
    {"id": "15", "ar": "تيزي وزو", "fr": "Tizi Ouzou"}, {"id": "16", "ar": "الجزائر", "fr": "Alger"},
    {"id": "17", "ar": "الجلفة", "fr": "Djelfa"}, {"id": "18", "ar": "جيجل", "fr": "Jijel"},
    {"id": "19", "ar": "سطيف", "fr": "Sétif"}, {"id": "20", "ar": "سعيدة", "fr": "Saïda"},
    {"id": "21", "ar": "سكيكدة", "fr": "Skikda"}, {"id": "22", "ar": "سيدي بلعباس", "fr": "Sidi Bel Abbès"},
    {"id": "23", "ar": "عنابة", "fr": "Annaba"}, {"id": "24", "ar": "قالمة", "fr": "Guelma"},
    {"id": "25", "ar": "قسنطينة", "fr": "Constantine"}, {"id": "26", "ar": "المدية", "fr": "Médéa"},
    {"id": "27", "ar": "مستغانم", "fr": "Mostaganem"}, {"id": "28", "ar": "المسيلة", "fr": "M'Sila"},
    {"id": "29", "ar": "معسكر", "fr": "Mascara"}, {"id": "30", "ar": "ورقلة", "fr": "Ouargla"},
    {"id": "31", "ar": "وهران", "fr": "Oran"}, {"id": "32", "ar": "البيض", "fr": "El Bayadh"},
    {"id": "33", "ar": "إليزي", "fr": "Illizi"}, {"id": "34", "ar": "برج بوعريريج", "fr": "B.B. Arréridj"},
    {"id": "35", "ar": "بومرداس", "fr": "Boumerdès"}, {"id": "36", "ar": "الطارف", "fr": "El Tarf"},
    {"id": "37", "ar": "تندوف", "fr": "Tindouf"}, {"id": "38", "ar": "تيسمسيلت", "fr": "Tissemsilt"},
    {"id": "39", "ar": "الوادي", "fr": "El Oued"}, {"id": "40", "ar": "خنشلة", "fr": "Khenchela"},
    {"id": "41", "ar": "سوق أهراس", "fr": "Souk Ahras"}, {"id": "42", "ar": "تيبازة", "fr": "Tipaza"},
    {"id": "43", "ar": "ميلة", "fr": "Mila"}, {"id": "44", "ar": "عين الدفلى", "fr": "Aïn Defla"},
    {"id": "45", "ar": "النعامة", "fr": "Naâma"}, {"id": "46", "ar": "عين تموشنت", "fr": "Aïn Témouchent"},
    {"id": "47", "ar": "غرداية", "fr": "Ghardaïa"}, {"id": "48", "ar": "غليزان", "fr": "Relizane"},
    {"id": "49", "ar": "تيميمون", "fr": "Timimoun"}, {"id": "50", "ar": "برج باجي مختار", "fr": "B.B.M."},
    {"id": "51", "ar": "أولاد جلال", "fr": "Ouled Djellal"}, {"id": "52", "ar": "بني عباس", "fr": "Béni Abbès"},
    {"id": "53", "ar": "عين صالح", "fr": "In Salah"}, {"id": "54", "ar": "عين قزام", "fr": "In Guezzam"},
    {"id": "55", "ar": "تقرت", "fr": "Touggourt"}, {"id": "56", "ar": "جانت", "fr": "Djanet"},
    {"id": "57", "ar": "المغير", "fr": "El M'Ghair"}, {"id": "58", "ar": "المنيعة", "fr": "El Meniaa"}
]

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS doctors 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, state TEXT, specialty TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html', states=ALGERIA_STATES)

@app.route('/api/register', methods=['POST'])
def register():
    # حماية Honeypot ضد الروبوتات
    if request.form.get('extra_field'):
        return "Bot Blocked", 403
    
    name = request.form.get('name')
    state = request.form.get('state')
    spec = request.form.get('specialty')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO doctors (name, state, specialty) VALUES (?, ?, ?)", (name, state, spec))
    conn.commit()
    conn.close()
    
    return "<h1>تم التسجيل بنجاح يا دكتور! موقع أيوب يرحب بك.</h1><a href='/'>العودة للرئيسية</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)