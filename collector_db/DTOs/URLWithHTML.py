from pydantic import BaseModel

from collector_db.DTOs.URLHTMLContentInfo import URLHTMLContentInfo


class URLWithHTML(BaseModel):
    url_id: int
    url: str
    html_infos: list[URLHTMLContentInfo]