import sys, os

def setupBackend():
    '''
        The purpose of this function is to include in sys.path, all directories that are needed in order for
        all the modules and packages that are imported by brontend, to be found. 

        Note: sys.path is a list of directories, where python will look at in order to find the modules and packages you ask for
    '''

    currentWorkingDirectory: str = os.getcwd()

    relativeDirectories: list[str] = [
        "",
    ]

    for path in relativeDirectories:
        newPath: str = os.path.join(currentWorkingDirectory, path)
        
        if (not (newPath in sys.path)):
            sys.path.append(newPath)

