from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

def db():
    return sqlite3.connect("tickets.db")

# Create DB
conn = db()
conn.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY, name TEXT, email TEXT, issue TEXT, status TEXT)")
conn.commit()
conn.close()

# Logo SVG
logo = """
<svg width="120" height="120" viewBox="0 0 100 100">
<g fill="gold">
<polygon points="50,5 55,35 45,35"/>
<rect x="48" y="35" width="4" height="40"/>
<circle cx="50" cy="80" r="8"/>
</g>
</svg>
"""

# Base Layout
def layout(content):
    return f"""
    <html>
    <head>
    <title>RoyalAnchor Support</title>
    <style>

    body {{
        margin:0;
        font-family:Arial;
        background:#0b1f44;
        color:white;
    }}

    nav {{
        background:#081633;
        padding:20px;
        display:flex;
        justify-content:space-between;
        align-items:center;
    }}

    nav a {{
        color:white;
        margin:15px;
        text-decoration:none;
        font-weight:bold;
    }}

    .hero {{
        text-align:center;
        padding:100px;
    }}

    h1 {{
        font-size:60px;
        color:gold;
    }}

    button {{
        padding:15px 30px;
        background:gold;
        border:none;
        font-weight:bold;
        cursor:pointer;
        border-radius:6px;
    }}

    .container {{
        padding:60px;
        max-width:1000px;
        margin:auto;
    }}

    input, textarea {{
        width:100%;
        padding:10px;
        margin:10px 0;
    }}

    </style>
    </head>

    <body>

    <nav>
        <div>{logo} RoyalAnchor</div>

        <div>
            <a href="/">Home</a>
            <a href="/ticket">Submit Ticket</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/careers">Careers</a>
            <a href="/login">Employee</a>
        </div>
    </nav>

    {content}

    </body>
    </html>
    """

# Home Page
@app.route("/")
def home():
    return layout("""
    <div class="hero">
    <h1>RoyalAnchor Support</h1>
    <p>Luxury outsourced technical support for ambitious startups.</p>
    <a href="/ticket"><button>Create Support Ticket</button></a>
    </div>
    """)

# Ticket Submission
@app.route("/ticket", methods=["GET","POST"])
def ticket():

    if request.method == "POST":
        conn = db()
        conn.execute("INSERT INTO tickets (name,email,issue,status) VALUES (?,?,?,?)",
        (request.form["name"],request.form["email"],request.form["issue"],"Open"))
        conn.commit()
        conn.close()
        return layout("<h2>Ticket Submitted Successfully</h2>")

    return layout("""
    <div class="container">
    <h2>Create Ticket</h2>

    <form method="post">

    Name
    <input name="name">

    Email
    <input name="email">

    Issue
    <textarea name="issue"></textarea>

    <button>Submit Ticket</button>

    </form>
    </div>
    """)

# Employee Login
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        if request.form["email"] == "admin@royalanchor.com" and request.form["password"] == "admin123":
            session["employee"] = True
            return redirect("/dashboard")

    return layout("""
    <div class="container">
    <h2>Employee Login</h2>

    <form method="post">

    Email
    <input name="email">

    Password
    <input name="password" type="password">

    <button>Login</button>

    </form>
    </div>
    """)

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "employee" not in session:
        return redirect("/login")

    conn = db()
    tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()

    html = "<div class='container'><h2>Support Dashboard</h2>"

    for t in tickets:
        html += f"""
        <hr>
        <b>{t[1]}</b> ({t[2]})<br>
        Issue: {t[3]}<br>
        Status: {t[4]}<br>
        <a href="/resolve/{t[0]}">Mark Resolved</a>
        """

    html += "</div>"

    return layout(html)

# Resolve Ticket
@app.route("/resolve/<id>")
def resolve(id):

    conn = db()
    conn.execute("UPDATE tickets SET status='Resolved' WHERE id=?",(id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

# About
@app.route("/about")
def about():
    return layout("""
    <div class="container">
    <h2>About Us</h2>
    <p>RoyalAnchor Support delivers elite outsourced customer service for modern SaaS companies.</p>
    </div>
    """)

# Contact
@app.route("/contact")
def contact():
    return layout("""
    <div class="container">
    <h2>Contact Us</h2>
    <p>Email: support@royalanchor.com</p>
    </div>
    """)

# Careers
@app.route("/careers")
def careers():
    return layout("""
    <div class="container">
    <h2>Careers</h2>
    <p>We're hiring support engineers and customer success specialists.</p>
    </div>
    """)

import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "royalanchor"

def db():
    return sqlite3.connect("tickets.db")

conn = db()
conn.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY, name TEXT, email TEXT, issue TEXT, status TEXT)")
conn.commit()
conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ticket", methods=["GET","POST"])
def ticket():

    if request.method == "POST":

        conn = db()
        conn.execute("INSERT INTO tickets (name,email,issue,status) VALUES (?,?,?,?)",
        (request.form["name"],request.form["email"],request.form["issue"],"Open"))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("ticket.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        if request.form["email"] == "admin@royalanchor.com" and request.form["password"] == "admin123":
            session["employee"] = True
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "employee" not in session:
        return redirect("/login")

    conn = db()
    tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()

    return render_template("dashboard.html", tickets=tickets)

@app.route("/resolve/<id>")
def resolve(id):

    conn = db()
    conn.execute("UPDATE tickets SET status='Resolved' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/careers")
def careers():
    return render_template("careers.html")

app.run(host="0.0.0.0", port=5000)
