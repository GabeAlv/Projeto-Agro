"""
Módulo de Banco de Dados SQLite (Estrutura e Esquema).
Pronto para ser ativado quando os dados deixarem de ser mockados.
"""
import sqlite3
import os

DB_PATH = "agro_dashboard.db"


def init_db():
    """Inicializa as tabelas no banco SQLite se não existirem."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de Talhões
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS talhoes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            area TEXT NOT NULL,
            crop TEXT NOT NULL,
            color TEXT NOT NULL,
            is_dashed INTEGER DEFAULT 0
        )
    """)

    # Tabela de Condições Meteorológicas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature TEXT NOT NULL,
            weather_status TEXT NOT NULL,
            forecast_note TEXT NOT NULL,
            humidity TEXT NOT NULL,
            wind_speed TEXT NOT NULL,
            insolation TEXT NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de Notificações / Alertas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            icon TEXT NOT NULL,
            color TEXT NOT NULL,
            bg_color TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            source_tag TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de Leituras Históricas de Sensores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            reading_value REAL NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def seed_mock_data():
    """Preenche o SQLite com a carga inicial de dados padrão para testes."""
    from mock_data import SPATIAL_DATA, NOTIFICATIONS_DATA

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Seed Talhões
    for t in SPATIAL_DATA["talhoes"]:
        cursor.execute("""
            INSERT OR REPLACE INTO talhoes (id, name, status, area, crop, color, is_dashed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (t["id"], t["name"], t["status"], t["area"], t["crop"], t["color"], 1 if t.get("is_dashed") else 0))

    # Seed Notificações
    for n in NOTIFICATIONS_DATA["items"]:
        cursor.execute("""
            INSERT OR REPLACE INTO notifications (id, type, icon, color, bg_color, title, location, source_tag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (n["id"], n["type"], str(n["icon"]), n["color"], n["bg_color"], n["title"], n["location"], n["source_tag"]))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_mock_data()
    print("Banco de dados SQLite inicializado e populado com sucesso!")
