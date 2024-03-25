class ProjectController:
    '''
        This class implements the Singleton pattern. It's responsible for exposing to all parts of the project,
        whether the project is running or terminated for any reason (ie user closed the window). \n
        This happens utilizing a public property called "projectIsTerminated"
    '''

    _instance = None

    def __new__(cls):
        if (cls._instance is None):
            # Creates the first and only instance of this class
            cls._instance = super().__new__(cls)
            cls._instance.projectIsTerminated = False

        return cls._instance
