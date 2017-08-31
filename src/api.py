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
# 0 - quitting voluntarily
# 1 - quitting non-voluntarily, reason: []
# 2 - bitmessage folder missing
# 3 - can not find our bitmessagemain.py
# 4 - keys.dat not found, file: []
# 5 - configuration information is missing. information: [], file: []
# 6 - incorrect bitmessagesettings option provided
# 7 - now running our bitmessage daemon
# 8 - our bitmessage is already running
# 9 - can not connect to bitmessage api
class APIError(Exception):
    def __init__(self, error_number, error_message):
        super(APIError, self).__init__()
        self.error_number = error_number
        self.error_message = error_message

    def __str__(self):
        return "Taskhive API Error - Code:[{0:d}] Message:[{1:s}]".format(self.error_number, self.error_message))


class Taskhive(object):
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
                        except(NoSectionError, NoOptionError):
                            return 'corrupted keys.dat'
                        else:
                            bitmessage_dict[process.pid]['file'] = each
                            bitmessage_dict[process.pid]['port'] = bitmessage_port
                            return json.dumps(bitmessage_dict, indent=4, separators=(',',': '))
                    else:
                        return 'keys.dat not found'
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
            raise APIError(5, 'can not find our bitmessagemain.py')

    def shutdown_bitmessage(self):
        try:
            self.api.shutdown()
        except socket.error:
            print('Socket Error')
        except(AttributeError, OSError):
            print('AttributeError / OSError')

    def verify_settings(self)
        CONFIG.read(KEYS_FILE)
        missing_options = []
        extra_options = []
        if 'bitmessagesettings' in CONFIG.sections():
            bitmessagesettings = CONFIG['bitmessagesettings']
            for each in EXPECTED_SETTINGS:
                if each in bitmessagesettings:
                    pass
                else:
                    missing_options.append(each)
            if len(missing_options) >= 1:
                APIError(Exception)
            for each in bitmessagesettings:
                if each in EXPECTED_SETTINGS:
                    pass
                else:
                    extra_options.append(each)

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

    # Allows you to reply to the message you are currently on.
    # Saves typing in the addresses and subject.
    def reply_message(message_number, forward_or_reply):
        inboxMessages = json.loads(self.api.getAllInboxMessages())
        # Address it was sent To, now the From address
        from_address = inboxMessages['inboxMessages'][message_number]['toAddress']
        # Message that you are replying to
        message = base64.b64decode(inboxMessages['inboxMessages'][message_number]['message'])
        subject = inboxMessages['inboxMessages'][message_number]['subject']
        subject = base64.b64decode(subject)
        if forward_or_reply == 'reply':
            # Address it was From, now the To address
            to_address = inboxMessages['inboxMessages'][message_number]['fromAddress']
            subject = 'Re: {0}'.format(subject)
        elif forward_or_reply == 'forward':
            subject = 'Fwd: {0}'.format(subject)
            while True:
                to_address = self.user_input('What is the To Address?')
                if not self.valid_address(to_address):
                    print('Invalid Address. Please try again.')
                else:
                    break
        else:
            print('Invalid Selection. Reply or Forward only')
            return
        subject = base64.b64encode(subject)
        new_message = self.user_input('Enter your Message.')
        self.send_message(to_address, from_address, subject, new_message)

    # Deletes a specified message from the outbox
    def delete_sent_message(self, message_number):
        try:
            outbox_messages = json.loads(self.api.getAllSentMessages())
            # gets the message ID via the message index number
            # TODO - message_number is wrapped in an int(), needed?
            message_id = outbox_messages['sentMessages'][int(message_number)]['msgid']
            message_ack = self.api.trashSentMessage(message_id)
            return message_ack
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t delete message due to an API connection issue')

    def list_address_book(self):
        try:
            response = self.api.listAddressBookEntries()
            if 'API Error' in response:
                return self.get_api_error_code(response)
            address_book = json.loads(response)
            if address_book['addresses']:
                print('-------------------------------------')
                for each in address_book['addresses']:
                    print('Label: {0}'.format(base64.b64decode(each['label'])))
                    print('Address: {0}'.format(each['address']))
                    print('-------------------------------------')
            else:
                print('No addresses found in address book.')
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t access address book due to an API connection issue')

    def add_address_book(self, address, label):
        try:
            response = self.api.addAddressBookEntry(address, base64.b64encode(label))
            if 'API Error' in response:
                return self.get_api_error_code(response)
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t add to address book due to an API connection issue')

    def get_api_error_code(self, response):
        if 'API Error' in response:
            # If we have an API error, return the number by getting
            # after the second space and removing the trailing colon
            return int(response.split()[2][:-1])

    def mark_message_read(self, message_id):
        try:
            response = self.api.getInboxMessageByID(message_id, True)
            if 'API Error' in response:
                return self.get_api_error_code(response)
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t mark message as read due to an API connection issue')

    def mark_message_unread(self, message_id):
        try:
            response = self.api.getInboxMessageByID(message_id, False)
            if 'API Error' in response:
               return self.get_api_error_code(response)
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t mark message as unread due to an API connection issue')

    def mark_all_messages_read(self):
        try:
            inbox_messages = json.loads(self.api.getAllInboxMessages())['inboxMessages']
            for message in inbox_messages:
                if not message['read']:
                    mark_message_read(message['msgid'])
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t mark all messages read due to an API connection issue')

    def mark_all_messages_unread(self):
        try:
            inbox_messages = json.loads(self.api.getAllInboxMessages())['inboxMessages']
            for message in inbox_messages:
                if message['read']:
                    mark_message_unread(message['msgid'])
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t mark all messages unread due to an API connection issue')

    def delete_inbox_messages(self):
        try:
            inbox_messages = json.loads(self.api.getAllInboxMessages())
            total_messages = len(inbox_messages['inboxMessages'])
            while True:
                message_number = self.user_input('Enter the number of the message you wish to delete or (A)ll to empty the inbox.').lower()
                try:
                    if message_number in ['all', 'a'] or int(message_number) == total_messages:
                        break
                    elif int(message_number) >= total_messages:
                        print('Invalid Message Number')
                    elif int(message_number) <= numMessages:
                        break
                    else:
                        print('Invalid input')
                except ValueError:
                    print('Invalid input')
            # Prevent accidental deletion
            delete_verify = self.user_input('Are you sure, (Y)/(n)').lower()
            if delete_verify in ['yes', 'y']:
                if message_number in ['all', 'a'] or int(message_number) == total_messages:
                    # Processes all of the messages in the inbox
                    for message_number in range (0, total_messages):
                        print('Deleting message {0} of {1}'.format(message_number+1, total_messages))
                        self.delete_message(0)
                    print('Inbox is empty.')
                else:
                    # No need for a try/except since it was already verified up above!
                    self.delete_message(int(message_number))
                print('Notice: Message numbers may have changed.')
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t delete inbox message(s) due to an API connection issue')

    def add_info(self):
        try:
            while True:
                address = self.user_input('Enter the Bitmessage Address:')
                address_information = json.loads(str(self.api.decodeAddress(address)))
                if address_information['status'] == 'success':
                    print('Address Version: {0}'.format(address_information['addressVersion']))
                    print('Stream Number: {0}'.format(address_information['streamNumber']))
                    break
                else:
                    print('Invalid address!')
        except AttributeError:
            print('Invalid address!')
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t display address information due to an API connection issue')

    def send_something(self):
        while True:
            send_which = self.user_input('Would you like to send a (M)essage or (B)roadcast?').lower()
            if send_which in ['message', 'm', 'broadcast', 'b']:
                break
            else:
                print('Invald input')
        if send_which in ['message', 'm']:
            self.send_message('','','','')
        elif send_which in ['broadcast', 'b']:
            self.send_broadcast('','','')

    def read_something(self):
        while True:
            read_which = self.user_input('Would you like to read a message from the (I)nbox or (O)utbox?').lower()
            if read_which in ['inbox', 'outbox', 'i', 'o']:
                break
            else:
                print('Invalid input')
        try:
            message_number = int(self.user_input('What is the number of the message you wish to open?'))
        except ValueError:
            print("That's not a whole number")
        if read_which in ['inbox', 'i']:
            print('Loading...')
            message_id = self.read_message(message_number)
            verify_unread = self.user_input('Would you like to keep this message unread, (Y)/(n)').lower()
            if verify_unread not in ['yes', 'y']:
                self.mark_message_read(message_id)
            while True:
                do_which = self.user_input('Would you like to (D)elete, (F)orward or (R)eply?').lower()
                if do_which in ['reply','r','forward','f','delete','d','forward','f','reply','r']:
                    break
                else:
                    print('Invalid input')
            if do_which in ['reply', 'r']:
                print('Loading...')
                self.reply_message(message_number,'reply')
            elif do_which in ['forward', 'f']:
                print('Loading...')
                self.reply_message(message_number,'forward')
            elif do_which in ['delete', 'd']:
                # Prevent accidental deletion
                verify_delete = self.user_input('Are you sure, (Y)/(n)').lower()
                if verify_delete in ['yes', 'y']:
                    self.delete_message(message_number)
                    print('Message Deleted.')
        elif read_which in ['outbox', 'o']:
            self.read_sent_message(message_number)
            # Gives the user the option to delete the message
            delete_this = self.user_input('Would you like to Delete this message, (Y)/(n)').lower()
            if delete_this in ['yes', 'y']:
                # Prevent accidental deletion
                verify_delete = self.user_input('Are you sure, (Y)/(n)').lower()
                if verify_delete in ['yes', 'y']:
                    self.delete_sent_message(message_number)
                    print('Message Deleted.')

    def save_message(self):
        while True:
            which_box = self.user_input('Would you like to read a message from the (I)nbox or (O)utbox?').lower()
            if which_box in ['inbox', 'outbox', 'i', 'o']:
                break
        try:
            message_number = int(self.user_input('What is the number of the message you wish to open?'))
        except ValueError:
            print("That's not a whole number")
        if which_box in ['inbox', 'i']:
            print('Loading...')
            message_id = self.read_message(message_number)
            keep_unread = self.user_input('Would you like to keep this message unread, (Y)/(n)').lower()
            if keep_unread not in ['yes', 'y']:
                self.mark_message_read(message_id)
            while True:
                message_options = self.user_input('Would you like to (D)elete, (F)orward or (R)eply?').lower()
                if message_options in ['reply','r','forward','f','delete','d','forward','f','reply','r']:
                    break
                else:
                    print('Invalid input')
            if message_options in ['reply', 'r']:
                print('Loading...')
                self.reply_message(message_number,'reply')
            elif message_options in ['forward', 'f']:
                print('Loading...')
                self.reply_message(message_number,'forward')
            elif message_options in ['delete', 'd']:
                # Prevent accidental deletion
                verify_delete = self.user_input('Are you sure, (Y)/(n)').lower()
                if verify_delete in ['yes', 'y']:
                    self.delete_message(message_number)
                    print('Message Deleted.')
        elif which_box in ['outbox', 'o']:
            self.read_sent_message(message_number)
            # Gives the user the option to delete the message
            delete_message = self.user_input('Would you like to Delete this message, (Y)/(n)').lower()
            if delete_message in ['yes', 'y']:
                # Prevent accidental deletion
                verify_delete = self.user_input('Are you sure, (Y)/(n)').lower()
                if verify_delete in ['yes', 'y']:
                    self.delete_sent_message(message_number)
                    print('Message Deleted.')

    def delete_message(self):
        try:
            which_box = self.user_input('Would you like to delete a message from the (I)nbox or (O)utbox?').lower()

            if which_box in ['inbox', 'i']:
                self.delete_inbox_messages()
            elif which_box in ['outbox', 'o']:
                outbox_messages = json.loads(self.api.getAllSentMessages())
                total_messages = len(outbox_messages['sentMessages'])

                while True:
                    message_number = self.user_input('Enter the number of the message you wish to delete or (A)ll to empty the outbox.').lower()
                    try:
                        if message_number in ['all', 'a'] or int(message_number) == total_messages:
                            break
                        elif int(message_number) >= total_messages:
                            break
                        else:
                            print('Invalid input')
                    except ValueError:
                        print('Invalid input')
                # Prevent accidental deletion
                verify_deletion = self.user_input('Are you sure, (Y)/(n)').lower()
                if verify_deletion in ['yes', 'y']:
                    if message_number in ['all', 'a'] or int(message_number) == total_messages:
                        # processes all of the messages in the outbox
                        for message_number in range (0, total_messages):
                            print('Deleting message {0} of {1}'.format(message_number+1, total_messages))
                            self.delete_sent_message(0)
                        print('Outbox is empty.')
                    else:
                        self.delete_sent_message(int(message_number))
                    print('Notice: Message numbers may have changed.')
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t access outbox due to an API connection issue')

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

    def add_adress_book(self):
        while True:
            address = self.user_input('Enter address')
            if self.valid_address(address):
                label = self.user_input('Enter label')
                if label:
                    break
                else:
                    print('You need to put a label')
            else:
                print('Invalid address')
        res = self.add_address_book(address, label)
        if res == 16:
            print('Error: Address already exists in Address Book.')

    def delete_address_book(self):
        while True:
            address = self.user_input('Enter address')
            if self.valid_address(address):
                res = self.delete_address_book2(address)
                if res in 'Deleted address book entry':
                     print('{0} has been deleted!'.format(address))
            else:
                print('Invalid address')

    def delete_address_book2(self, address):
        try:
            response = self.api.deleteAddressBookEntry(address)
            if 'API Error' in response:
                return self.get_api_error_code(response)
            else:
                return response
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t delete from address book due to an API connection issue')

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
            print('\nYou have {0} unread message(s)'.format(unread_messages))
        else:
            return

    def generate_deterministic(self):
        deterministic = True
        label = self.user_input('Label the new address:')
        passphrase = self.user_input('Enter the Passphrase.')

        while True:
            try:
                number_of_addresses = int(self.user_input('How many addresses would you like to generate?'))
            except ValueError:
                print("That's not a whole number.")
            else:
                if number_of_addresses <= 0:
                    print('How were you expecting that to work?')
                elif number_of_addresses >= 1000:
                    print('Limit of 999 addresses generated at once.')
                else:
                    break
        address_version = 3
        # TODO - I hate that this is hardcoded..
        stream_number = 1
        is_ripe = self.user_input('Shorten the address, (Y)/(n)').lower()
        print('Generating, please wait...')

        if is_ripe in ['yes', 'y']:
            ripe = True
        else:
            ripe = False
        # TODO - Catch the error that happens when deterministic is not True/False
        generated_address = self.generate_address(label,deterministic,passphrase,number_of_addresses,address_version,stream_number,ripe)
        json_addresses = json.loads(generated_address)

        if number_of_addresses >= 2:
            print('Addresses generated: ')
        elif number_of_addresses == 1:
            print('Address generated: ')
        for each in json_addresses['addresses']:
            print(each)

    def generate_random(self):
        deterministic = False
        label = self.user_input('Enter the label for the new address.')
        generated_address = self.generate_address(label,deterministic,'', '', '', '', '')
        if generated_address:
            print('Generated Address: {0}'.format(generated_address))
        else:
            # TODO - Have a more obvious error message here
            print('An error has occured')

    def generate_an_address(self):
        while True:
            type_of_address = self.user_input('Would you like to create a (D)eterministic or (R)andom address?').lower()
            if type_of_address in ['deterministic', 'd', 'random', 'r']:
                break
            else:
                print('Invalid input')
        # Creates a deterministic address
        if type_of_address in ['deterministic', 'd']:
            self.generate_deterministic()
        # Creates a random address with user-defined label
        elif type_of_address in ['random', 'r']:
            self.generate_random()

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
        try:
            if self.enable_bm.poll() is None:
                self.bm_active = True
            else:
                self.bm_active = False
                self.run_bitmessage()
        except AttributeError:
            self.bm_active = False
            self.run_bitmessage()

        if not self.bm_api_import:
            self.api = xmlrpclib.ServerProxy(self.return_api())

        if not self.api_check():
            self.bm_api_import = False
        else:
            if not self.bm_api_import:
                self.bm_api_import = True

if __name__ == "__main__":
    print('The API should never be called directly.')
    sys.exit(0)
