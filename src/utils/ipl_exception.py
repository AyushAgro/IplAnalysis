# Some Common Exceptions which can occur during execution of code
# we assign code to each code, so we can also print code in log file and
# then check what that code means something like how sql show it error

# if any match has more than 2 teams

class IplException(Exception):
    def __init__(self):
        pass

# Different Team 
class DifferentTeam(IplException):
    def __init__(self):
        self.code = 1
        self.message = "Team used with the Same Match Id is different"

# if any Innings exceed 20 over.
class TooManyBall(IplException):
    def __init__(self):
        self.code = 2
        self.message = "An Single Inning Cannot have more than 20 over"

# when format is wrong
class InvalidFormat(IplException):
    def __init__(self):
        self.code = 3
        self.message = (
            "Given Data is not correctly Format, Please Check your data before Passing"
        )

# if file we are looking is not found
class FileNotFound(IplException):
    def __init__(self):
        self.code = 4
        self.message = "File Not Found.. Please Try Again"

# when file doesn't have valid extension
class InvalidFile(IplException):

    def __init__(self, file = None, fileType = None):
        self.code = 5
        if file :
            self.message = (
                f"File Type of {file} not allowed.\nAllowed FileType as {fileType}"
            )

# Table is empty
class TableEmpty(IplException):
    def __init__(self):
        self.code = 6
        self.message = "Given Table is Empty"

# Required columns is not found
class ColumnsNotFound(IplException):
    def __init__(self, column = []):
        self.code = 7
        self.message = f"Given Columns not found {column}, Please add it"

# Direcotry Not Found
class DirectoryNotFound(IplException):
    def __init__(self, dir_ = None):
        self.code = 8
        self.message = f"{dir_} not found"

# Teams has player count more than 11
class MaximumPlayer(IplException):
    def __init__(self, name):
        self.code = 9
        self.message = f"Any Single Team can have maximum of 11 player playing"
