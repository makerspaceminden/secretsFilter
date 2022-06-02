import os

class KeyFilter:

    # Variables
    mapping = {}
    scanDirPath: str
    preDelimiter: str
    postDelimiter: str
    isVerbose: bool
    doReverse: bool

    def __init__(self, keyObject, scanDirPath: str, preDelimiter: str = "{", postDelimiter: str = "}", verbosity: bool = False, doReverse: bool = False):
        """Initializes a KeyFilter object
        keyObject{dict}:    Dictionary of name-->secret mappings. Example: {"key1":"TopSecret", "key2":"123456"},
        scanDirPath{str}:   Path to the directory where the scan should be performed. overwrites files in there, so write rights are required.
        preDelimiter{str}:  Delimiter used in replacing the secret keys. Prepended before the name.
        postDelimiter{str}: Delimiter used in replacing the secret keys. Appended after the name.
            Example: preDelimiter={, postDelimiter=} => "TopSecret" -> "{key1}" """

        self.mapping = keyObject
        self.scanDirPath = scanDirPath
        self.preDelimiter = preDelimiter
        self.postDelimiter = postDelimiter
        self.isVerbose = verbosity
        self.doReverse = doReverse

    def doScan(self):
        for dirName, subdirList, fileList in os.walk(self.scanDirPath):
            if(self.isVerbose):
                print("Filtering dir \""+dirName+"\": ")

            for fileName in fileList:
                if(self.isVerbose):
                    print("\tFiltering file \""+os.path.join(dirName, fileName)+"\"")

                self._ScanFile(os.path.join(dirName, fileName))

    def _ScanFile(self, fileName:str):
        fileContent: str
        with open(fileName, "r") as f:
            fileContent = f.read()

        # do the replacing
        if(self.doReverse):
            fileContent = self._ReplaceNames(fileContent)
        else:
            fileContent = self._ReplaceSecrets(fileContent)

        with open(fileName, "w") as f:
            f.write(fileContent)

    def _ReplaceSecrets(self, content:str) -> str:
        retVal = content
        for name, secretValue in self.mapping.items():
            retVal = retVal.replace(secretValue, self._GetDelimitedString(name))

        return retVal

    
    def _ReplaceNames(self, content:str) -> str:
        retVal = content
        for name, secretValue in self.mapping.items():
            retVal = retVal.replace(self._GetDelimitedString(name), secretValue)

        return retVal


    def _GetDelimitedString(self, inValue:str) -> str:
        return self.preDelimiter + inValue + self.postDelimiter