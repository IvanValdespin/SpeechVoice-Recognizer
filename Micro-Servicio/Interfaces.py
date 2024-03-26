from abc import abstractclassmethod

#Iterfaz for generate folders
class IFolder():
    @abstractclassmethod
    def create_folder()->None:
        """Interface Method"""
#Interfaz for generate Filters 
class IFilter():
    @abstractclassmethod
    def create_filter()->None:
        """Interface Method"""
#Iterfaz for creating patterns in spanish or english
class IPatterns():
#@abstractclassmethod
#def chargeSentences():
# Interfaz chargeSentence Method
    @abstractclassmethod
    def createPatterns():
        """Interfaz createPattern Method"""

    @abstractclassmethod
    def chargePatterns():
        """Interfaz chargePattern Method"""