from unittest import mock

import pytest

from collector_db.DTOs.URLInfo import URLInfo
from collector_db.DatabaseClient import DatabaseClient
from core.CoreLogger import CoreLogger
from source_collectors.common_crawler.CommonCrawlerCollector import CommonCrawlerCollector
from source_collectors.common_crawler.DTOs import CommonCrawlerInputDTO


@pytest.fixture
def mock_get_common_crawl_search_results():
    mock_path = "source_collectors.common_crawler.CommonCrawler.get_common_crawl_search_results"
    # Results contain other keys, but those are not relevant and thus
    # can be ignored
    mock_results = [
        "http://keyword.com",
        "http://example.com",
        "http://keyword.com/page3"
    ]
    with mock.patch(mock_path) as mock_get_common_crawl_search_results:
        mock_get_common_crawl_search_results.return_value = mock_results
        yield mock_get_common_crawl_search_results


def test_common_crawl_collector(mock_get_common_crawl_search_results):
    collector = CommonCrawlerCollector(
        batch_id=1,
        dto=CommonCrawlerInputDTO(
            search_term="keyword",
        ),
        logger=mock.MagicMock(spec=CoreLogger),
        db_client=mock.MagicMock(spec=DatabaseClient)
    )
    collector.run()
    mock_get_common_crawl_search_results.assert_called_once()

    collector.db_client.insert_urls.assert_called_once_with(
        url_infos=[
            URLInfo(url="http://keyword.com"),
            URLInfo(url="http://keyword.com/page3")
        ],
        batch_id=1
    )

