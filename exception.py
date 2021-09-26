class DiffrentTeam(Exception):
    def __init__(self):
        self.code = 1
        self.message = 'Team used with the Same Match Id is different'


class TooManyBall(Exception):
    def __init__(self):
        self.code = 2
        self.message = 'An Single Inning Cannot have more than 20 over'


class InvalidFormat(Exception):
    def __init__(self):
        self.code = 3
        self.message = 'Given Data is not correctly Format, Please Check your data before Passing'


class FileNotFound(Exception):
    def __init__(self):
        self.code = 4
        self.message = 'File Not Found.. Please Try Again'


class InvalidFile(Exception):
    def __init__(self, file, fileType):
        self.code = 5
        self.message = f'File Type of {file} not allowed.\nAllowed FileType as {fileType}'


class TableEmpty(Exception):
    def __init__(self):
        self.code = 6
        self.message = 'Given Table is Empty'


class ColumnsNotFound(Exception):
    def __init__(self, column):
        self.code = 7
        self.message = f"Columns not found {column}, Please add it"


class DirectoryNotFound(Exception):
    def __init__(self, dir):
        self.code = 8
        self.message = f'{dir} not found'
