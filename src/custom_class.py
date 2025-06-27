from fastapi_cache import KeyBuilder
from typing import Optional, Any
from fastapi import Request, Response


class KeyBuilderCustom(KeyBuilder):
    def __init__(self, my_key: str):
        self.my_key = my_key

    async def __call__(
            self,
            function: Any,
            namespace: str = "",
            request: Optional[Request] = None,
            response: Optional[Response] = None,
            *args,
            **kwargs,
    ) -> str:
        return f"{self.my_key}"
