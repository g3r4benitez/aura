import httpx
from fastapi import APIRouter, Request, Response

from app.core.config import EXTERNAL_API_URL

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(request: Request, path: str):
    url = f"{EXTERNAL_API_URL}/{path}"

    async with httpx.AsyncClient() as client:

        params = request.query_params

        headers = dict(request.headers)
        headers.pop("host", None)  # Opcional: eliminar la cabecera 'host'

        body = await request.body()

        try:
            external_response = await client.request(
                method=request.method,
                url=url,
                params=params,
                headers=headers,
                content=body,
                timeout=30.0
            )
        except httpx.RequestError as e:
            return Response(
                content=f"Error al conectarse a la API externa: {e}, url: {url}, params: {params}, headers: {headers}, body: {body}",
                status_code=502
            )


    response = Response(
        content=external_response.content,
        status_code=external_response.status_code,
        headers=external_response.headers
    )

    return response