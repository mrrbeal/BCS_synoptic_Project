import os,sys

def DEBUG(text):
    if DEBUGON == True:
        print(text)



DEBUGON = True


class ImageFile:
    def __init__(self) -> None:
        if getattr(sys, 'frozen', False):
            dname = os.path.dirname(sys.executable)
        elif __file__:
            dname = os.path.dirname(__file__)

        self.image_path = rf'{dname}\no_image.png'
        self.image_name = os.path.split(self.image_path)[1].split(".")[0]

    def setImage(self,filePath):
            self.image_path = filePath
            self.image_name = os.path.split(filePath)[1].split(".")[0]

class CategoryList:
    def __init__(self) -> None:
        self.categories = []

    def getSize(self):
        DEBUG(f"GETSIZE: {len(self.categories)}")
        return len(self.categories)

    def createCategory(self,name):
        self.categories.append(name)

    def removeCategory(self,categoryName):
        self.categories.remove(categoryName)

class MediaFile(ImageFile):
    def __init__(self,filePath) -> None:
        ImageFile.__init__(self)
        self.file_path = filePath
        self.file_name = os.path.split(filePath)[1].split(".")[0]
        self.file_type = os.path.splitext(filePath)[1][1:]
        self.file_comment = ""
        self.categories = []

class MediaLibrary:
    def __init__(self) -> None:
        self.files = {}
        if self.getSize() == 0:
            self.keyCount = 1
        else:
            self.keyCount =  max(self.files.keys()) + 1
    def getSize(self):
        DEBUG(f"GETSIZE: {len(self.files)}")
        return len(self.files)
    def add_file(self,filePath):
        self.files[self.keyCount] = (MediaFile(filePath))
        self.keyCount +=1

    def add_folder(self,folderDir,fileTypes) -> list:
        for subdir, dir, files in os.walk(folderDir):
            for file in files:
                file_path = subdir + os.sep + file
                file_type = os.path.splitext(file)[1][1:]
                if file_type in fileTypes:
                    self.files[self.keyCount] = (MediaFile(file_path))
                    self.keyCount +=1

    def removeFile(self,fileid,filename,filetype):
        DEBUG(f"GETSIZE BEFORE REMOVE: {len(self.files)}")
        for key, value in self.files.items():
            if value.file_name == filename and value.file_type == filetype and key == fileid:
                del self.files[key]
                DEBUG(f"GETSIZE AFTER REMOVE: {len(self.files)}")
                break
    
    def get_file(self,dictKey):
        return self.files.get(dictKey)
    def exportLibrary():
        pass
    def importLibrary(json):
        pass

class PlaylistLibrary:
    def __init__(self) -> None:
        self.playlists = {}
        self.playlists["test"] = [(1,"A"),(2,"e"),(3,"w"),(4,"d"),(5,"b")]

    def getSize(self):
        DEBUG(f"GETSIZE: {len(self.playlists)}")
        return len(self.playlists)
    
    def add_playlist(self,name):
        self.playlists[name] =[]
    def delete_playlist(self):
        pass
    def rename_playlist(self,newkey,oldkey):
        if newkey!=oldkey:  
            self.playlists[newkey] = self.playlists[oldkey]
            del self.playlists[oldkey]
    
    def delete_file_from_playist(self,name,index):
        for i in self.playlists[name]:
            print(self.playlists[name])
            if i[0] == index:
                print(i[0])
                self.playlists[name].pop(self.playlists[name].index(i))
        