from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

users = {
    'admin1': User('admin1', 'adminpass1', 'admin'),
    'admin2': User('admin2', 'adminpass2', 'admin'),
    'admin3': User('admin3', 'adminpass3', 'admin'),
    'admin4': User('admin4', 'adminpass4', 'admin'),
    'admin5': User('admin5', 'adminpass5', 'admin'),
    'admin6': User('admin6', 'adminpass6', 'admin'),
    'admin7': User('admin7', 'adminpass7', 'admin'),
    'admin8': User('admin8', 'adminpass8', 'admin'),
    'admin9': User('admin9', 'adminpass9', 'admin'),
    'admin10': User('admin10', 'adminpass10', 'admin'),
    'student1': User('student1', 'studentpass1', 'student'),
    'student2': User('student2', 'studentpass2', 'student'),
    'student3': User('student3', 'studentpass3', 'student'),
    'student4': User('student4', 'studentpass4', 'student'),
    'student5': User('student5', 'studentpass5', 'student'),
    'student6': User('student6', 'studentpass6', 'student'),
    'student7': User('student7', 'studentpass7', 'student'),
    'student8': User('student8', 'studentpass8', 'student'),
    'student9': User('student9', 'studentpass9', 'student'),
    'student10': User('student10', 'studentpass10', 'student')
}

