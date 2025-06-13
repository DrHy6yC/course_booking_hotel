from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter(prefix="/docs")


@router.get(
    path="",
    include_in_schema=False
)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=router.openapi_url,
        title=router.title + " - Swagger UI",
        oauth2_redirect_url=router.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )