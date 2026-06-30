import sqlite3
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # تفعيل CORS للسماح بالاتصال من تطبيقات فلاتر ويب وموبايل

DB_FILE = 'database.db'

# دالة للاتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # للوصول للأعمدة بأسماء المفاتيح
    return conn

# دالة لتشفير كلمات المرور باستخدام SHA-256 (مدمجة ولا تحتاج لمكاتب خارجية)
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# تهيئة قاعدة البيانات وإنشاء الجداول إذا لم تكن موجودة
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # 2. جدول الحجوزات الطبية
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            doctor_specialty TEXT NOT NULL,
            doctor_image TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 3. جدول التقارير والتحاليل الطبية
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            doctor TEXT NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# ----------------- منافذ الـ API (Endpoints) -----------------

# 1. تسجيل مستخدم جديد
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'message': 'جميع الحقول مطلوبة!'}), 400
        
    hashed = hash_password(password)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed)
        )
        conn.commit()
        
        # جلب المعرف المضاف تلقائياً
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'message': 'تم إنشاء الحساب بنجاح!',
            'user': {
                'id': user_id,
                'name': name,
                'email': email
            }
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'البريد الإلكتروني مسجل بالفعل!'}), 400

# 2. تسجيل الدخول
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'البريد الإلكتروني وكلمة المرور مطلوبان!'}), 400
        
    hashed = hash_password(password)
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND password = ?',
        (email, hashed)
    ).fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'message': 'تم تسجيل الدخول بنجاح!',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            },
            'token': f"user-token-{user['id']}" # رمز أمان وهمي للتبسيط
        }), 200
    else:
        return jsonify({'message': 'البريد الإلكتروني أو كلمة المرور غير صحيحة!'}), 401

# 3. جلب الحجوزات الطبية الخاصة بالمستخدم
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'معرف المستخدم (user_id) مطلوب!'}), 400
        
    conn = get_db_connection()
    bookings = conn.execute(
        'SELECT * FROM bookings WHERE user_id = ? ORDER BY id DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    
    result = []
    for b in bookings:
        result.append({
            'id': b['id'],
            'doctorName': b['doctor_name'],
            'doctorSpecialty': b['doctor_specialty'],
            'doctorImage': b['doctor_image'],
            'date': b['date'],
            'time': b['time']
        })
        
    return jsonify(result), 200

# 4. إضافة حجز طبي جديد
@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    user_id = data.get('user_id')
    doctor_name = data.get('doctorName')
    doctor_specialty = data.get('doctorSpecialty')
    doctor_image = data.get('doctorImage')
    date = data.get('date')
    time = data.get('time')
    
    if not user_id or not doctor_name or not date or not time:
        return jsonify({'message': 'بيانات الحجز غير مكتملة!'}), 400
        
    conn = get_db_connection()
    conn.execute(
        '''INSERT INTO bookings (user_id, doctor_name, doctor_specialty, doctor_image, date, time)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (user_id, doctor_name, doctor_specialty, doctor_image, date, time)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'تم حفظ الحجز بنجاح!'}), 201

# 5. جلب التقارير والتحاليل الطبية الخاصة بالمستخدم
@app.route('/api/records', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'معرف المستخدم (user_id) مطلوب!'}), 400
        
    conn = get_db_connection()
    records = conn.execute(
        'SELECT * FROM records WHERE user_id = ? ORDER BY id DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    
    result = []
    for r in records:
        result.append({
            'id': r['id'],
            'title': r['title'],
            'doctor': r['doctor'],
            'date': r['date'],
            'type': r['type']
        })
        
    return jsonify(result), 200

# 6. إضافة تقرير طبي جديد
@app.route('/api/records', methods=['POST'])
def create_record():
    data = request.json
    user_id = data.get('user_id')
    title = data.get('title')
    doctor = data.get('doctor')
    date = data.get('date')
    file_type = data.get('type')
    
    if not user_id or not title or not doctor or not file_type:
        return jsonify({'message': 'بيانات التقرير غير مكتملة!'}), 400
        
    conn = get_db_connection()
    conn.execute(
        '''INSERT INTO records (user_id, title, doctor, date, type)
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, title, doctor, date, file_type)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'تم حفظ التقرير الطبي بنجاح!'}), 201

if __name__ == '__main__':
    init_db()
    # تشغيل السيرفر على جميع الـ IPs بالشبكة المحلية بمنفذ 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
