from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)
app.secret_key = 'FnDbezjkkNcX8Fv6u4RGePqoTqvZAKxVDgqeAiZs'  # Ganti dengan secret key asli

# Firebase init
cred = credentials.Certificate("D:\project111-web\project111-aa20b-firebase-adminsdk-8a3ea-0317271ecc.json")  # Ganti sesuai file json kamu
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project111-aa20b-default-rtdb.firebaseio.com/'
})

users_ref = db.reference('users')

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        konfirmasi = request.form['konfirmasi'].strip()
        nomor_hp = request.form['nomor_hp'].strip()

        if not username or not password or not konfirmasi or not nomor_hp:
            return "Ada data yang kosong!", 400
        if password != konfirmasi:
            return "Konfirmasi password tidak sesuai!", 400

        user = users_ref.child(username).get()
        if user:
            return "Username sudah terdaftar!", 400

        users_ref.child(username).set({
            'username': username,
            'password': password,
            'nomorHp': nomor_hp
        })

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            return "Username dan password wajib diisi!", 400

        user = users_ref.child(username).get()
        if not user:
            return "Data tidak ditemukan!", 404

        if user['password'] != password:
            return "Password salah!", 401

        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f"Selamat datang, {session['username']}!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# API Endpoint (optional)
@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    user = users_ref.child(username).get()
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# Run server
if __name__ == '__main__':
    app.run(debug=True)
