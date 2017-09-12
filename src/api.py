#!/usr/bin/env python3
# Uses pieces from bitmessagecli.py and api.py
# Credit for bitmessagecli.py: Adam Melton (Dokument), Scott King (Lvl4Sword)
# Credit for api.py: Bitmessage developers, Peter Surda (Shurdeek)
# Created for use in the Taskhive project (taskhive.io)
# Distributed under the MIT/X11 software license (http://www.opensource.org/licenses/mit-license.php)
# https://bitmessage.org/wiki/API_Reference for Bitmessage API documentation
# Taskhive API documentation is a work in progress

import base64
import configparser
import datetime
import json
import os
import sys
import xml
import psutil
from bitmessage.debug import logger
import address_generator
from address_generator import VERSION_BYTE

APPNAME = 'Taskhive'
CONFIG = configparser.ConfigParser()
TASKHIVE_DIR = os.path.dirname(os.path.abspath(__file__))
BITMESSAGE_DIR = os.path.join(TASKHIVE_DIR, 'bitmessage')
BITMESSAGE_PROGRAM = os.path.join(BITMESSAGE_DIR, 'bitmessagemain.py')
KEYS_FILE = os.path.join(BITMESSAGE_DIR, 'keys.dat')
EXPECTED_SETTINGS = frozenset(['apienabled','apiinterface','apipassword',
'apiport','apiusername','blackwhitelist','daemon','defaultnoncetrialsperbyte',
'defaultpayloadlengthextrabytes','digestalg','hidetrayconnectionnotifications',
'identiconsuffix','keysencrypted','maxacceptablenoncetrialsperbyte',
'maxacceptablepayloadlengthextrabytes','maxdownloadrate','maxoutboundconnections',
'maxuploadrate','messagesencrypted','minimizeonclose','minimizetotray',
'namecoinrpchost','namecoinrpcpassword','namecoinrpcport','namecoinrpctype',
'namecoinrpcuser','onionbindip','onionhostname','onionport','opencl','port',
'replybelow','sendoutgoingconnections','settingsversion','showtraynotifications',
'smtpdeliver','socksauthentication','sockshostname','sockslisten','sockspassword',
'socksport','socksproxytype','socksusername','startintray','startonlogon',
'stopresendingafterxdays','stopresendingafterxmonths','timeformat','trayonclose',
'ttl','useidenticons','userlocale','willinglysendtomobile'])


# error codes
#  0 - quitting voluntarily
#  1 - quitting non-voluntarily, reason: []
#  2 - bitmessage folder missing
#  3 - can not find our bitmessagemain.py
#  4 - keys.dat not found, file: []
#  5 - configuration information is missing. information: [], file: []
#  6 - incorrect bitmessagesettings option provided
#  7 - now running our bitmessage daemon
#  8 - our bitmessage is already running
#  9 - can not connect to bitmessage api
class APIError(Exception):
    def __init__(self, error_number, error_message):
        super(APIError, self).__init__()
        self.error_number = error_number
        self.error_message = error_message

    def __str__(self):
        return "Taskhive API Error - Code:({0:d}) Message:({1:s})".format(self.error_number, self.error_message))


class Taskhive(object):
    def verify_settings(self)
        CONFIG.read(KEYS_FILE)
        missing_options = []
        extra_options = []
        if 'bitmessagesettings' in CONFIG.sections():
            bitmessagesettings = CONFIG.options('bitmessagesettings')
            for each in EXPECTED_SETTINGS:
                if each in bitmessagesettings:
                    pass
                else:
                    missing_options.append(each)
            for each in bitmessagesettings:
                if each in EXPECTED_SETTINGS:
                    pass
                else:
                    extra_options.append(each)
            if len(missing_options) >= 1 or len(extra_options) >= 1:
                return missing_options, extra_options
        else:
            return 'bitmessagesettings section missing'

    def keys_file_exist(self):
        if os.path.isfile(KEYS_FILE):
            CONFIG.read(KEYS_FILE)
        else:
            return 'our keys file is missing'

    def create_bitmessage_api(self):
        self.verify_settings()
        api_username = CONFIG.get('bitmessagesettings', 'apiusername')
        api_password = CONFIG.get('bitmessagesettings', 'apipassword')
        api_interface = CONFIG.get('bitmessagesettings', 'apiinterface')
        api_port = CONFIG.getint('bitmessagesettings', 'apiport')
        # Build the api credentials
        return 'http://{0}:{1}@{2}:{3}/'.format(api_username,
                                                api_password,
                                                api_interface,
                                                api_port)

    def generate_and_store_keys(self):
        private_key = address_generator.generate_key()
        public_key = address_generator.private_to_public(private_key)
        address = address_generator.address_from_public(public_key)
        address_encoded = address_generator.base58_check_encoding(address)
        self.keys_file_exist()
        if 'taskhivekeys' not in CONFIG.sections():
            CONFIG.add_section('taskhivekeys')
        CONFIG.set('taskhivekeys', 'private', private_key)
        CONFIG.set('taskhivekeys', 'public', public_key)
        CONFIG.set('taskhivekeys', 'address', address)
        CONFIG.set('taskhivekeys', 'address_encoded' address_encoded)
        with open(self.keys_file, 'wb') as configfile:
            CONFIG.write(configfile)
        return private_key, public_key, address, address_encoded

    def retrieve_keys(self):
        self.keys_file_exist()
        if 'taskhivekeys' in CONFIG.sections():
            CONFIG.add_section('taskhivekeys')
            private_key = CONFIG.get('taskhivekeys', 'private')
            public_key = CONFIG.get('taskhivekeys', 'public')
            address = CONFIG.get('taskhivekeys', 'address')
            address_encoded = CONFIG.get('taskhivekeys', 'address_encoded')
            return private_key, public_key, address, address_encoded            
        else:
            return 'no taskhivekeys section'

    def find_running_bitmessage_port(self):
        for process in psutil.process_iter():
            cmdline = process.cmdline()
            for each in cmdline:
                if 'bitmessagemain' in each:
                    bitmessage_dict[process.pid] = {}
                    for x in process.open_files():
                        break
                    keysfile = os.path.join(os.path.dirname(x.path), 'keys.dat')
                    if os.path.isfile(keysfile):
                        CONFIG.read(keysfile)
                        try:
                            bitmessage_port = CONFIG.getint('bitmessagesettings', 'port')
                        except NoOptionError:
                            raise APIError(5, 'configuration information is missing. information: [port], file: [{0}]'.format(keysfile))
                        except NoSectionError:
                           raise APIError(5, 'configuration information is missing. information: [bitmessagesettings], file: [{0}]'.format(keysfile))
                        else:
                            bitmessage_dict[process.pid]['file'] = each
                            bitmessage_dict[process.pid]['port'] = bitmessage_port
                            return json.dumps(bitmessage_dict, indent=4, separators=(',',': '))
                    else:
                        logger.warn('Taskhive API Error - Code:(4) Message:(keys.dat not found, file: [{0}]'.format(keysfile))
                        raise APIError(4, 'keys.dat not found, file: [{0}]'.format(keysfile))
                else:
                    pass

    def run_bitmessage(self):
        try:
            if sys.platform.startswith('win'):
                run_bm = subprocess.Popen(BITMESSAGE_PROGRAM),
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE,
                                          bufsize=0,
                                          cwd=TASKHIVE_DIR)
            else:
                run_bm = subprocess.Popen(BITMESSAGE_PROGRAM,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE,
                                          bufsize=0,
                                          cwd=TASKHIVE_DIR,
                                          preexec_fn=os.setpgrp,
                                          close_fds=True)
        except OSError:
            logger.warn('Taskhive API Error - Code:(3) Message:(can not find our bitmessagemain.py)')
            raise APIError(3, 'can not find our bitmessagemain.py')

    def shutdown_bitmessage(self):
        try:
            self.api.shutdown()
        except socket.error:
            sys.exit(0)
        except AttributeError, OSError:
            return 'shutdown'

    def bitmessagesettings_change_option(self, setting):
        if setting in EXPECTED_SETTINGS:
            CONFIG.read(KEYS_FILE)
            try:
                bitmessage_port = CONFIG.get('bitmessagesettings', setting)
            except configparser.NoSectionError:
                return 'corrupted keys.dat'
            except configparser.NoOptionError:
        else:
            raise APIError(6, 'incorrect bitmessagesettings option provided')

    # Tests the API connection to bitmessage.
    # Returns True if it is connected.
    def api_check(self):
        result = self.api.add(2,3)
        if result == 5:
            return True
        else:
            return False

    def valid_address(self, address):
        address_information = json.loads(self.api.decodeAddress(address))
        if address_information.get('status') == 'success':
            return True
        else:
            return False

    def get_address(self, passphrase):
        # passphrase must be encoded
        passphrase = base64.b64encode(passphrase)
        # TODO - stream_number shouldn't be hardcoded, but it's all we have right now.
        return(self.api.getDeterministicAddress(passphrase, version_number=4, stream_number=1)))

    def subscribe(self, address, label):
        if self.valid_address(address):
            label = base64.b64encode(label)
            subscription_check = self.api.addSubscription(address, label)
            if subscription_check == 'Added subscription.':
                return True
            else:
                
        else:
            return False

    def unsubscribe(self, address):
        if self.valid_address(address):
            verify = self.api.deleteSubscription(address)
            if verify:
                return True
            else:
                return False

    def list_subscriptions(self):
        total_subscriptions = json.loads(self.api.listSubscriptions())
        return total_subscriptions

    def create_chan(self, password):
        password = base64.b64encode(password)
        return(self.api.createChan(password))
 
    def join_chan(self, address, password):
        if self.valid_address(address):
            password = base64.b64encode(password)
            joining_channel = self.api.joinChan(password, address)
            if joining_channel == 'success':
                return True
            # TODO - This should probably be done better
            elif joining_channel.endswith('list index out of range'):
                return 'Already participating.'

    def leave_chan(self, address):
        if self.valid_address(address):
            leaving_channel = self.api.leaveChan(address)
            if leaving_channel == 'success':
                return True
            else:
                return False

    # Lists all of the addresses and their info
    def list_add(self):
        json_load_addresses = json.loads(self.api.listAddresses())
        json_addresses = json_load_addresses['addresses']
        if not json_addresses:
            return False
        else:
            return json_addresses

    # Generate address
    def generate_address(self, label, deterministic, passphrase, number_of_addresses,
                         address_version_number, stream_number, ripe):
        # Generates a new address with the user defined label, non-deterministic
        if deterministic is False:
            address_label = base64.b64encode(label)
            generated_address = self.api.createRandomAddress(address_label)
            return generated_address
        # Generates a new deterministic address with the user inputs
        elif deterministic is True:
            passphrase = base64.b64encode(passphrase)
            generated_address = self.api.createDeterministicAddresses(passphrase, number_of_addresses, address_version_number, stream_number, ripe)
            return generated_address
        else:
            return False

    def delete_address(self, address):
        json_load_addresses = json.loads(self.api.listAddresses())
        json_addresses = json_load_addresses['addresses']
        number_of_addresses = len(json_addresses['addresses'])
        if not json_addresses:
            return False
        else:
            if self.valid_address(address):
                delete_this = self.api.deleteAddress(address)
                if delete_this == 'success':
                    return True
                else:
                    return delete_this

    def send_message(self, to_address, from_address, subject, message):
        # TODO - Was using .encode('UTF-8'), not needed?
        json_addresses = json.loads(self.api.listAddresses())
        if not self.valid_address(to_address):
            return 'invalid to address'
        if not self.valid_address(from_address):
            return 'invalid from address'
        else:
            if from_address not in json_addresses:
                return 'not our address'
        subject = base64.b64encode(subject)
        message = base64.b64encode(message)
        ack_data = self.api.sendMessage(to_address, from_address, subject, message)
        sending_message = self.api.getStatus(ack_data)
        return sending_message

    def send_broadcast(self, from_address, subject, message):
        json_addresses = json.loads(self.api.listAddresses())
        if not self.valid_address(from_address):
            return 'invalid from address'
        else:
            if from_address not in json_addresses:
                return 'not our address'
        subject = base64.b64encode(subject)
        message = base64.b64encode(message)
        ack_data = self.api.sendBroadcast(from_address, subject, message)
        sending_broadcast = self.api.getStatus(ack_data)
        return sending_broadcast

    def inbox(self, unread_only):
        json_messages = json.loads(self.api.getAllInboxMessages())
        inbox_messages = json_messages['inboxMessages']
        return inbox_messages

    def outbox(self):
        json_messages = json.loads(self.api.getAllSentMessages())
        outbox_outbox = json_messages['sentMessages']
        return json_outbox

    def read_sent_message(self, message_number):
        outbox_messages = json.loads(self.api.getAllSentMessages())
        total_messages = len(outbox_messages['sentMessages'])
        if message_number >= total_messages:
            return 'invalid message number'
        else:
            return base64.b64decode(outbox_messages['sentMessages'][message_number])

    # Opens an inbox message for reading
    def read_inbox_message(self, message_number):
        inbox_messages = json.loads(self.api.getAllInboxMessages())
        total_messages = len(inbox_messages['inboxMessages'])
        if message_number >= total_messages:
            return 'invalid message number'
        else:
            return base64.b64decode(inbox_messages['inboxMessages'][message_number])

# Task requests and offers have an identical JSON array format, differing only in task_type.
#   [{
#   "task_data":{
#   "task_type":"offer",
#   "task_categories":[ A1, C4C1, F122, … ],
#   "task_title":"Write a short story for my cat blog",
#   "task_body":"I have a cat blog that needs a story written for it. I will pay for a story about cats.",
#   "task_keywords":[ "cats", "blog", "writing"],
#   "task_references":[ "URL1", "URL2", … ],
#   "task_cost":"0.001",
#   "task_currency":"BTC",
#   "task_payment_rate_type":"task",
#   "task_payment_methods":[ "BTC", "DOGE"],
#   "task_deadline":1482710400,
#   "task_license":"CC BY 4.0",
#   "task_escrow_required":1,
#   "task_escrow_recommendation":"BITCOIN-PUBKEY",
#   "task_address":"TEMP-BM-ADDRESS",
#   "task_owner":"BITCOIN-PUBKEY",
#   "task_id":"YsBGsF3dc9But9GN5mXOTwEFIZWZ8=",
#   "task_entropy":"LATEST-BLOCKCHAIN-HASH",
#   "task_expiration":1482710400
#   },
#   "task_data_signed":"IKQ2TXYsBGsF3dc9But9GN/TNhW5mXOTwEFIZWZ8="
#   }]

# terminate
#   [{
#   "task_data":{
#   "task_type":"terminate",
#   "task_id":"YsBGsF3dc9But9GN5mXOTwEFIZWZ8=",
#   "task_owner":"BITCOIN-PUBKEY"
#   },
#   "task_data_signed":"IKDrBFLmzUJyG1d6iuoP7zZDley8bBYh="
#   }]

    def create_request_json(self:

    def create_offer_json(self):

    def create_terminate_json(self):

    def verify_request_json(self:

    def verify_offer_json(self:

    def verify_terminate_json(self:

    def read_request_json(self:

    def read_offer_json(self):

    def read_terminate_json(self):

    def unread_message_info(self):
        inbox_messages = json.loads(self.api.getAllInboxMessages())
        CONFIG.read(self.keys_file)
        unread_messages = 0
        for each in inbox_messages['inboxMessages']:
            if not each['read']:
                if each['toAddress'] in CONFIG.sections():
                    unread_messages += 1
        # If the bitmessageheader is there, AND you have at least one address
        if unread_messages >= 1 and len(CONFIG.sections()) >= 2:
            return unread_messages
        else:
            return 0

    def client_status(self):
        status = json.loads(self.api.clientStatus())
        if status['networkStatus'] == 'notConnected':
            connection = 'RED'
        elif status['networkStatus'] == 'connectedButHaveNotReceivedIncomingConnections':
            connection = 'YELLOW'
        else:
            connection = 'GREEN'
        return connection

    def client_connections(self):
        status = json.loads(self.api.clientStatus())
        connections = status['networkConnections']
        pubkeys = status['numberOfPubkeysProcessed']
        messages = status['numberOfMessagesProcessed']
        broadcasts = status['numberOfBroadcastsProcessed']
        return connections, pubkeys, messages, broadcasts

    def preparations(self):
        self.api_data()
        self.bitmessage_api = xmlrpclib.ServerProxy(self.return_api())
        self.run_bitmessage()

if __name__ == "__main__":
    print('The API should never be called directly.')
    sys.exit(0)
