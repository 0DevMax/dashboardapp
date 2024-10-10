import psycopg2
import os
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

# Conexão com o banco de dados
conn = psycopg2.connect(
    database=os.getenv("NAME"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    port=os.getenv("PORT"),
    host=os.getenv("HOST")
)

cursor = conn.cursor()

# Consulta
cursor.execute("SELECT * FROM vendas")

rows = cursor.fetchmany(3)

for row in rows:
    print(row)

conn.close()



####

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)