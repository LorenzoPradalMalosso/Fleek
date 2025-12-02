from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re
import dns.resolver
import osc
print("Templates path:", os.listdir("templates"))


# --- Configuração ---
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "segredo_top"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# --- Validações ---
def email_valido(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email)

def dominio_tem_mx(email):
    try:
        dominio = email.split('@')[-1]
        dns.resolver.resolve(dominio, "MX")
        return True
    except Exception:
        return False

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        con.commit()

init_db()

# --- ROTAS ---

@app.route("/")
def login():
    # --- MUDANÇA AQUI: ---
    # Em vez de checar se está logado e redirecionar para home,
    # nós limpamos a sessão. Assim, acessar "/" sempre desloga o usuário.
    session.pop("user", None) 
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_user():
    email = request.form["email"]
    password = request.form["password"]

    if not email_valido(email):
        flash("E-mail inválido!", "error")
        return redirect("/")

    # Validação de MX comentada para agilidade nos testes
    # if not dominio_tem_mx(email):
    #     flash("Domínio de e-mail não existe!", "error")
    #     return redirect("/")

    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("SELECT email, password FROM users WHERE email = ?", (email,))
        user = cur.fetchone()

    if user and check_password_hash(user[1], password):
        session["user"] = email
        return redirect("/home")
    else:
        flash("Email ou senha incorretos!", "error")
        return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_user():
    email = request.form["email"]
    password = request.form["password"]

    if not email_valido(email):
        flash("E-mail inválido!", "error")
        return redirect("/register")

    password_hash = generate_password_hash(password)

    try:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password_hash))
            con.commit()

        flash("Conta criada com sucesso!", "success")
        return redirect("/")
    
    except sqlite3.IntegrityError:
        flash("E-mail já está em uso!", "error")
        return redirect("/register")

@app.route("/home")
def home():
    if "user" in session:
        # Certifique-se que o arquivo na sua pasta é index.html
        return render_template("index.html")
    
    # Se tentar acessar /home direto sem logar, joga pro login
    return redirect("/")

@app.route("/conta")
def conta():
    print("Templates path:", os.listdir("templates"))
    return render_template("conta.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":

    app.run(debug=True)

