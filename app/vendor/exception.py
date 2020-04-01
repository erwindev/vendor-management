class ApplicationException(Exception):

    def __init__(self, arg):
        self.msg = arg
