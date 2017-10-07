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


if __name__ == '__main__':
	channels = [
	{'hex':'01', 'name':'Video'},
	{'hex':'02', 'name':'Audio'},
	{'hex':'03', 'name':'Graphics and Art'},
	{'hex':'04', 'name':'Reading and Writing'},
	{'hex':'05', 'name':'Teaching and Consulting'},
	{'hex':'06', 'name':'Engineering'},
	{'hex':'07', 'name':'Administrative / Business / Legal'},
	{'hex':'08', 'name':'Misc'}]
	chn_type = ChannelType(name='Requests')
	chn_type2 = ChannelType(name='Offers')
	ses.add_all([chn_type, chn_type2])
	ses.commit()
	for channel in channels:
		try:
			offers = 'taskhive_offers_{}'.format(channel['hex'])
			requests = 'taskhive_requests_{}'.format(channel['hex'])
			encoded_offers_name = base64.b64encode(bytes(offers.encode('utf8'))) 
			encoded_requests_name = base64.b64encode(bytes(requests.encode('utf8')))
			new_req_chan = Channel(channel_HEX=channel['hex'], name=channel['name'], encoded_name=encoded_requests_name, channel_type=1)
			new_offer_chan = Channel(channel_HEX=channel['hex'], name=channel['name'], encoded_name=encoded_offers_name, channel_type=2)
			ses.add_all([new_offer_chan, new_req_chan])
			ses.commit()
		except IntegrityError:
			ses.rollback()
			continue

	all_channels = ses.query(Channel).all()
	for chan in all_channels:

		print(chan.name, ses.query(ChannelType).filter_by(id=chan.channel_type).first().name, chan.encoded_name)


