from distutils.log import error, fatal


class GetStatus:
    def __init__(self):
        self.msg = ''
        self.error = ''
        self.fatal = False

    def get_status(self, action):
        self.msg = action
        return action
    
    def error_msg(self, errormsg, isFatal):
        self.error = errormsg
        self.fatal = isFatal
        return {"error_msg": errormsg, "fatal":isFatal}
    