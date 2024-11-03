import requests

BASE_URL = "http://localhost:8080"

def register_user():
    username = input("Enter a username for registration: ")
    password = input("Enter a password for registration: ")
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print(f"Registration successful for {username}: {response.json()}")
    else:
        print(f"Registration failed for {username}: {response.status_code} {response.text}")

def login_user():
    username = input("Enter your username to log in: ")
    password = input("Enter your password to log in: ")
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print(f"Login successful for {username}: {response.json()}")
        return response.json()['token'], username
    else:
        print(f"Login failed for {username}: {response.status_code} {response.text}")
        return None, None

def send_message(token, sender):
    receiver = input("Enter the username of the receiver: ")
    message = input("Enter your message: ")
    url = f"{BASE_URL}/message/conversations"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "content": message,
        "receiver": receiver
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print(f"Message sent from {sender} to {receiver}: {message}")
    else:
        print(f"Failed to send message from {sender} to {receiver}: {response.status_code} {response.text}")

def get_messages(token, username):
    participant = input("Enter the username of the participant to retrieve messages: ")
    url = f"{BASE_URL}/message/conversations/{participant}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Messages with {participant}:", response.json())
    else:
        print(f"Failed to retrieve messages with {participant}: {response.status_code} {response.text}")

# Main interactive loop
def main():
    token = None
    username = None
    
    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Log In")
        print("3. Send Message")
        print("4. Get Messages")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            register_user()
        elif choice == "2":
            token, username = login_user()
        elif choice == "3":
            if token and username:
                send_message(token, username)
            else:
                print("You must log in to send messages.")
        elif choice == "4":
            if token and username:
                get_messages(token, username)
            else:
                print("You must log in to retrieve messages.")
        elif choice == "5":
            print("Exiting the application.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
