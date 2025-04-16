from werkzeug.security import generate_password_hash, check_password_hash

class PasswordMixin:
    @property
    def password(self): # make user.password non-readable
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password): # hash password before storing
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password): # check if given password matches stored hash
        return check_password_hash(self.password_hash, password)
