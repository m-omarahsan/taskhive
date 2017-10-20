from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError


engine = create_engine('sqlite:///taskhive.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

ses = Session()

class ChannelType(Base):
	__tablename__ = 'channeltype'
	id = Column(Integer, primary_key=True)
	name = Column(String)


class Category(Base):
	__tablename__ = 'category'
	id = Column(String, primary_key=True)
	name = Column(String)

class Channel(Base):

	__tablename__ = 'channel'
	channel_ID = Column(Integer, primary_key=True)
	channel_HEX = Column(String, ForeignKey('category.id'))
	name = Column(String)
	encoded_name = Column(String)
	bit_address = Column(String)
	channel_type = Column(Integer, ForeignKey('channeltype.id'))

	def __repr__(self):
		return "<Channel(channel_HEX='{}', name='{}')>".format(self.channel_HEX, self.name)


class Profile(Base):

	__tablename__ = 'profile'
	id = Column(String, primary_key=True)
	handle = Column(String)
	public_key = Column(String)
	address = Column(String)
	address_encoded = Column(String)
	privacy_level = Column(Integer)


class UserCategories(Base):
	__tablename__ = 'usercategories'
	id = Column(Integer, primary_key=True)
	hex_code = Column(String, ForeignKey('category.id'))
	profile = Column(String, ForeignKey('profile.id'))


Base.metadata.create_all(engine)


def getCategories():
	cats = []
	for cat in ses.query(Category).all():
		cats.append({
			"hex": cat.id,
			"name": cat.name
			})
	return cats


def generateCategories():
	with open('categories.txt', 'r') as f:
		for line in f.readlines():
			if line.strip():
				elements = line.split()
				hex_code = elements[0]
				name = ''.join([el + ' ' for el in elements[1:]]).strip()
				new_cat = Category(id=hex_code, name=name)
				ses.add(new_cat)
				try:
					ses.commit()
				except IntegrityError:
					ses.rollback()


def getChannelTypes():
	return ses.query(ChannelType).all()


def getChannels():
	return ses.query(Channel).all()

def getChannelByCategory(category_hex):
	channels = []
	for category in category_hex:
		cat = [category[i:i+2] for i in range(0, len(category), 2)][0]
		chan = ses.query(Channel).filter_by(channel_HEX=cat).first()
		print(cat, category)
		if chan is not None:
			if chan.channel_HEX in channels:
				continue
			channels.append(chan)
	return channels


def createChannelTypes(types=['Offers', 'Requests']):
	for t in types:
		result = ses.query(ChannelType).filter_by(name=t).first()
		if not result:
			typ = ChannelType(name=t)
			ses.add(typ)
	ses.commit()
	return ses.query(ChannelType).all()



def getProfile():
	try:
		profile = ses.query(Profile).all()[0]
	except:
		return False
	categoriesInfo = ses.query(UserCategories).filter_by(id=profile.id).first()
	return ses.query(Profile).all()



def createProfile(profile_DATA):
	new_prof = Profile(
		id=profile_DATA['private_key'],
		handle=profile_DATA['handle'],
		public_key=profile_DATA['public_key'],
		address=profile_DATA['address'],
		address_encoded=profile_DATA['address_encoded'],
		privacy_level=profile_DATA['privacy_level']
	)
	ses.add(new_prof)
	for cat in profile_DATA['categories']:
		new_usercat = UserCategories(hex_code=cat['hex_code'], profile=profile_DATA['private_key'])
		ses.add(new_usercat)
	ses.commit()



def storeChannels(channelInfo):
	for channel in channelInfo:
		try:
			chan = Channel(
				channel_HEX=channel['hex'],
				name=channel['name'],
				encoded_name=channel['encoded_name'],
				channel_type=channel['type'],
				bit_address=channel['bit_address']
			)
			ses.add(chan)
			ses.commit()
		except IntegrityError:
			ses.rollback()


