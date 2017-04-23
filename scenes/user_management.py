from gi.repository import Gtk

class LoginView(object):
    def __init__(self, prev, stage, builder, db, window):
        self.builder = builder
        self.prev = prev
        self.stage = stage
        self.db = db
        self.window = window

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_login')
        self.button_cancel = self.builder.get_object('login_cancel_button')
        self.button_cancel.connect('clicked', self.signal_button_cancel)

        self.button_submit = self.builder.get_object('login_submit_button')
        self.button_submit.connect('clicked', self.signal_button_submit)

        self.id_entry = self.builder.get_object('login_email_field')
        self.password_entry = self.builder.get_object('login_password_field')

    def signal_button_submit(self, _):
        user_text = self.id_entry.get_text()
        pass_text = self.password_entry.get_text()

        valid, user = LoginManager(user_text, pass_text, self.db).valid
        if not valid:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                Gtk.ButtonsType.OK, "Sorry")
            dialog.format_secondary_text(
                "That username/password combination does not exist.")
            dialog.run()
            dialog.destroy()
            return
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_main')
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )

    def signal_button_cancel(self, _):
        self.stage.remove(self.scene)
        self.stage.pack_end(self.prev,
                                True,
                                True,
                                0
                        )

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

class RegisterView(object):
    def __init__(self, prev, stage, builder, db, window):
        self.builder = builder
        self.prev = prev
        self.stage = stage
        self.db = db
        
        self.window = window
        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_register')
        self.button_cancel = self.builder.get_object('register_cancel_button')
        self.button_cancel.connect('clicked', self.signal_button_cancel)
        
        self.button_submit = self.builder.get_object('register_submit_button')
        self.button_submit.connect('clicked', self.signal_button_submit)

        self.pass_entry = self.builder.get_object('register_password_field')

        self.user_entry = self.builder.get_object('register_user_field')
        
        self.email_entry = self.builder.get_object('register_email_field')
        
        self.name_entry = self.builder.get_object('register_name_field')

    def signal_button_submit(self, _):
        username = self.email_entry.get_text()
        password = self.pass_entry.get_text()
        name = self.name_entry.get_text()
        user_type = self.user_entry.get_text()
        if not Registration(username, password, user_type, name, self.db).valid:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                Gtk.ButtonsType.OK, "Sorry")
            dialog.format_secondary_text(
                "Invalid user type.")
            dialog.run()
            dialog.destroy()
            return
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_start')
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )

    def signal_button_cancel(self, _):
        self.stage.remove(self.scene)
        self.stage.pack_end(self.prev,
                                True,
                                True,
                                0
                        )
