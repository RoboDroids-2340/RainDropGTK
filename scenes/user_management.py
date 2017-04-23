from gi.repository import Gtk

class LoginView(object):
    def __init__(self, prev, stage, builder):
        self.builder = builder
        self.prev = prev
        self.stage = stage

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_login')
        self.button_cancel = self.builder.get_object('login_cancel_button')
        self.button_cancel.connect('clicked', self.signal_button_cancel)

        self.button_submit = self.builder.get_object('login_submit_button')
        self.button_submit.connect('clicked', self.signal_button_submit)

    def signal_button_submit(self, _):
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

class RegisterView(object):
    def __init__(self, prev, stage, builder):
        self.builder = builder
        self.prev = prev
        self.stage = stage

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_register')
        self.button_cancel = self.builder.get_object('register_cancel_button')
        self.button_cancel.connect('clicked', self.signal_button_cancel)
        

    def signal_button_cancel(self, _):
        self.stage.remove(self.scene)
        self.stage.pack_end(self.prev,
                                True,
                                True,
                                0
                        )
