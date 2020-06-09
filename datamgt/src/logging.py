import logging

from django.http import HttpRequest
from django.contrib import messages

def mylog(response, msg):
	messages.success(response, msg)
	logging.info(msg)
