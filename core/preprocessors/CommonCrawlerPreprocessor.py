from typing import List

from collector_db.DTOs.URLInfo import URLInfo
from core.preprocessors.PreprocessorBase import PreprocessorBase


class CommonCrawlerPreprocessor(PreprocessorBase):


    def preprocess(self, data: dict) -> List[URLInfo]:
        url_infos = []
        for url in data["urls"]:
            url_info = URLInfo(
                url=url,
            )
            url_infos.append(url_info)

        return url_infos