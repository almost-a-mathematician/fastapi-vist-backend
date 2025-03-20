import bcrypt

class PasswordManager:
    def generate(self, password: str):
        bytes = password.encode()
        salt = bcrypt.gensalt() 
        return bcrypt.hashpw(bytes, salt).decode()

    def check(self, provided_password: str, hashed_password: str): 
        try:
            return bcrypt.checkpw(provided_password.encode(), hashed_password.encode())
        except:
            return False


password_manager = PasswordManager()





