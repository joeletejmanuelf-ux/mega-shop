from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Tabela de megas
tabela = {
    13: 512, 25: 1024, 38: 1536, 50: 2048,
    75: 3072, 100: 4096, 125: 5120, 150: 6144,
    200: 8192, 250: 10240, 500: 20400,
    60: 1700, 110: 3400, 165: 5200, 220: 7100,
    320: 10700, 180: 5120, 215: 7168, 225: 8000,
    300: 10240, 320: 10752, 590: 20480
}

# Inicializar banco de dados


def init_db():
    conn = sqlite3.connect("loja.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            numero TEXT,
            saldo REAL
        )
    ''')
    conn.commit()
    conn.close()


init_db()

# Página inicial


@app.route("/")
def index():
    conn = sqlite3.connect("loja.db")
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clientes = c.fetchall()
    conn.close()
    return render_template("index.html", clientes=clientes)

# Adicionar cliente


@app.route("/add", methods=["POST"])
def add():
    nome = request.form["nome"]
    numero = request.form["numero"]
    saldo = float(request.form["saldo"])
    conn = sqlite3.connect("loja.db")
    c = conn.cursor()
    c.execute("INSERT INTO clientes (nome, numero, saldo) VALUES (?, ?, ?)",
              (nome, numero, saldo))
    conn.commit()
    conn.close()
    return redirect("/")

# Comprar megas


@app.route("/comprar", methods=["POST"])
def comprar():
    numero = request.form["numero"]
    valor = int(request.form["valor"])
    conn = sqlite3.connect("loja.db")
    c = conn.cursor()
    c.execute("SELECT saldo FROM clientes WHERE numero=?", (numero,))
    cliente = c.fetchone()
    if not cliente:
        return "❌ Cliente não encontrado"
    saldo = cliente[0]
    if saldo < valor:
        return "❌ Saldo insuficiente"
    novo_saldo = saldo - valor
    c.execute("UPDATE clientes SET saldo=? WHERE numero=?",
              (novo_saldo, numero))
    conn.commit()
    conn.close()
    return f"✅ Compra feita: {tabela.get(valor, 0)} MB | Novo saldo: {novo_saldo} MT"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
