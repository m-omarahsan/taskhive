#!/usr/bin/env python3
# Derivitation of the Bitmessage CLI originally created by Adam Melton (Dokument)
# Modified by Scott King (Lvl4Sword)
# Modified for use in the Taskhive project (taskhive.io)
# Distributed under the MIT/X11 software license
# See http://www.opensource.org/licenses/mit-license.php
# https://bitmessage.org/wiki/API_Reference for API documentation

import base64
import configparser
import json
import os
import sys

APPNAME = 'Taskhive'


# Failure codes
# 0 - Quitting voluntarily
# 1 - Configuration information is missing
# 2 - Can't connect to API
# 3 - Can't find bitmessagemain.py
class RaiseFailure(Exception):
    def __init__(self, code, message):
        self.failure_message = message
        self.failure_code = code    


class PassThrough(object):
    def __init__(self, **kwargs):
        self.running = True

    def Clean(self, _print=print):
        while True:
            try:
                value = self.convert(raw_value, **self.convert_kwargs)
            except ConversionFailed as e:
                return e.failure_message
            else:
                return value


class Bitmessage(object):
    #def verify_bitmessage():
    #def run_bitmessage():

    def kill_bitmessage(self, error_number, reason):
        try:
            self.api.shutdown()
        except(AttributeError, OSError, socket.error):
            sys.exit(1)
        else:
            sys.exit(0)

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

    # With no arguments sent, send_message fills in the blanks
    # subject and message must be encoded before they are passed
    def send_message(self, to_address, from_address, subject, message):
        # TODO - Was using .encode('UTF-8'), not needed?
        json_addresses = json.loads(self.api.listAddresses())
        # Number of addresses
        number_of_addresses = len(json_addresses['addresses'])

        if not self.valid_address(to_address):
            return 'invalid to address'

        if not self.valid_address(from_address):
            return 'invalid from address'
        else:
            if from_address not in number_of_addresses:
                return 'unsendable address'

        subject = base64.b64encode(subject)
        message = base64.b64encode(message)
        ack_data = self.api.sendMessage(to_address, from_address, subject, message)
        sending_message = self.api.getStatus(ack_data)
        return sending_message

    def send_broadcast(self, from_address, subject, message):
            if subject == '':
                    subject = self.user_input('Enter your Subject.')
                    subject = base64.b64encode(subject)
            if message == '':
                    message = self.user_input('Enter your Message.')

            add_attachment = self.user_input('Would you like to add an attachment, (Y)/(n)').lower()
            if add_attachment in ['yes', 'y']:
                message = message + '\n\n' + self.attachment()
            message = base64.b64encode(message)

            ack_data = self.api.sendBroadcast(from_address, subject, message)
            sending_message = self.api.getStatus(ack_data)
            # TODO - There are more statuses that should be paid attention to
            if sending_message == 'broadcastqueued':
                print('Broadcast is now in the queue')
            else:
                print(sending_message)
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t send message due to an API connection issue')


    # Lists the messages by: Message Number, To Address Label,
    # From Address Label, Subject, Received Time
    def inbox(self, unread_only):
        try:
            inbox_messages = json.loads(self.api.getAllInboxMessages())
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t access inbox due to an API connection issue')
        else:        
            total_messages = len(inbox_messages['inboxMessages'])
            messages_printed = 0
            messages_unread = 0
            # processes all of the messages in the inbox
            for each in range (0, total_messages):
                message = inbox_messages['inboxMessages'][each]
                # if we are displaying all messages or
                # if this message is unread then display it
                if not unread_only or not message['read']:
                    print('-----------------------------------')
                    # Message Number
                    print('Message Number: {0}'.format(each))
                    # Get the to address
                    print('To: {0}'.format(message['toAddress']))
                    # Get the from address
                    print('From: {0}'.format(message['fromAddress']))
                    # Get the subject
                    print('Subject: {0}'.format(base64.b64decode(message['subject'])))
                    print('Received: {0}'.format(datetime.datetime.fromtimestamp(float(message['receivedTime'])).strftime('%Y-%m-%d %H:%M:%S')))
                    messages_printed += 1
                    if not message['read']:
                        messages_unread += 1
            print('-----------------------------------')
            print('There are {0:d} unread messages of {1:d} in the inbox.'.format(messages_unread, total_messages))
            print('-----------------------------------')


    def outbox(self):
        try:
            outbox_messages = json.loads(self.api.getAllSentMessages())
            json_outbox = outbox_messages['sentMessages']
            total_messages = len(json_outbox)
            # processes all of the messages in the outbox
            for each in range(0, total_messages):
                print('-----------------------------------')
                # Message Number
                print('Message Number: {0}'.format(each))
                # Get the to address
                print('To: {0}'.format(json_outbox[each]['toAddress']))
                # Get the from address
                print('From: {0}'.format(json_outbox[each]['fromAddress']))
                # Get the subject
                print('Subject: {0}'.format(base64.b64decode(json_outbox[each]['subject'])))
                # Get the subject
                print('Status: {0}'.format(json_outbox[each]['status']))
                last_action_time = datetime.datetime.fromtimestamp(float(json_outbox[each]['lastActionTime']))
                print('Last Action Time: {0}'.format(last_action_time.strftime('%Y-%m-%d %H:%M:%S')))
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t access outbox due to an API connection issue')
        else:
            print('-----------------------------------')
            print('There are {0} messages in the outbox.'.format(total_messages))
            print('-----------------------------------')


    # Opens a sent message for reading
    def read_sent_message(self, message_number):
        try:
            outbox_messages = json.loads(self.api.getAllSentMessages())
            total_messages = len(outbox_messages['sentMessages'])
            if message_number >= total_messages:
                print('Invalid Message Number')
                self.main()

            message = base64.b64decode(outbox_messages['sentMessages'][message_number]['message'])
            self.detect_attachment(message)

            # Get the to address
            print('To: {0}'.format(outbox_messages['sentMessages'][message_number]['toAddress']))
            # Get the from address
            print('From: {0}'.format(outbox_messages['sentMessages'][message_number]['fromAddress']))
            # Get the subject
            print('Subject: {0}'.format(base64.b64decode(outbox_messages['sentMessages'][message_number]['subject'])))
            #Get the status
            print('Status: {0}'.format(outbox_messages['sentMessages'][message_number]['status']))
            last_action_time = datetime.datetime.fromtimestamp(float(outbox_messages['sentMessages'][message_number]['lastActionTime']))
            print('Last Action Time: {0}'.format(last_action_time.strftime('%Y-%m-%d %H:%M:%S')))
            print('Message: {0}'.format(message))
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t access outbox due to an API connection issue')


    # Opens a message for reading
    def read_message(self, message_number):
        try:
            inbox_messages = json.loads(self.api.getAllInboxMessages())
            total_messages = len(inbox_messages['inboxMessages'])
            if message_number >= total_messages:
                print('Invalid Message Number.')
                self.main()

            message = base64.b64decode(inbox_messages['inboxMessages'][message_number]['message'])
            self.detect_attachment(message)

            # Get the to address
            print('To: {0}'.format(inbox_messages['inboxMessages'][message_number]['toAddress']))
            # Get the from address
            print('From: {0}'.format(inbox_messages['inboxMessages'][message_number]['fromAddress']))
            # Get the subject
            print('Subject: {0}'.format(base64.b64decode(inbox_messages['inboxMessages'][message_number]['subject'])))

            received_time = datetime.datetime.fromtimestamp(float(inbox_messages['inboxMessages'][message_number]['receivedTime']))
            print('Received: {0}'.format(received_time.strftime('%Y-%m-%d %H:%M:%S')))
            print('Message: {0}'.format(message))
            return inbox_messages['inboxMessages'][message_number]['msgid']
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t access inbox due to an API connection issue')


    # Allows you to reply to the message you are currently on.
    # Saves typing in the addresses and subject.
    def reply_message(message_number, forward_or_reply):
        try:
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

            add_attachment = self.user_input('Would you like to add an attachment, (Y)/(n)').lower()
            if add_attachment in ['yes', 'y']:
                new_message = new_message + '\n\n' + self.attachment()
            new_message = new_message + '\n\n' + '-' * 55 + '\n'
            new_message = new_message + message
            new_message = base64.b64encode(new_message)

            self.send_message(to_address, from_address, subject, new_message)
        except socket.error:
            self.bm_api_import = False
            print('Couldn\'t send message due to an API connection issue')


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
        print("Network Status: {0}".format(connection))
        print("Number Of Network Connections: {0}".format(status['networkConnections']))
        print("Number Of Pubkeys Processed: {0}".format(status['numberOfPubkeysProcessed']))
        print("Number Of Messages Processed: {0}".format(status['numberOfMessagesProcessed']))
        print("Number Of Broadcasts Processed: {0}".format(status['numberOfBroadcastsProcessed']))


if __name__ == "__main__":
    print('The API should never be called directly.')
    sys.exit(0)
