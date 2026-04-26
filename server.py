from user import User

if __name__ == "__main__":
    user = User(refresh_token=False)
    user.send_message("Hello, this is a test message from the server!")
