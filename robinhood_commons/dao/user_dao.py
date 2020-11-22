from __future__ import annotations

from typing import Dict, List

from robinhood_commons.entity.printable import Printable
from robinhood_commons.entity.user import User
from robinhood_commons.util.constants import USERS_KEY
from robinhood_commons.util.aws_client import AwsClient


KEY_MFA_CODE: str = 'mfa_code'


class UserDao(Printable):

    @staticmethod
    def get_users() -> List[User]:
        secret_client = AwsClient.create_boto_client()

        user_names: List[str] = UserDao.get_usernames(secret_client=secret_client)

        return [User(**AwsClient.get_secret(client=secret_client, secret_name=user_name)) for user_name in user_names]

    @staticmethod
    def get_users_by_email() -> Dict[str, User]:
        return {u.email: u for u in UserDao.get_users()}

    @staticmethod
    def get_user_by_email(email: str) -> User:
        return UserDao.get_users_by_email()[email]

    @staticmethod
    def get_usernames(secret_client) -> List[str]:
        return AwsClient.get_secret(client=secret_client, secret_name=USERS_KEY)[USERS_KEY].split(':')

    @staticmethod
    def to_user(user_info: Dict[str, str]) -> User:
        if KEY_MFA_CODE not in user_info:
            user_info[KEY_MFA_CODE] = None

        return User(**user_info)


def main() -> None:
    user_dao = UserDao()
    print(user_dao.get_users())


if __name__ == '__main__':
    main()
