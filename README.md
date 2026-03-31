#  Secure Password Storage Demo

##  Objective
This project demonstrates why plain-text password storage is insecure and compares it with hashing and salted hashing.

---

##  How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   python app.py

3. Open browser:
   http://127.0.0.1:5000

---

##  Demo Scenario

### Step 1: Create Users
- David / password123
- John / password123
- Alice / qwerty

---

### Step 2: Leak Mode
Click "Leak Database"

Explain:
- Plain text → visible (insecure)
- Hash → same for same password
- Salt + Hash → different values

---

### Step 3: Attack Mode
Click "Attack Passwords"

Explain:
- Dictionary attack cracks common passwords
- Demonstrates weakness of hashing alone

---

##  Key Takeaways
- Plain text storage is extremely dangerous
- Hashing improves security but is still vulnerable
- Salting significantly increases protection