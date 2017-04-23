class User(object):
    def __init__(self, name=None, id=None, password=None, user_type=None):
        self.json = {}
        if name != None:
            self.json['name'] = name
        if id != None:
            self.json['id'] = id
        if password != None:
            self.json['password'] = password
        if user_type != None:
            self.json['type'] = user_type
    def add(self, name, data):
        self.json[name] = data
    
class LoginManager(object):
    def __init__(self, username, password, db):
        self.db = db
        self.valid = self.check_account(User(id=username, password=password))

    def check_account(self, user):
        out = self.db.raindrop.find_one(user.json) 
        if out == None:
            return (False, user)
        else:
            user.add('type', out['type'])
            user.add('name', out['name'])
            return (True, user)

class Registration(object):
    def __init__(self, username, password, user_type, name, db):
        self.db = db
        if user_type not in ["User", "Administrator", "Moderator"]:
            self.valid = False
        else:
            user = User(name=name, id=username, user_type=user_type, password=password)
            self.db.raindrop.insert_one(user.json)
            self.valid = True

class UserUpdate(object):
    def __init__(self, user, updates, db):
        db.raindrop.find_one_and_update(user.json, {'$set': updates.json})
        self.new = user
        for field in updates.json:
            self.new.add(field, updates.json[field])
