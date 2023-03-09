from typing import Union

from fastapi_mail import FastMail, MessageSchema, errors
from starlette.background import BackgroundTasks
from app.pkg.settings import config_email
from app.pkg import models
from starlette import status
from app.pkg.models.exceptions import email
import secrets
import string


class SendEmail:
    async def send_email(self,
                         template_name: str,
                         contents: Union[models.EmailSchema, models.ActivateUser],
                         background_task: BackgroundTasks
                         ):
        try:
            if type(contents) is models.EmailSchema:
                template_body = {
                    'verification_url': contents.verification_url,
                    'user_email': contents.user_email
                }

            if type(contents) is models.ActivateUser:
                template_body = {
                    'verification_url': contents.verification_url,
                }

            message = MessageSchema(
                subject='Требуются действия с учетной записью Fund Incubator',
                recipients=contents.recipient,
                subtype="html",
                template_body=template_body
            )

            fm = FastMail(config_email)

            background_task.add_task(fm.send_message, message, template_name=template_name)
        except errors.ConnectionErrors:
            raise email.SendingError
        except ValueError:
            raise email.EmptyListAddresses
        except:
            raise email.Unknown
        else:
            return status.HTTP_200_OK

    @staticmethod
    async def random_string(_len: int = 24):
        return "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(_len)
        )
