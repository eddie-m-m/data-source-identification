import pytest

from collector_db.DTOs.InsertURLsInfo import InsertURLsInfo
from core.DTOs.GetURLsResponseInfo import GetURLsResponseInfo


@pytest.mark.asyncio
async def test_get_urls(api_test_helper):
    # Basic test, no results
    data: GetURLsResponseInfo = api_test_helper.request_validator.get_urls()

    assert data.urls == []
    assert data.count == 0

    db_data_creator = api_test_helper.db_data_creator

    # Create batch with status `in-process` and strategy `example`
    batch_id = db_data_creator.batch()
    # Create 2 URLs with outcome `pending`
    iui: InsertURLsInfo = db_data_creator.urls(batch_id=batch_id, url_count=3)

    url_id_1st = iui.url_mappings[0].url_id

    # Add metadata
    await db_data_creator.metadata(url_ids=[url_id_1st])

    # Get the latter 2 urls
    url_ids = [iui.url_mappings[1].url_id, iui.url_mappings[2].url_id]

    # Add errors
    await db_data_creator.error_info(url_ids=url_ids)


    data: GetURLsResponseInfo = api_test_helper.request_validator.get_urls()
    assert data.count == 3
    assert len(data.urls) == 3
    assert data.urls[0].url == iui.url_mappings[0].url
    assert len(data.urls[0].metadata) == 1

    for i in range(1, 3):
        assert data.urls[i].url == iui.url_mappings[i].url
        assert len(data.urls[i].errors) == 1
        assert len(data.urls[i].metadata) == 0

    # Retrieve data again with errors only
    data: GetURLsResponseInfo = api_test_helper.request_validator.get_urls(errors=True)
    assert data.count == 2
    assert len(data.urls) == 2
    for url in data.urls:
        assert url.id != url_id_1st

