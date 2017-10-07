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
import ipaddress
import json
import os
import random
import socket
import string
import subprocess
import sys
import xml
import psutil
import xmlrpc.client
import address_generator
import database
from address_generator import VERSION_BYTE
from change import CRYPTO_COINS
from change import CURRENCIES
from lib import bitcoin

APPNAME = 'Taskhive'
CHARACTERS = string.digits + string.ascii_letters
CONFIG = configparser.ConfigParser()
SECURE_RANDOM = random.SystemRandom()
RANDOM_INT = random.randint(50, 150)

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
        return "Taskhive API Error - Code:({0:d}) Message:({1:s})".format(self.error_number, self.error_message)


class Taskhive(object):
    def __init__(self):
        self.api = ''
        self.run_bm = ''
        self.bitmessage_dict = {}

    def find_running_bitmessage_port(self):
        self.bitmessage_dict = {}
        for process in psutil.process_iter():
            process_name = process.name()
            process_path = None
            if sys.platform.startswith('win'):
                if 'python' in process_name:
                    for each in process.cmdline():
                        if 'bitmessagemain' in each:
                            self.bitmessage_dict[process.pid] = {}
                            process_path = each
            else:
                if 'bitmessagemain' in process_name:
                    for each in process.cmdline():
                        if 'bitmessagemain' in each:
                            self.bitmessage_dict[process.pid] = {}
                            process_path = each
            if process_path is not None:
                keysfile = os.path.join(os.path.dirname(process_path), 'keys.dat')
                if os.path.isfile(keysfile):
                    CONFIG.read(keysfile)
                else:
                    keysfile = os.path.join(self.lookup_appdata_folder(), 'keys.dat')
                    if os.path.isfile(keysfile):
                        CONFIG.read(keysfile)
                    else:
                        print("Can't find keysfile?")
                        break
                try:
                    bitmessage_port = CONFIG.getint('bitmessagesettings', 'port')
                except configparser.NoOptionError:
                    print('port is missing from', keysfile)
                except configparser.NoSectionError:
                    print('bitmessagesettings section is missing from', keysfile)
                try:
                    bitmessage_apiport = CONFIG.getint('bitmessagesettings', 'apiport')
                except configparser.NoOptionError:
                    print('apiport is missing from', keysfile)
                except configparser.NoSectionError:
                    print('bitmessagesettings section is missing from', keysfile)
                self.bitmessage_dict[process.pid]['file'] = each
                self.bitmessage_dict[process.pid]['port'] = bitmessage_port
                self.bitmessage_dict[process.pid]['apiport'] = bitmessage_apiport
        return self.bitmessage_dict

    def bitmessage_port_picker(self):
        check_bitmessage_ports = self.find_running_bitmessage_port()
        port_list = []
        apiport_list = []
        bitmessage_port = None
        bitmessage_apiport = None
        try:
            for each in check_bitmessage_ports.values():
                port_list.append(each['port'])
                apiport_list.append(each['apiport'])
        except (AttributeError, KeyError):
            pass
        # 17600 - 17650 is set for OnionShare in the Tails OS.
        # If this is randomized, it won't work.
        # Thus, won't connect using xmlrpclib.
        for each in range(8444, 8501):
            if each not in port_list:
                bitmessage_port = each
                break
        for each in range(17600, 17651):
            if each not in apiport_list:
                bitmessage_apiport = each
                break
        # This should never happen, because that would mean 66 ports are
        # being taken up for the Bitmessage port, or 50 for the apiport.
        # This should be done better, but even psutil isn't giving us
        # xmlrpc ports in-use.
        if bitmessage_port is None or bitmessage_apiport is None: 
            return None
        else:
            return bitmessage_port, bitmessage_apiport

    def create_settings(self):
        bitmessage_port, bitmessage_apiport = self.bitmessage_port_picker()
        try:
            CONFIG.add_section('bitmessagesettings')
        except configparser.DuplicateSectionError:
            pass
        CONFIG.set('bitmessagesettings', 'port', str(bitmessage_port))
        CONFIG.set('bitmessagesettings', 'settingsversion', '10')
        CONFIG.set('bitmessagesettings', 'apiport', str(bitmessage_apiport))
        CONFIG.set('bitmessagesettings', 'apiinterface', 'localhost')
        CONFIG.set('bitmessagesettings', 'apiusername',
                   ''.join([SECURE_RANDOM.choice(CHARACTERS) for x in range(RANDOM_INT)]))
        CONFIG.set('bitmessagesettings', 'apipassword',
                   ''.join([SECURE_RANDOM.choice(CHARACTERS) for x in range(RANDOM_INT)]))
        CONFIG.set('bitmessagesettings', 'apienabled', 'True')
        CONFIG.set('bitmessagesettings', 'daemon', 'True')
        CONFIG.set('bitmessagesettings', 'timeformat', '%%c')
        CONFIG.set('bitmessagesettings', 'blackwhitelist', 'black')
        CONFIG.set('bitmessagesettings', 'startonlogon', 'False')
        CONFIG.set('bitmessagesettings', 'minimizetotray', 'False')
        CONFIG.set('bitmessagesettings', 'showtraynotifications', 'True')
        CONFIG.set('bitmessagesettings', 'startintray', 'False')
        CONFIG.set('bitmessagesettings', 'socksproxytype', '')
        CONFIG.set('bitmessagesettings', 'sockshostname', '')
        CONFIG.set('bitmessagesettings', 'socksport', '')
        CONFIG.set('bitmessagesettings', 'socksauthentication', 'False')
        CONFIG.set('bitmessagesettings', 'sockslisten', 'False')
        CONFIG.set('bitmessagesettings', 'socksusername', '')
        CONFIG.set('bitmessagesettings', 'sockspassword', '')
        CONFIG.set('bitmessagesettings', 'smtpdeliver', '')
        # https://www.reddit.com/r/bitmessage/comments/5vt3la/sha1_and_bitmessage/deev8je/
        CONFIG.set('bitmessagesettings', 'digestalg', 'sha256')
        CONFIG.set('bitmessagesettings', 'keysencrypted', 'False')
        CONFIG.set('bitmessagesettings', 'messagesencrypted', 'False')
        CONFIG.set('bitmessagesettings', 'defaultnoncetrialsperbyte', '1000')
        CONFIG.set('bitmessagesettings', 'defaultpayloadlengthextrabytes', '1000')
        CONFIG.set('bitmessagesettings', 'minimizeonclose', 'False')
        CONFIG.set('bitmessagesettings', 'maxacceptablenoncetrialsperbyte', '20000000000')
        CONFIG.set('bitmessagesettings', 'maxacceptablepayloadlengthextrabytes', '20000000000')
        CONFIG.set('bitmessagesettings', 'userlocale', 'system')
        CONFIG.set('bitmessagesettings', 'useidenticons', 'False')
        CONFIG.set('bitmessagesettings', 'identiconsuffix', '')
        CONFIG.set('bitmessagesettings', 'replybelow', 'False')
        CONFIG.set('bitmessagesettings', 'maxdownloadrate', '0')
        CONFIG.set('bitmessagesettings', 'maxuploadrate', '0')
        CONFIG.set('bitmessagesettings', 'maxoutboundconnections', '8')
        CONFIG.set('bitmessagesettings', 'ttl', '367200')
        CONFIG.set('bitmessagesettings', 'stopresendingafterxdays', '')
        CONFIG.set('bitmessagesettings', 'stopresendingafterxmonths', '')
        CONFIG.set('bitmessagesettings', 'namecoinrpctype', 'namecoind')
        CONFIG.set('bitmessagesettings', 'namecoinrpchost', 'localhost')
        CONFIG.set('bitmessagesettings', 'namecoinrpcuser', '')
        CONFIG.set('bitmessagesettings', 'namecoinrpcpassword', '')
        CONFIG.set('bitmessagesettings', 'namecoinrpcport', '')
        CONFIG.set('bitmessagesettings', 'sendoutgoingconnections', 'True')
        CONFIG.set('bitmessagesettings', 'onionhostname', '')
        CONFIG.set('bitmessagesettings', 'onionbindip', '')
        CONFIG.set('bitmessagesettings', 'onionport', '')
        CONFIG.set('bitmessagesettings', 'hidetrayconnectionnotifications', 'False')
        CONFIG.set('bitmessagesettings', 'trayonclose', 'False')
        CONFIG.set('bitmessagesettings', 'willinglysendtomobile', 'False')
        CONFIG.set('bitmessagesettings', 'opencl', 'None')
        with open(KEYS_FILE, 'w') as configfile:
           CONFIG.write(configfile)

#    def set_proxy_hostname(self, hostname):
#        CONFIG.read(KEY_FILE)
#        try:
#            ipaddress.ip_address(hostname)
#        except ValueError:
#            return 'invalid hostname'
#        else:
#            CONFIG.set('bitmessagesettings', 'sockshostname', hostname)
#            with open(KEYS_FILE, 'wb') as configfile:
#                CONFIG.write(configfile)

#    def set_proxy_type(self, proxy):
#        proxy_types = {'none': 'none', 'socks4a': 'SOCKS4a', 'socks5': 'SOCKS5'}
#        if proxy in proxy_types:
#            CONFIG.set('bitmessagesettings', 'socksproxytype', proxy)
#            with open(KEYS_FILE, 'wb') as configfile:
#                CONFIG.write(configfile)

    def verify_settings(self, keyfile):
        CONFIG.read(keyfile)
        missing_options = []
        extra_options = []
        incorrect_options = []
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
                return True
        else:
            return 'bitmessagesettings section missing'

    def keys_file_exists(self, keyfile):
        if os.path.isfile(keyfile):
            return True
        else:
            return False

    def create_bitmessage_api(self):
        key_file_existence = self.keys_file_exists(KEYS_FILE)
        verifying_settings = self.verify_settings(KEYS_FILE)
        print(verifying_settings)
        if key_file_existence is True:
            if verifying_settings is True:
                api_username = CONFIG.get('bitmessagesettings', 'apiusername')
                api_password = CONFIG.get('bitmessagesettings', 'apipassword')
                api_interface = CONFIG.get('bitmessagesettings', 'apiinterface')
                api_port = CONFIG.getint('bitmessagesettings', 'apiport')
                api_info = 'http://{0}:{1}@{2}:{3}/'.format(api_username,
                                                            api_password,
                                                            api_interface,
                                                            api_port)
                self.api = xmlrpc.client.ServerProxy(api_info)
                print(self.api_check())
            else:
                return 'invalid keys_file settings'
                
        else:
            return 'keyfile does not exist'

    def generate_and_store_keys(self):
        private_key = address_generator.generate_key()
        public_key = address_generator.private_to_public(private_key)
        address = address_generator.address_from_public(public_key, VERSION_BYTE)
        address_encoded = address_generator.base58_check_encoding(address)
        print(private_key, public_key, address, address_encoded)
        self.keys_file_exists(KEYS_FILE)
        self.verify_settings(KEYS_FILE)
        if 'taskhivekeys' not in CONFIG.sections():
            CONFIG.add_section('taskhivekeys')
        CONFIG.set('taskhivekeys', 'private', private_key)
        CONFIG.set('taskhivekeys', 'public', public_key)
        CONFIG.set('taskhivekeys', 'address', address)
        CONFIG.set('taskhivekeys', 'address_encoded', address_encoded)
        with open(KEYS_FILE, 'w') as configfile:
            CONFIG.write(configfile)

    def retrieve_keys(self):
        self.keys_file_exists(KEYS_FILE)
        self.verify_settings(KEYS_FILE)
        if 'taskhivekeys' in CONFIG.sections():
            #try:
            private_key = CONFIG.get('taskhivekeys', 'private')
            public_key = CONFIG.get('taskhivekeys', 'public')
            address = CONFIG.get('taskhivekeys', 'address')
            address_encoded = CONFIG.get('taskhivekeys', 'address_encoded')
            #except configparser.NoOptionError:
            return private_key, public_key, address, address_encoded
        else:
            return 'no taskhivekeys section'

    def lookup_appdata_folder(self):
        if sys.platform.startswith('darwin'):
            if 'HOME' in os.environ:
                keys_path = os.path.join(os.environ['HOME'],
                                         'Library/Application support/',
                                         APPNAME)
            else:
                return 'can not detect darwin keys_path'
        elif sys.platform.startswith('win'):
            keys_path = os.path.join(os.environ['APPDATA'], APPNAME)
        else:
            keys_path = os.path.join(os.path.expanduser('~'), '.config', APPNAME)
        return keys_path

    def run_bitmessage(self):
        try:
            if sys.platform.startswith('win'):
                self.run_bm = subprocess.Popen(BITMESSAGE_PROGRAM,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE,
                                               bufsize=0,
                                               cwd=TASKHIVE_DIR,
                                               shell=True)
                print("started running!")
            else:
                self.run_bm = subprocess.Popen(BITMESSAGE_PROGRAM,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE,
                                               bufsize=0,
                                               cwd=TASKHIVE_DIR,
                                               shell=True,
                                               preexec_fn=os.setpgrp,
                                               close_fds=True)
        except OSError:
            logger.warn('Taskhive API Error - Code:(3) Message:(can not find our bitmessagemain.py)')
            raise APIError(3, 'can not find our bitmessagemain.py')

    def shutdown_bitmessage(self):
        try:
            self.api.shutdown()
        except(AttributeError, OSError, socket.error) as e:
            return e

    def bitmessagesettings_change_option(self, setting):
        if setting in EXPECTED_SETTINGS:
            CONFIG.read(KEYS_FILE)
            try:
                bitmessage_setting = CONFIG.set('bitmessagesettings', setting)
            except configparser.NoSectionError:
                return 'corrupted keys.dat'
            except configparser.NoOptionError:
                return 'corrupted keys.dat'
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
        print(address_information)
        if address_information.get('status') == 'success':
            return True
        else:
            return False

    def get_address(self, passphrase):
        # passphrase must be encoded
        passphrase = base64.b64encode(passphrase)
        # TODO - stream_number shouldn't be hardcoded, but it's all we have right now.
        return(self.api.getDeterministicAddress(passphrase, version_number=4, stream_number=1))

    def subscribe(self, address, label):
        if valid_address(address):
            label = base64.b64encode(label)
            subscription_check = self.api.addSubscription(address, label)
            if subscription_check == 'Added subscription.':
                return True
            else:
                return False
        else:
            return False

    def unsubscribe(self, address):
        if self.valid_address(address):
            verify = self.api.deleteSubscription(address)
            if verify:
                return True
            else:
                return False
        else:
            return 'invalid address'

    def list_subscriptions(self):
        total_subscriptions = json.loads(self.api.listSubscriptions())
        return total_subscriptions

    def create_chan(self, password):
        password = base64.b64encode(password).decode('utf8')
        return self.api.createChan(password)
 
    def join_chan(self, address, password):
        if self.valid_address(address):
            password = base64.b64encode(bytes(password.encode('utf8'))).decode('utf8')
            print(address, password)
            joining_channel = self.api.joinChan(password, address)
            print(joining_channel)
            if joining_channel == 'success':
                return True
            else:
                return False
        else:
            return 'invalid address'

    def leave_chan(self, address):
        if self.valid_address(address):
            leaving_channel = self.api.leaveChan(address)
            if leaving_channel == 'success':
                return True
            else:
                return False
        else:
            return 'invalid address'

    # Lists all of the addresses and their info
    def list_add(self):
        json_load_addresses = json.loads(self.api.listAddresses())
        json_addresses = json_load_addresses['addresses']
        if not json_addresses:
            return False
        else:
            return json_addresses

    # Generate address
    def generate_address(self, deterministic=False, passphrase=None, number_of_addresses=1,
                         address_version_number=0, stream_number=0, ripe=False, label=None):
        # Generates a new address with the user defined label, non-deterministic
        if deterministic is False and label is not None:
            address_label = base64.b64encode(bytes(label.encode('utf8'))).decode('utf8')
            generated_address = self.api.createRandomAddress(address_label)
            return generated_address
        # Generates a new deterministic address with the user inputs
        elif deterministic is True:
            # passphrase = base64.b64encode(passphrase)
            generated_address = self.api.createDeterministicAddresses(passphrase.decode('utf8'), number_of_addresses, address_version_number, stream_number, ripe)
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
            else:
                return 'invalid address'

    def send_message(self, to_address, from_address, subject, message):
        # TODO - Was using .encode('UTF-8'), not needed?
        json_addresses = json.loads(self.api.listAddresses())
        JSON_add = json_addresses['addresses']
        addresses = []
        for add in JSON_add:
            addresses.append(add['address'])
        if not self.valid_address(to_address):
            return 'invalid to address'
        if not self.valid_address(from_address):
            return 'invalid from address'
        else:
            if from_address not in addresses:
                return 'not our address'
        subject = base64.b64encode(bytes(subject.encode('utf8'))).decode('utf8')
        message = base64.b64encode(bytes(message.encode('utf8'))).decode('utf8')
        ack_data = self.api.sendMessage(to_address, from_address, subject, message)
        print(ack_data)
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
        json_outbox = json_messages['sentMessages']
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


    def setup_channels(self):
        channels = database.getChannels()
        channel_addresses = []
        self.api.check()
        for channel in channels:
            print(channel.encoded_name)       
            address = self.generate_address(True,channel.encoded_name,1, 0,0,False)
            print(address)

    def test_channels(self):
        #channel = self.create_chan(b'dGFza2hpdmVfb2ZmZXJzXzAx')
        #print("ADDRESS: ", channel)
        #response = self.join_chan('BM-2cVQgSEDtYSYUU2wh5SFmXA1fNd4uDWQLa', 'dGFza2hpdmVfb2ZmZXJzXzAx')
        #if response:
        #    print("We did it, reddit!")
        randomAddress = self.generate_address(label='TestAddress')
        print(randomAddress)
        message = self.send_message('BM-2cVQgSEDtYSYUU2wh5SFmXA1fNd4uDWQLa', randomAddress, 'TESTING PLEASE, WORK', 'TEST #1')
        print(message)
        print(self.outbox())


    def create_request_json(self, task_INFO):
        task_id = address_generator.generate_key()
        preliminary_json = {}
        final_signed_json = {}
        task_json = json.loads(task_INFO)
        private_key, public_key, address, address_encoded = self.retrieve_keys()
        try:
            preliminary_json['task_type'] = task_json['task_type']
            preliminary_json['task_categories'] = task_json['task_categories']
            preliminary_json['task_title'] = task_json['task_title']
            preliminary_json['task_body'] = task_json['task_body']
            preliminary_json['task_keywords'] = task_json['task_keywords']
            preliminary_json['task_references'] = task_json['task_references']
            preliminary_json['task_cost'] = task_json['task_cost']
            preliminary_json['task_currency'] = task_json['task_currency']
            preliminary_json['task_payment_methods'] = task_json['task_payment_methods']
            preliminary_json['task_payment_rate_type'] = task_json['task_payment_rate_type']
            preliminary_json['task_deadline'] = task_json['task_deadline']
            preliminary_json['task_license'] = task_json['task_license']
            preliminary_json['task_escrow_required'] = task_json['task_escrow_required']
            preliminary_json['task_escrow_recommendation'] = task_json['task_escrow_recommendation']
            preliminary_json['task_address'] = task_json['task_address']
            preliminary_json['task_owner'] = public_key
            preliminary_json['task_id'] = task_id
            preliminary_json['task_entropy'] = 'CURRENTLY-NOT-IN-USE'
            preliminary_json['task_expiration'] = task_json['task_expiration']
        except KeyError:
            return "Invalid data" 

        json_string = json.dumps(preliminary_json)
        wif_private_key = address_generator.private_to_wif(private_key, address_generator.WIF_VERSION_BYTE, address_generator.TYPE_PUB)
        sign = bitcoin.sign_message_with_wif_privkey(wif_private_key, json_string)
        encoded_sign = base64.b64encode(sign)
        print(json_string)
        final_signed_json['task_data'] = json_string
        final_signed_json['task_data_signed'] = encoded_sign.decode('utf-8')
        self.generate_address
        bit_address = self.create_chan('testtaskhive')
        if self.join_chan(bit_address, 'testtaskhive'):
            print("Successfully joined")
            self.send_message('')

        return final_signed_json
    
    def verify_request_json(self, json_data, task_owner):
        data = json.loads(json_data)
        signature = bytes(data['task_data_signed'].encode('utf8'))
        decoded_sign = base64.b64decode(signature)
        temporary_json = json.loads(data['task_data'])
        owner_public_key = temporary_json['task_owner']
        add  = address_generator.address_from_public(bytes(owner_public_key.encode('utf8')), VERSION_BYTE) 
        encoded_address = address_generator.base58_check_encoding(add)
        json_string = json.dumps(data['task_data'])
        result = bitcoin.verify_message(encoded_address, decoded_sign, bytes(data['task_data'].encode('utf8')))
        return result


# Task requests and offers have an identical JSON array format, differing only in task_type.
#   [{
#   "task_data":{
#   "task_type":"offer",
#   "task_categories":[ A1, C4C1, F122, ... ],
#   "task_title":"Write a short story for my cat blog",
#   "task_body":"I have a cat blog that needs a story written for it. I will pay for a story about cats.",
#   "task_keywords":[ "cats", "blog", "writing"],
#   "task_references":[ "URL1", "URL2", ... ],
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

#    def create_request_json(self:

#    def create_offer_json(self):

#    def create_terminate_json(self):

#    def verify_request_json(self):

#    def verify_offer_json(self):

#    def verify_terminate_json(self):

#    def read_request_json(self):

#    def read_offer_json(self):

#    def read_terminate_json(self):

    def unread_message_info(self):
        inbox_messages = json.loads(self.api.getAllInboxMessages())
        CONFIG.read(KEYS_FILE)
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

    # This isn't ready
    def preparations(self):
        self.run_bitmessage()

if __name__ == "__main__":
    print('The API should never be called directly.')
    sys.exit(0)
