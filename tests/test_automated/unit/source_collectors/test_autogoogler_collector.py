from unittest.mock import MagicMock

import pytest

from collector_db.DTOs.URLInfo import URLInfo
from collector_db.DatabaseClient import DatabaseClient
from core.CoreLogger import CoreLogger
from source_collectors.auto_googler.AutoGooglerCollector import AutoGooglerCollector
from source_collectors.auto_googler.DTOs import GoogleSearchQueryResultsInnerDTO, AutoGooglerInputDTO


@pytest.fixture
def patch_get_query_results(monkeypatch):
    patch_path = "source_collectors.auto_googler.GoogleSearcher.GoogleSearcher.get_query_results"
    mock = MagicMock()
    mock.side_effect = [
        [GoogleSearchQueryResultsInnerDTO(url="https://include.com/1", title="keyword", snippet="snippet 1"),],
        None
    ]
    monkeypatch.setattr(patch_path, mock)
    yield mock

def test_auto_googler_collector(patch_get_query_results):
    mock = patch_get_query_results
    collector = AutoGooglerCollector(
        batch_id=1,
        dto=AutoGooglerInputDTO(
            queries=["keyword"]
        ),
        logger=MagicMock(spec=CoreLogger),
        db_client=MagicMock(spec=DatabaseClient),
        raise_error=True
    )
    collector.run()
    mock.assert_called_once_with("keyword")

    collector.db_client.insert_urls.assert_called_once_with(
        url_infos=[URLInfo(url="https://include.com/1", collector_metadata={"query": "keyword", "title": "keyword", "snippet": "snippet 1"})],
        batch_id=1
    )