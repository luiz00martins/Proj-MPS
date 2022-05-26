import Users, Institute, Turma

class Management():
    def __init__(self, conn):
        self.__conn = conn
        self.user_repo = Users.UserRepository(self.__conn)
        self.user_validation = Users.UserDefaultValidation()
        self.turma_repo = Turma.TurmaRepository(self.__conn)
        self.institute_repo = Institute.InsituteRepository(self.__conn)

    def add_user(self, user: Users.User):
        self.user_repo.add_user(user, self.user_validation)

    def get_user(self, user_id: int):
        self.user_repo.get_user_by_id(user_id)

    def remove_user(self, user_id: int):
        self.user_repo.remove_user_by_id(user_id)

    def add_turma(self, turma: Turma.Turma):
        self.turma_repo.add_turma(turma)

    def add_institute(self, institute: Institute.Institute):
        self.institute_repo.add_institute(institute)




