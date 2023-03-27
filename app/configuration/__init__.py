from app.internal.services import Services
from app.pkg.connectors import Connectors
from app.pkg.models.core import Container, Containers

from .server import Server

__all__ = ["__containers__"]

__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Connectors),
        Container(container=Services),
    ],
)