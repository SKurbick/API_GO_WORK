"""Global point for collected routes."""

from app.internal.pkg.models import Routes
from app.internal.routes import (
    # auth,
    # email,
    # funds,
    # funds_users,
    # static,
    users,
)

__all__ = ["__routes__"]

__routes__ = Routes(
    routers=(
        # auth.router,
        users.router,
        # funds.router,
        # email.router,
        # funds_users.router,
        # static.router,
    ),
)
