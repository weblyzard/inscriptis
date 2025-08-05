#!/usr/bin/env python3
"""Inscriptis Web Service."""

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from inscriptis import get_text
from inscriptis.css_profiles import RELAXED_CSS_PROFILE
from inscriptis.metadata import __version__
from inscriptis.model.config import ParserConfig

app = FastAPI()
CONFIG = ParserConfig(
    css=RELAXED_CSS_PROFILE,
    display_images=True,
    deduplicate_captions=True,
    display_links=False,
)


@app.get("/")
def index() -> PlainTextResponse:
    """Print a short status message for the Web service's base URL."""
    return PlainTextResponse("Inscriptis text to HTML Web service.")


@app.post("/get_text", response_class=PlainTextResponse)
async def get_text_call(request: Request) -> str:
    """Return the text representation of the given HTML content."""
    content_type = request.headers.get("Content-type", "")
    encoding = content_type.split("; charset=")[1] if "; charset=" in content_type else "UTF-8"
    html_content = await request.body()
    return get_text(html_content.decode(encoding, errors="ignore"), CONFIG)


@app.get("/version", response_class=PlainTextResponse)
def get_version_call() -> str:
    """Return the used inscriptis version."""
    return __version__


def start() -> None:
    """Start the webservice."""
    import uvicorn

    print("Starting Web service based on Inscriptis", __version__)
    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    start()
