from app.users import models


def create_user(**kwargs) -> models.User:
    return models.User.objects.create_user(**kwargs)


def update_user() -> models.User:
    pass


''
