import datetime
import urllib.parse
from urllib.parse import urlparse

from aiohttp import web
from google.cloud import storage

from app import config
from app.sdk import sdk
from app.contrib.google_cloud import generate_signed_url
from app.fhirdate import get_now
from app.contrib.utils import robust_fn, sync_to_async


DEFAULT_EXPIRATION = 3600


@sdk.operation(
    ['GET'], ['$sign', {"name": "resource-type"}, {"name": "id"}])
async def operation_sign_resource(operation, request):
    expiration = DEFAULT_EXPIRATION

    resource_type = request['route-params']['resource-type']
    resource_id = request['route-params']['id']
    resource = await sdk.client.resources(resource_type).get(id=resource_id)
    sign_resource(resource)
    headers = {
        'Cache-Control': 'private, max-age={0}'.format(expiration),
    }

    return web.json_response(resource.serialize(), headers=headers)


@sdk.operation(
    ["POST"],
    ["$signed-upload"]
)
async def operation_singed_upload(operation, request):
    resource = request["resource"]
    file_name = resource['fileName'].split(".")
    extension = file_name[-1]
    file_name[-1] = str(datetime.datetime.now().timestamp())
    file_name.append(extension)
    file_name = ".".join(file_name)
    now = get_now()
    object_name = "uploads/{year}/{month}/{day}/{file_name}".format(
        file_name=file_name, year=now.year, month=now.month, day=now.day)
    object_url = "https://storage.googleapis.com/{bucket}/{object_name}".format(
        bucket=config.gc_bucket, object_name=object_name)
    signed_url = generate_signed_url(
        config.gc_account_file,
        config.gc_bucket,
        object_name=object_name,
        expiration=3600,
        http_method='PUT',
        headers={"Content-Type": resource['contentType']},
    )

    return web.json_response({
        "signedUploadUrl": signed_url,
        "objectUrl": object_url,
        "fileName": file_name})


@robust_fn
@sync_to_async
def google_storage_upload(path, content_str, content_type):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(config.gc_bucket)
    blob = storage.Blob(path, bucket)
    blob.upload_from_string(content_str, content_type=content_type)
    return urllib.parse.unquote(blob.public_url)


@robust_fn
@sync_to_async
def google_storage_download(path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(config.gc_bucket)
    blob = storage.Blob(path, bucket)
    return blob.download_as_string()


def sign_url(url: str, expiration: int):
    object_name = extract_google_storage_object_name_from_url(url)
    if object_name:
        return generate_signed_url(
            config.gc_account_file, config.gc_bucket, object_name, expiration)
    return url


def sign_resource(resource):
    def walk(tree):
        if isinstance(tree, dict):
            if 'url' in tree:
                tree['url'] = sign_url(tree['url'], DEFAULT_EXPIRATION)
        if isinstance(tree, dict):
            for branch in tree.values():
                walk(branch)
        if isinstance(tree, list):
            for branch in tree:
                walk(branch)

    walk(resource)


def extract_google_storage_object_name_from_url(url):
    if url.startswith('https://www.googleapis.com/'):
        return urlparse(url).path.split('/').pop()
    elif url.startswith('https://storage.googleapis.com/'):
        return urlparse(url).path.replace(
            '/{0}/'.format(config.gc_bucket),
            '',
        )
    else:
        return None
