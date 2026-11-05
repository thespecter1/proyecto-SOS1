from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='')

# Database Initialization
def init_db():
    conn = sqlite3.connect('emergencias.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            edad INTEGER,
            telefono TEXT,
            tipo_usuario TEXT,
            resumen_emergencia TEXT,
            latitud REAL,
            longitud REAL,
            fecha_hora TEXT,
            recomendacion_ia TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def simular_recomendacion_ia(resumen):
    resumen_lower = resumen.lower()
    if "fuego" in resumen_lower or "incendio" in resumen_lower or "humo" in resumen_lower:
        return "ALERTA ROJA: Bomberos notificados. Evacue inmediatamente por las escaleras mas cercanas. No use ascensores. Cubra su boca si hay humo."
    elif "robo" in resumen_lower or "asalto" in resumen_lower or "arma" in resumen_lower:
        return "ALERTA ROJA: Seguridad del campus notificada. Resguardese en un area segura, bloquee puertas si es posible y evite confrontar a los sospechosos."
    elif "desmayo" in resumen_lower or "herida" in resumen_lower or "sangre" in resumen_lower or "salud" in resumen_lower or "choque" in resumen_lower or "cai" in resumen_lower or "caida" in resumen_lower or "rompi" in resumen_lower or "hueso" in resumen_lower or "cabeza" in resumen_lower or "pierna" in resumen_lower or "brazo" in resumen_lower or "duele" in resumen_lower:
        return "ALERTA MEDICA: Paramedicos en camino. Manténgase inmóvil si sospecha de una fractura o lesión grave en la cabeza/cuello. Verifique si la persona respira y NO la mueva a menos que haya un peligro inminente."
    else:
        return "EVALUACIÓN IA: Hemos analizado su reporte. Le recomendamos mantenerse en una zona segura y visible. Hemos transmitido sus datos al equipo de respuesta rápida. Por favor, mantenga la calma y espere instrucciones."

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/api/sos', methods=['POST'])
def handle_sos():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    nombre = data.get('nombre', 'Desconocido')
    apellido = data.get('apellido', 'Desconocido')
    edad = data.get('edad', 0)
    telefono = data.get('telefono', '0000')
    tipo_usuario = data.get('tipo_usuario', 'Afectado')
    resumen = data.get('resumen', '')
    
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. IA procesa y genera recomendacion
    recomendacion = simular_recomendacion_ia(resumen)
    
    # 2. Guardar en SQLite
    conn = sqlite3.connect('emergencias.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO alertas (nombre, apellido, edad, telefono, tipo_usuario, resumen_emergencia, latitud, longitud, fecha_hora, recomendacion_ia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, apellido, edad, telefono, tipo_usuario, resumen, lat, lng, fecha_hora, recomendacion))
    conn.commit()
    conn.close()
    
    print(f"==========================================")
    print(f"NUEVA ALERTA SOS: {fecha_hora}")
    print(f"Usuario: {nombre} {apellido} ({tipo_usuario}) - Telf: {telefono}")
    print(f"Resumen: {resumen}")
    print(f"Recomendacion enviada: {recomendacion}")
    print(f"==========================================")
    
    # 3. Respuesta con recomendaciones de la IA
    return jsonify({
        "status": "success",
        "recomendacion": recomendacion
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
