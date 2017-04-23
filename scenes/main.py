from scenes.managers import User, UserUpdate


from gi.repository import Gtk

class MainView(object):
    def __init__(self, prev, stage, builder, user, db, window):
        self.builder = builder
        self.prev = prev
        self.stage = stage
        self.db = db
        self.window = window
        self.user = user
        self.setup()

        self.edit_view = None
    def setup(self):
        self.scene = self.builder.get_object('scene_main')

        self.button_edit = self.builder.get_object('menu_button_edit_profile')
        edit_handler = self.button_edit.connect('clicked', self.signal_button_edit)

        self.button_view_reports = self.builder.get_object('menu_button_view_reports')
        view_handler = self.button_view_reports.connect('clicked', lambda x: print(self.user.json))

        self.button_logout = self.builder.get_object('menu_button_logout')
        logout_handler = self.button_logout.connect('clicked', self.signal_button_logout)
    
    def signal_button_logout(self, _):
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_start')
        
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )

    def signal_button_edit(self, _):
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_edit')

        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )
        if not self.edit_view:
            self.edit_view = EditView(self.scene, self.stage, self.builder, self.user, self.db, self.window)
        self.user = self.edit_view.user


class EditView(object):
    def __init__(self, prev, stage, builder, user, db, window):
        self.prev = prev
        self.stage = stage
        self.builder = builder
        self.user  = user
        self.db = db
        self.window = window

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_edit')

        self.button_cancel = self.builder.get_object('edit_button_cancel')
        self.button_cancel.connect('clicked', self.signal_button_cancel)

        self.button_submit = self.builder.get_object('edit_button_submit')
        self.button_submit.connect('clicked', self.signal_button_submit)

        self.new_pass = self.builder.get_object('edit_password_field')
        self.new_name = self.builder.get_object('edit_name_field')

    def signal_button_submit(self, _):
        updates = User()
        if self.new_pass.get_text():
            updates.add('password', self.new_pass.get_text())
        if self.new_name.get_text():
            updates.add('name', self.new_name.get_text())
        self.user = UserUpdate(self.user, updates, self.db).new
        self.exit()

    def signal_button_cancel(self, _):
        self.exit()
    
    def exit(self):
        self.stage.remove(self.scene)
        self.stage.pack_end(self.prev,
                                True,
                                True,
                                0
                        ) 
