import os
import json

# --- MJ's Incident Manager Tool ---
# Developer: Mujahid Adamu Aliyu (MJ Tech Solutions)
# Purpose: A persistent database tool to track and resolve Cyber Incidents.
# Location: Bauchi, Nigeria

users = {}

def get_input(prompt):
    """MJ's helper function to clean inputs (removes spaces, lowers case)"""
    return input(prompt).strip().lower()

def load():
    """Logic to load the database safely. If missing, MJ creates a new one."""
    global users 
    try:
        if os.path.exists("incident.json"):
            with open("incident.json", "r") as file:
                users = json.load(file)
        else:
            users = {}
    except FileNotFoundError:
        users = {}

def save():
    """Saves data to JSON so MJ never loses a report."""
    with open("incident.json", "w") as file:
        json.dump(users, file, indent=4)

def log():
    # Load database immediately when MJ starts the tool
    load()
    active = True
    
    print("\n" + "="*40)
    print("   🛡️  MJ INCIDENT MANAGER V1.0  🛡️")
    print("="*40)

    while active:
        print("\nWhat do you want to do?")
        print("(1) Add New Report")
        print("(2) View Incident Details")
        print("(3) Change Incident Status")
        print("(4) View Resolved Reports (Closed)")
        print("(5) View Unresolved Reports (Open)")
        print("(0) Logout")
        
        opt = get_input("Enter selection: ")
        
        # Validation Loop
        while opt not in ["1", "2", "3", "4", "5", "0"]:
            print("\n[!] Invalid response provided.")
            opt = get_input("Enter valid selection: ")

        # --- OPTION 1: ADD REPORT ---
        if opt == "1":
            print("\n-- Adding New Report --")
            ip = get_input("Enter the IP address: ")
            
            # MJ's IP validation logic
            while len(ip) < 7 or len(ip) > 15:
                ip = get_input("Invalid IP length. Enter valid IP address: ")             
            
            users[ip] = {
                "type": get_input("Enter attack type (e.g., DDoS, Phishing): "),
                "severity": get_input("Enter severity (Low/Med/High): "),
                "status": "open", # Default status is always open
                "timestamp": "undefined"
            }
            save()
            print(f"[+] Incident for {ip} saved successfully!")

        # --- OPTION 2: VIEW SPECIFIC ---
        elif opt == "2":
            print("\n-- Viewing Incident Details --")
            ip = get_input("Enter IP address to view: ")
            
            while ip not in users:
                print(f"[!] IP {ip} does not exist in MJ's database.")
                ip = get_input("Enter IP address: ")
            
            # Extracting data for display
            details = users[ip]
            print("-" * 30)
            print(f"Target IP: {ip}")
            print(f"Type:      {details['type']}")
            print(f"Severity:  {details['severity']}")
            print(f"Status:    {details['status'].upper()}")
            print("-" * 30)

        # --- OPTION 3: UPDATE STATUS ---
        elif opt == "3":
            print("\n-- Changing Incident Status --")
            ques = get_input("Enter IP address to update: ")
            
            while ques not in users:
                print("[!] IP not found.")
                ques = get_input("Enter IP address: ")
                
            update = get_input("Enter new status (open/closed): ")
            while update not in ["open", "closed"]:
                print("[!] Status must be 'open' or 'closed'.")
                update = get_input("Enter status: ")
            
            users[ques]["status"] = update 
            save()
            print(f"[+] Status for {ques} updated to {update.upper()}.")

        # --- OPTION 4: VIEW RESOLVED ---
        elif opt == "4":
            print("\n-- Resolved Incidents (Closed) --")
            found = False
            for ip in users:
                if users[ip]["status"] == "closed":
                    print(f"✅ {ip} | Type: {users[ip]['type']}")
                    found = True
            
            if not found:
                print("No resolved incidents found.")

        # --- OPTION 5: VIEW UNRESOLVED ---
        elif opt == "5":
            print("\n-- Unresolved Incidents (Open) --")
            found = False
            for ip in users:
                if users[ip]["status"] == "open":
                    print(f"⚠️  {ip} | Severity: {users[ip]['severity']}")
                    found = True
            
            if not found:
                print("Great job MJ! No open incidents.")

        # --- OPTION 0: EXIT ---
        elif opt == "0":
            active = False
            print("\n[!] Session terminated by User.")
            print("© MJ Tech Solutions - Stay Secure.")

# Run the car program
if __name__ == "__main__":
    log()
