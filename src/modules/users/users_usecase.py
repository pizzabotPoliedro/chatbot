from src.modules.users.users_repository import UsersRepository

class UsersUseCase:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def create(self, data: dict):
        try:
            pass
        except:
            pass