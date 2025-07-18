import hashlib
from database import get_cursor, commit_db
from crypto import encrypt_msg, decrypt_msg

def user_request():
    print(\"\\n📥 User Registration Request\")
    name = input(\"Name: \")
    mobile = input(\"Mobile: \")
    email = input(\"Email: \")
    password_raw = input(\"Password: \")
    password = hashlib.sha256(password_raw.encode()).hexdigest()
    nid_path = input(\"Path to NID image: \")
    bank_card_path = input(\"Path to Bank Card image: \")
    c = get_cursor()
    c.execute(\"INSERT INTO users (name, mobile, email, password, nid_path, bank_card_path) VALUES (?, ?, ?, ?, ?, ?)\", (name, mobile, email, password, nid_path, bank_card_path))
    commit_db()
    print(\"Registration request submitted. Please wait for admin approval.\")

def user_login():
    print(\"\\n👤 User Login\")
    email = input(\"Email: \")
    password_raw = input(\"Password: \")
    password = hashlib.sha256(password_raw.encode()).hexdigest()
    c = get_cursor()
    row = c.execute(\"SELECT is_verified FROM users WHERE email=? AND password=?\", (email, password)).fetchone()
    if row and row[0] == 1:
        user_dashboard(email)
    else:
        print(\"Invalid credentials or not approved yet.\")

def user_dashboard(email):
    c = get_cursor()
    while True:
        print(\"\\n[1] Send Message\n[2] View My Messages\n[3] Manage Contacts\n[4] Logout\")
        choice = input(\">> \")
        if choice == '1':
            send_msg(email)
        elif choice == '2':
            view_my_msgs(email)
        elif choice == '3':
            manage_contacts(email)
        elif choice == '4':
            print(\"Logging out...\")
            break
        else:
            print(\"Invalid choice.\")

def send_msg(sender_email):
    c = get_cursor()
    # Fetch contacts of sender
    contacts = c.execute(\"SELECT contact_email FROM contacts WHERE user_email=?\", (sender_email,)).fetchall()
    if not contacts:
        print(\"No contacts found. Please add contacts first.\")
        return
    print(\"Your contacts:\")
    for i, contact in enumerate(contacts, 1):
        print(f\"{i}. {contact[0]}\")
    choice = input(\"Select contact number to send message: \")
    try:
        idx = int(choice) - 1
        receiver_email = contacts[idx][0]
    except (ValueError, IndexError):
        print(\"Invalid choice.\")
        return
    message_raw = input(\"Message: \")
    encrypted = encrypt_msg(message_raw)
    c.execute(\"INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)\", (sender_email, receiver_email, encrypted))
    commit_db()
    print(\"Message sent.\")

def view_my_msgs(email):
    c = get_cursor()
    rows = c.execute(\"SELECT sender, message FROM messages WHERE receiver=? ORDER BY timestamp DESC\", (email,)).fetchall()
    if not rows:
        print(\"No messages.\")
        return
    print(\"\\nYour messages:\")
    for r in rows:
        decrypted = decrypt_msg(r[1])
        print(f\"From {r[0]}: {decrypted}\")

def manage_contacts(user_email):
    c = get_cursor()
    while True:
        print(\"\\n[1] View Contacts\n[2] Add Contact\n[3] Remove Contact\n[4] Back\")
        choice = input(\">> \")
        if choice == '1':
            contacts = c.execute(\"SELECT contact_email FROM contacts WHERE user_email=?\", (user_email,)).fetchall()
            if not contacts:
                print(\"No contacts found.\")
            else:
                print(\"Your contacts:\")
                for contact in contacts:
                    print(contact[0])
        elif choice == '2':
            new_contact = input(\"Enter email of user to add: \")
            # Check if new_contact is verified user
            row = c.execute(\"SELECT is_verified FROM users WHERE email=?\", (new_contact,)).fetchone()
            if row and row[0] == 1:
                try:
                    c.execute(\"INSERT INTO contacts (user_email, contact_email) VALUES (?, ?)\", (user_email, new_contact))
                    commit_db()
                    print(\"Contact added.\")
                except:
                    print(\"Contact already exists or error occurred.\")
            else:
                print(\"User not found or not verified.\")
        elif choice == '3':
            del_contact = input(\"Enter email of contact to remove: \")
            c.execute(\"DELETE FROM contacts WHERE user_email=? AND contact_email=?\", (user_email, del_contact))
            commit_db()
            print(\"Contact removed if existed.\")
        elif choice == '4':
            break
        else:
            print(\"Invalid choice.\")
