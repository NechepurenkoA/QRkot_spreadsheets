import os
import asyncio

from dotenv import load_dotenv

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

load_dotenv()

INFO = {
    'type':  os.environ['TYPE'],
    'project_id':  os.environ['PROJECT_ID'],
    'private_key_id':  os.environ['PRIVATE_KEY_ID'],
    'private_key':  os.environ['PRIVATE_KEY'],
    'client_email':  os.environ['CLIENT_EMAIL'],
    'client_id':  os.environ['CLIENT_ID'],
    'auth_uri':  os.environ['AUTH_URI'],
    'token_uri':  os.environ['TOKEN_URI'],
    'auth_provider_x509_cert_url':  os.environ['AUTH_PROVIDER_X509_CERT_URL'],
    'client_x509_cert_url':  os.environ['CLIENT_X509_CERT_URL']
}

creds = ServiceAccountCreds(
    scopes=[
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/devstorage.read_write",
        "https://www.googleapis.com/auth/devstorage.full_control",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
        "https://www.googleapis.com/auth/cloud-platform",
    ],
    **INFO
)


async def list_storage_buckets(project_id=creds["project_id"]):
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        storage = await aiogoogle.discover("storage", "v1")
        res = await aiogoogle.as_service_account(
            storage.buckets.list(project=creds["project_id"])
        )
        print(res)


if __name__ == "__main__":
    asyncio.run(list_storage_buckets())
