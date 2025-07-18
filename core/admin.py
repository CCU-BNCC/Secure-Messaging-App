import getpass
import hashlib
import base64
from database import get_cursor, commit_db
from crypto import decrypt_msg

def admin_login():
    print(\"\\n🔑 Admin Login\")
    pwd = getpass.getpass(\"Password: \")
    c = get_cursor()
    data = c.execute(\"SELECT password FROM admin WHERE id=1\").fetchone()
    if not data:
        print(\"Admin not found.\")
        return False
    stored = data[0]
    stored_hash = stored[:64]
    stored_salt = base64.b64decode(stored[64:])
    input_hash = hashlib.sha256(pwd.encode() + stored_salt).hexdigest()
    if input_hash == stored_hash:
        print(\"Login successful.\")
        return True
    else:
        print(\"Incorrect password.\")
        return False

def admin_dashboard():
    c = get_cursor()
    while True:
        print(\"\\n[1] Approve Users\n[2] View All Messages\n[3] Logout\")
        choice = input(\">> \")
        if choice == '1':
            rows = c.execute(\"SELECT id, name, email, is_verified FROM users WHERE is_verified=0\").fetchall()
            if not rows:
                print(\"No pending users.\")
                continue
            for r in rows:
                print(f\"[ID:{r[0]}] {r[1]} <{r[2]}> Verified: {r[3]}\")
            uid = input(\"Enter ID to approve (or 'b' to back): \")
            if uid.lower() == 'b':
                continue
            c.execute(\"UPDATE users SET is_verified=1 WHERE id=?\", (uid,))
            commit_db()
            print(\"User approved.\")
        elif choice == '2':
            rows = c.execute(\"SELECT sender, receiver, message, timestamp FROM messages ORDER BY timestamp DESC\").fetchall()
            for r in rows:
                decrypted = decrypt_msg(r[2])
                print(f\"[{r[3]}] {r[0]} → {r[1]}: {decrypted}\")
        elif choice == '3':
            print(\"Logging out...\")
            break
        else:
            print(\"Invalid option.\")
