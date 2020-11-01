

class TopicService:
    def __init__(self, name: str, classType):
        self.__name = name
        self.__classType = classType
        self.__data = None

    def setData(self, data):
        self.__data = data
        print("sett:", data)

    def getData(self):
        return self.__data

    def getType(self):
        return self.__classType

    def getName(self):
        return self.__name