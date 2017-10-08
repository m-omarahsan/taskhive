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

class Channel(Base):

	__tablename__ = 'channel'
	channel_ID = Column(Integer, primary_key=True)
	channel_HEX = Column(String)
	name = Column(String)
	encoded_name = Column(String)
	bit_address = Column(String)
	channel_type = Column(Integer, ForeignKey('channeltype.id'))

	def __repr__(self):
		return "<Channel(channel_HEX='{}', name='{}')>".format(self.channel_HEX, self.name)

Base.metadata.create_all(engine)


def getChannels():
	return ses.query(Channel).all()


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
		chan = Channel(
			channel_HEX=channel['hex'],
			name=channel['name'],
			encoded_name=channel['encoded_name'],
			channel_type=channel['type'],
			bit_address=channel['bit_address']
		)
		ses.add(chan)
	ses.commit()


