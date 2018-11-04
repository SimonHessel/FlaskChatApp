from database import *

db=Database()

class user():
    def __init__(self,  '''name, vorname, nutzername, geburtsdatum, geschlecht, email, biography'''):
	'''
        self.name=name
        self.vorname=vorname
        self.geburtsdatum=geburtsdatum
        self.geschlecht=geschlecht
        self.email=email
        self.biography=biography
        self.friends=None
	'''
		self.data = db.get(SELECT * FROM 'users' WHERE username = 'hessesim00', )
	
    def get.name(self):
        return self.data[2]

    def get.vorname(self):
        return self.data[1]

    def get.geburtsdatum(self):
        return self.data[5]

    def get.geschlecht(self):
        return self.data[6]

    def get.email(self):
        return self.data[7]

    def get.biography(self):
        pass

    def set.biography(self):
		pass


    def get.friends(self):
        pass



