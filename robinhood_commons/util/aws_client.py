from __future__ import annotations

from typing import Dict

import boto3
import base64
from boto3.session import Session
from botocore.exceptions import ClientError

from util.constants import USERS_KEY

REGION_NAME: str = 'us-west-2'


class AwsClient:

    @classmethod
    def _open_boto_session(cls) -> Session:
        return boto3.session.Session()

    @classmethod
    def create_boto_client(cls, name: str = 'secretsmanager', region_name: str = REGION_NAME):
        return AwsClient._open_boto_session().client(service_name=name, region_name=region_name)

    @classmethod
    def get_secret(cls, client, secret_name: str) -> Dict[str, str]:

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            print(e)
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                raise e
        else:
            secret = get_secret_value_response['SecretString'] if 'SecretString' in get_secret_value_response else \
                base64.b64decode(get_secret_value_response['SecretBinary'])

        return eval(secret)


if __name__ == '__main__':
    print(AwsClient.get_secret(client=AwsClient.create_boto_client(), secret_name=USERS_KEY))
