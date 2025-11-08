import backend

@backend.table
class Accounts(backend.Table):
    def __init__(self) -> None:
        super().__init__()
        print(self._rows)

@backend.table
class Profiles(backend.Table):
    def __init__(self) -> None:
        pass

@backend.table
class Dashboard(backend.Table):
    def __init__(self) -> None:
        pass

@backend.table
class Logs(backend.Table):
    def __init__(self) -> None:
        pass
