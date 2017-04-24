import requests
import json
import datetime

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

class ReportManager(object):

    def __init__(self, report=None, db=None):
        self.report = report
        self.db = db

    def create(self):
        loc = send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        self.report.add('lat', lat)
        self.report.add('lon', lon)
        self.report.add('ts', str(datetime.datetime.now()))

        self.db.water_reports.insert_one(self.report.json)

    def get_all(self):
        toRet = []
        for found in self.db.water_reports.find({}):
            toRet.append(found)
        return toRet

class Report(object):
    def __init__(self, water_type, water_quality, user):
        self.json = {}
        self.json['type'] = water_type
        self.json['quality'] = water_quality
        self.json['name'] = user

    def add(self, field, data):
        self.json[field] = data

class QualityReportManager(object):

    def __init__(self, report=None, db=None):
        self.report = report
        self.db = db

    def create(self):
        loc = send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        self.report.add('lat', lat)
        self.report.add('lon', lon)
        self.report.add('ts', str(datetime.datetime.now()))

        self.db.quality_reports.insert_one(self.report.json)

    def get_all(self):
        toRet = []
        for found in self.db.quality_reports.find({}):
            toRet.append(found)
        return toRet
        
class QualityReport(object):
    def __init__(self, virus_ppm, contaminant_ppm, quality, user):
        self.json = {}
        self.json['virus_ppm'] = virus_ppm
        self.json['contaminant_ppm'] = contaminant_ppm
        self.json['quality'] = quality
        self.json['user'] = user

    def add(self, field, data):
        self.json[field] = data
