class ConverterError(Exception):

     def __init__(self, message='Wrong file!'):
        self.message = message
        super().__init__(message)


class ApplicationError(Exception):
    """Error to handle application errors"""



