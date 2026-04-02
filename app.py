from flask import Flask, render_template, request, jsonify
import hashlib, json, os, time

app = Flask(__name__)
DB_FILE = "db.json"


# ================= DB =================
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


# ================= ROUTES =================


@app.route("/")
def home():
    return render_template("index.html")


# -------- ADD USER --------
@app.route("/add", methods=["POST"])
def add():
    data = request.json
    db = load_db()

    salt = os.urandom(4).hex()

    user = {
        "username": data["username"],
        "plain": data["password"],
        "hash": sha256(data["password"]),
        "salt_hash": sha256(data["password"] + salt)
    }

    db.append(user)
    save_db(db)

    return jsonify({"status": "ok"})


# -------- LEAK --------
@app.route("/leak")
def leak():
    return jsonify(load_db())


# -------- DICTIONARY --------
@app.route("/attack/dictionary")
def dictionary():
    db = load_db()
    words = ["123456", "password", "hello123", "qwerty"]

    result = []

    for w in words:
        h = sha256(w)
        matches = [u["username"] for u in db if u["hash"] == h]

        result.append({"word": w, "match": matches})

    return {"results": result, "wordlist": words}


# -------- RAINBOW --------
@app.route("/attack/rainbow")
def rainbow():
    db = load_db()

    # rainbow table
    table = {
        sha256("123456"): "123456",
        sha256("password"): "password",
        sha256("hello123"): "hello123",
        sha256("qwerty"): "qwerty"
    }

    grouped = {}

    for u in db:
        h = u["hash"]

        if h in table:
            if h not in grouped:
                grouped[h] = []

            grouped[h].append(u["username"])

    result = []

    for h, users in grouped.items():
        result.append({
            "hash": h,
            "users": users,
            "password": table[h],
            "count": len(users)
        })

    return {
        "results": result,
        "table": table
    }
@app.route("/defense/lock")
def lock():
    db = load_db()

    attempts = ["123456", "password", "hello123","qwerty","password123"]
    username = "Alice"
    max_attempts = 3

    user = next((u for u in db if u["username"] == username), None)

    output = ""
    remaining = max_attempts
    if not user:
        return "User not found"

    for i, p in enumerate(attempts):
        output += f"Attempt {i+1}:\n"
        output += f"User: {username}\n"
        output += f"Password: {p}\n"
        if sha256(p) == user["hash"]:
            output += "Result: Login SUCCESS \n"
            return output
        else:
            remaining = max_attempts - i - 1
            output += "Result: Incorrect password\n"
            output += f"Remaining Attempts: {remaining}\n\n"
            if remaining == 0:
                break
                

    output += "ACCOUNT LOCKED \nToo many failed attempts."

    return {"attempts": attempts, "output": output}


# -------- SLOW HASH --------
@app.route("/defense/slow")
def slow():
    db = load_db()

    username = "Alice"
    wordlist = ["123456", "password", "hello123", "qwerty"]

    user = next((u for u in db if u["username"] == username), None)

    if not user:
        return {"error": "User not found"}

    results = []
    total_time = 0

    for word in wordlist:
        start = time.time()

        time.sleep(2)

        hashed = sha256(word)
        elapsed = round(time.time() - start, 2)

        total_time += elapsed

        results.append(
            {
                "username": username,
                "password": word,
                "time": elapsed,
                "match": hashed == user["hash"]
            }
        )

    return {
        "results": results,
        "total_time": round(total_time, 2),
        "wordlist": wordlist
    }


if __name__ == "__main__":
    app.run(debug=True)
