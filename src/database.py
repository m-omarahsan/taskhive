from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
import base64


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




Base.metadata.create_all(engine)


def generateCategories():
	with open('categories.txt', 'r') as f:
		for line in f.readlines():
			if line.strip():
				elements = line.split()
				hex_code = elements[0]
				name = elements[1]
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


