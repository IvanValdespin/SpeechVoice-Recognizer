import sys
import os
from Interfaces import IFolder


class Folder(IFolder):
    def __init__(self,name) -> None:
        self.__FOLDER = name

    def create_folder(self) -> None:
        if not os.path.exists(self.__FOLDER):
            os.mkdir(os.path.join(self.__FOLDER))
        else:
            pass


class UserFolder(IFolder):

    def __init__(self) -> None:
        self.__AUDIO_FOLDER = "audio"
        self.audio_folder = Folder(self.__AUDIO_FOLDER)
        self.__USER = 1
        self.__userpath = "user"+str(self.__USER)
        self.__USER_FOLDER = os.path.join(self.__AUDIO_FOLDER,self.__userpath)



    def create_folder(self)->__name__:

        self.audio_folder.create_folder();

        while  os.path.exists(self.__USER_FOLDER) == True:
            self.__USER += 1
            self.__userpath = "user"+str(self.__USER)
            self.__USER_FOLDER = os.path.join(self.__AUDIO_FOLDER,self.__userpath)
        
        os.mkdir(self.__USER_FOLDER)
        return self.__USER_FOLDER


class RespositoryFactory():
    @staticmethod
    def build_repository(folder_type):
        if folder_type != "user":
            return Folder(folder_type).create_folder()
        else:
            return UserFolder().create_folder()
        