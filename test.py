import requests


BASE_URL = "https://pwr-messenger.hyperit.pl"


TOKEN = None
HEADERS = None

def register():
    username = input("Enter your desired username: ")
    password = input("Enter your desired password: ")
    payload = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print("Register Response:", response.json())

def login():
    global TOKEN, HEADERS
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    client_pub = 17
    payload = {"username": username, "password": password, "clientPub": client_pub}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    result = response.json()
    print("Login Response:", result)
    TOKEN = result.get("token")
    if TOKEN:
        HEADERS = {"Authorization": f"Bearer {TOKEN}"}
        print("Login successful!")
    else:
        print("Login failed!")

def view_users():
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS)
    print("Users List:", response.json())

def send_message():
    recipient = input("Enter the recipient's username: ")
    message = input("Enter your message: ")
    payload = {"receiver": recipient, "content": message}
    response = requests.post(f"{BASE_URL}/message/conversations", json=payload, headers=HEADERS)
    print("Send Message Response:", response.json())

def view_conversations():
    response = requests.get(f"{BASE_URL}/message/conversations", headers=HEADERS)
    print("Conversations List:", response.json())

def view_conversation_with_user():
    recipient = input("Enter the username of the user you want to view conversation with: ")
    try:
        response = requests.get(f"{BASE_URL}/message/conversations/{recipient}", headers=HEADERS)
        if response.status_code == 200:
            try:
                data = response.json()  
                print("Conversation with", recipient, ":", data)
            except requests.exceptions.JSONDecodeError:
                print("Error: Response is not in JSON format.")
                print("Raw response text:", response.text)
        else:
            print(f"Error: Received status code {response.status_code}")
            print("Raw response text:", response.text)
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        
def main_menu():
    while True:
        print("\n=== Messenger Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. View Users")
        print("4. Send a Message")
        print("5. View Conversations")
        print("6. View Conversation with a User")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            if HEADERS:
                view_users()
            else:
                print("Please login first.")
        elif choice == "4":
            if HEADERS:
                send_message()
            else:
                print("Please login first.")
        elif choice == "5":
            if HEADERS:
                view_conversations()
            else:
                print("Please login first.")
        elif choice == "6":
            if HEADERS:
                view_conversation_with_user()
            else:
                print("Please login first.")
        elif choice == "7":
            print("Exiting the messenger. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
