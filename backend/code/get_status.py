from distutils.log import error, fatal
from flask import Response

class GetStatus:
    def __init__(self):
        self.msg = ''
        self.error = ''
        self.fatal = False
        self.status_code = None

    def get_status(self, message):
        '''
        this method is for sending to user data about the status of the login 
        or of the converting process
        '''
        self.msg = ''
        self.msg = message
        return message
    
    def error_msg(self, errormsg, isFatal):
        '''
        this method is to raise errors UI on the client-side
        '''
        self.error = errormsg
        self.fatal = isFatal
        return {"error_msg": errormsg, "fatal":isFatal}

    def login_status(self, message, status_code):
        self.msg = message
        self.status_code = status_code
        return Response(message, status=status_code)

    def clear(self):
        return GetStatus()
    