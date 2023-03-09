from dependency_injector import containers, providers

# from .emails import Email
# from .funds import Fund
# from .funds_users import FundsUsers
from .users import User

# from .static import StaticUser


# __all__ = ["Repository", "Email"]

__all__ = ["Repository"]


class Repository(containers.DeclarativeContainer):
    users = providers.Factory(User)
    # email = providers.Factory(Email)
    # static_user = providers.Factory(StaticUser)
