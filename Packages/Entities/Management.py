import Users
import Institute
import Classroom


class ManagementMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Management(metaclass=ManagementMeta):

    # Setup should be called once
    def setup(self, conn):
        if self.__conn is None:
            return

        self.__conn = conn
        self.user_repo = Users.UserRepository(self.__conn)
        self.user_validation = Users.UserDefaultValidation()
        self.classroom_repo = Classroom.ClassroomRepository(self.__conn)
        self.institute_repo = Institute.InsituteRepository(self.__conn)

    def __init__(self):
        self.classroom_repo = None
        self.__conn = None
        self.user_repo = None
        self.user_validation = None
        self.classroom_repo = None
        self.institute_repo = None

    def add_user(self, user: Users.User):
        self.user_repo.add_user(user, self.user_validation)

    def get_user(self, user_id: int):
        self.user_repo.get_user_by_id(user_id)

    def remove_user(self, user_id: int):
        self.user_repo.remove_user_by_id(user_id)

    def add_classroom(self, classroom: Classroom.Classroom):
        self.classroom_repo.add_turma(classroom)

    def add_institute(self, institute: Institute.Institute):
        self.institute_repo.add_institute(institute)