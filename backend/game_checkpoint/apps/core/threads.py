
from threading import Thread
from django.core.mail import get_connection, EmailMessage
from django.utils import timezone
from game_checkpoint.apps.users.models import User
from django.db.models import F, ExpressionWrapper, DateTimeField
from django.conf import settings
import time
import os
import datetime

queued_messages = []

def queue_message(msg):
    queued_messages.append(EmailMessage(*msg))

def _send_queued_message():
    if len(queued_messages) == 0:
        return

    msgs = queued_messages[:5]
    try: 
        mailer = get_connection()
        mailer.open()
        mailer.send_messages(msgs)
        mailer.close()
        del queued_messages[:5]
    except:
        pass

thread_list = [
    (_send_queued_message, 1),
]

def _new_thread(function, delay):
    while True:
        time.sleep(delay)
        function()

def start_threads():
    if os.getpid() == 1:
        print('skipping thread creation on watcher process')
        return
    for x in thread_list:
        try:
            t= Thread( target = _new_thread, args=x)
            t.daemon = True
            t.start()
        except:
            print("Error: unable to start thread")