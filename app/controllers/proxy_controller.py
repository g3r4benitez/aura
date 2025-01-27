import httpx
from fastapi import APIRouter, Request, Response, BackgroundTasks, Depends

from app.core.config import EXTERNAL_API_URL
from app.exceptions.general_exeptions import BadGatewayError
from app.core.config import CONNECTION_TIMEOUT
from app.core.celery_worker import save_statistic_task

from app.core.logger import logger

router = APIRouter()

#background_task = BackgroundTasks()

@router.api_route("/{path:path}", methods=["GET"])
async def proxy(request: Request, path: str, background_task: BackgroundTasks):
    url = f"{EXTERNAL_API_URL}/{path}"
    background_task.add_task(logger.info, msg=f"calling to external api with: '{url}'")

    async with httpx.AsyncClient() as client:

        params = request.query_params

        headers = dict(request.headers)
        headers.pop("host", None)  # Opcional: eliminar la cabecera 'host'

        body = await request.body()

        try:
            external_response = await call_external_api(body, client, headers, params, request, url)
        except httpx.RequestError as e:
            message = (f"Error al conectarse a la API externa: {e}, "
                       f"url: {url}, params: {params}, headers: {headers}, body: {body}")

            background_task.add_task(logger.info, msg=message)
            save_statistic_task.delay(url, 502, 0)

            raise BadGatewayError(message)

    background_task.add_task(logger.info, msg=f"response.status_code: {external_response.status_code}, "
                                              f"response.content: {external_response.content}")
    save_statistic_task.delay(url, external_response.status_code, external_response.elapsed.total_seconds())


    response = Response(
        content=external_response.content,
        status_code=external_response.status_code,
        headers=external_response.headers,
    )

    return response


async def call_external_api(body, client, headers, params, request, url):
    external_response = await client.request(
        method=request.method,
        url=url,
        params=params,
        headers=headers,
        content=body,
        timeout=CONNECTION_TIMEOUT
    )
    return external_response