import os

from gi.repository import Gtk
from scenes.user_management import LoginView, RegisterView

build_file = gtk_builder_file = os.path.splitext(__file__)[0] + '.ui'

class Application(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gtk_builder_file)
        
        self.window = self.builder.get_object('main_window')
        self.stage = self.builder.get_object('stage')
        self.scene_start = self.builder.get_object('scene_start')
        self.stage.pack_end(self.scene_start ,
                            True,
                            True,
                            10
                        )
        
        
        self.button_login = self.builder.get_object('main_login')
        self.button_register = self.builder.get_object('main_register')

        self.window.connect('destroy', self.signal_window_destroy)
        self.button_login.connect('clicked', self.signal_window_login)
        self.button_register.connect('clicked', self.signal_window_register)

        
        self.window.show()

    def signal_window_destroy(self, _):
        self.window.destroy()
        Gtk.main_quit()

    def signal_window_login(self, _):
        self.scene_login = self.builder.get_object('scene_login')
        self.stage.remove(self.scene_start)
        self.stage.pack_end(self.scene_login,
                            True,
                            True,
                            10
                        )
        LoginView(self.scene_start, self.stage, self.builder)
        
                    

    def signal_window_register(self, _):
        self.scene_register = self.builder.get_object('scene_register')
        self.stage.remove(self.scene_start)
        self.stage.pack_end(self.scene_register,
                            True,
                            True,
                            10
                        )
        RegisterView(self.scene_start, self.stage, self.builder)
if __name__ == '__main__':
    Application()
    Gtk.main()
