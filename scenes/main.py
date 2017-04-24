import datetime

from scenes.managers import User, UserUpdate, ReportManager, Report, QualityReport, QualityReportManager

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
        self.create_report_view = None
        self.view_report_view = None
        self.create_quality_view = None
        self.view_quality_view = None

    def setup(self):
        self.scene = self.builder.get_object('scene_main')

        self.button_edit = self.builder.get_object('menu_button_edit_profile')
        edit_handler = self.button_edit.connect('clicked', self.signal_button_edit)

        self.button_create_reports = self.builder.get_object('menu_button_create_reports')
        view_handler = self.button_create_reports.connect('clicked', self.signal_button_create_report)

        self.button_view_reports = self.builder.get_object('menu_button_view_reports')
        self.button_view_reports.connect('clicked', self.signal_button_view_report)
    
        self.button_create_quality_reports = self.builder.get_object('menu_button_create_quality_report')
        self.button_create_quality_reports.connect('clicked', self.signal_button_create_quality_report)

        self.button_view_quality_reports = self.builder.get_object('menu_button_view_quality_reports')
        self.button_view_quality_reports.connect('clicked', self.signal_button_view_quality_reports)

        self.button_logout = self.builder.get_object('menu_button_logout')
        logout_handler = self.button_logout.connect('clicked', self.signal_button_logout)

    def signal_button_view_quality_reports(self, _):
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_view_quality')
        
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )
        if not self.view_quality_view:
            self.view_quality_view = QualityReportView(self.scene, self.stage, self.builder, self.user, self.db, self.window)
        self.view_quality_view.update()

    def signal_button_create_quality_report(self, _):
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_create_quality_report')
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )        
        if not self.create_report_view:
            self.create_report_view = CreateQualityReportView(self.scene, self.stage, self.builder, self.user, self.db, self.window)

    def signal_button_view_report(self, _):
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_view')
        
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )
        if not self.view_report_view:
            self.view_report_view = ViewReportView(self.scene, self.stage, self.builder, self.user, self.db, self.window)
        self.view_report_view.update()
        
    def signal_button_logout(self, _):
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_start')
        
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )

    def signal_button_create_report(self, _):
        self.stage.remove(self.scene)
        self.new = self.builder.get_object('scene_create_report')
        self.stage.pack_end(self.new,
                                True,
                                True,
                                0
                        )        
        if not self.create_report_view:
            self.create_report_view = CreateReportView(self.scene, self.stage, self.builder, self.user, self.db, self.window)
        

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

class CreateReportView(object):
    def __init__(self, prev, stage, builder, user, db, window):
        self.prev = prev
        self.stage = stage
        self.builder = builder
        self.user  = user
        self.db = db
        self.window = window

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_create_report')

        self.button_cancel = self.builder.get_object('create_report_cancel_button')
        self.button_cancel.connect('clicked', self.signal_button_cancel)

        self.button_submit = self.builder.get_object('create_report_submit_button')
        self.button_submit.connect('clicked', self.signal_button_submit)

        self.quality = self.builder.get_object('create_report_water_quality_field')
        self.type = self.builder.get_object('create_report_water_type_field')

    def signal_button_submit(self, _):
        if self.type.get_text() and self.quality.get_text():
            report = Report(self.type.get_text(), self.quality.get_text(), self.user.json['name'])
            ReportManager(report, self.db).create()
        else:
            print("WRONG")
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

class ViewReportView(object):
    def __init__(self, prev, stage, builder, user, db, window):
        self.prev = prev
        self.stage = stage
        self.builder = builder
        self.user  = user
        self.db = db
        self.window = window

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_view')

        self.button_done = self.builder.get_object('view_button_done')
        self.button_done.connect('clicked', self.signal_button_done)

        self.tv = self.builder.get_object('report_tv')
        self.tv_model = Gtk.ListStore(int, str, str, str, str, str)
        self.tv.set_model(self.tv_model)
        renderer = Gtk.CellRendererText()
        _id = Gtk.TreeViewColumn("ID", renderer, text=0)
        loc = Gtk.TreeViewColumn("Location", renderer, text=1)
        _type = Gtk.TreeViewColumn("Type", renderer, text=2)
        time = Gtk.TreeViewColumn("Time", renderer, text=3)
        qual = Gtk.TreeViewColumn("Quality", renderer, text=4)
        user = Gtk.TreeViewColumn("User", renderer, text=5)
        for col in [_id, loc, _type, time, qual, user]:
            self.tv.append_column(col)

    def update(self):
        to_update = ReportManager(db=self.db).get_all()
        counter = 1
        self.tv_model.clear()
        for update in to_update:
            _id = counter
            loc = str(update['lat']) + ', ' + str(update['lon'])
            _type = update['type']
            time = update['ts'][:update['ts'].index('.')]
            qual = update['quality']
            user = update['name']
            self.tv_model.append([_id, loc, _type, time, qual, user])
            counter += 1

    def signal_button_done(self, _):
        self.exit()

    def exit(self):
        self.stage.remove(self.scene)
        self.stage.pack_end(self.prev,
                                True,
                                True,
                                0
                        ) 

class CreateQualityReportView(object):
    def __init__(self, prev, stage, builder, user, db, window):
        self.prev = prev
        self.stage = stage
        self.builder = builder
        self.user  = user
        self.db = db
        self.window = window

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_create_quality_report')

        self.button_cancel = self.builder.get_object('create_quality_report_cancel_button')
        self.button_cancel.connect('clicked', self.signal_button_cancel)

        self.button_submit = self.builder.get_object('create_quality_report_submit_button')
        self.button_submit.connect('clicked', self.signal_button_submit)

        self.virus_ppm = self.builder.get_object('create_quality_report_virus_ppm_field')
        self.cont_ppm = self.builder.get_object('create_quality_report_cont_ppm_field')
        self.quality = self.builder.get_object('create_quality_report_water_quality_field')

    def signal_button_submit(self, _):
        if self.virus_ppm.get_text() and self.cont_ppm.get_text() and self.quality.get_text():
            report = QualityReport(self.virus_ppm.get_text(), self.cont_ppm.get_text(), self.quality.get_text(), self.user.json['name'])
            QualityReportManager(report, self.db).create()
        else:
            print("WRONG")
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

class QualityReportView(object):
    def __init__(self, prev, stage, builder, user, db, window):
        self.prev = prev
        self.stage = stage
        self.builder = builder
        self.user  = user
        self.db = db
        self.window = window

        self.setup()

    def setup(self):
        self.scene = self.builder.get_object('scene_view_quality')

        self.button_done = self.builder.get_object('view_quality_button_done')
        self.button_done.connect('clicked', self.signal_button_done)

        self.tv = self.builder.get_object('quality_tv')
        self.tv_model = Gtk.ListStore(int, str, str, str, str, str, str)
        self.tv.set_model(self.tv_model)
        renderer = Gtk.CellRendererText()
        _id = Gtk.TreeViewColumn("ID", renderer, text=0)
        loc = Gtk.TreeViewColumn("Location", renderer, text=1)
        virus = Gtk.TreeViewColumn("Virus PPM", renderer, text=2)
        cont = Gtk.TreeViewColumn("Contaminant PPM", renderer, text=3)
        time = Gtk.TreeViewColumn("Time", renderer, text=4)
        qual = Gtk.TreeViewColumn("Quality", renderer, text=5)
        user = Gtk.TreeViewColumn("User", renderer, text=6)
        for col in [_id, loc, virus, cont, time, qual, user]:
            self.tv.append_column(col)
        

    def update(self):
        to_update = QualityReportManager(db=self.db).get_all()
        counter = 1
        self.tv_model.clear()
        for update in to_update:
            _id = counter
            loc = str(update['lat']) + ', ' + str(update['lon'])
            virus = update['virus_ppm']
            cont = update['contaminant_ppm']
            time = update['ts'][:update['ts'].index('.')]
            qual = update['quality']
            user = update['user']
            self.tv_model.append([_id, loc, virus, cont, time, qual, user])
            counter += 1

    def signal_button_done(self, _):
        self.exit()

    def exit(self):
        self.stage.remove(self.scene)
        self.stage.pack_end(self.prev,
                                True,
                                True,
                                0
                        ) 
