from app.core.database import engine

try:
    connection = engine.connect()
    print("🔥 Conexão com banco bem-sucedida!")
    connection.close()
except Exception as e:
    print("❌ Erro ao conectar:", e)