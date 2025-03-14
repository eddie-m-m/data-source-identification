from unittest.mock import MagicMock

from collector_db.DatabaseClient import DatabaseClient
from core.CoreLogger import CoreLogger
from source_collectors.muckrock.DTOs import MuckrockSimpleSearchCollectorInputDTO, \
    MuckrockCountySearchCollectorInputDTO, MuckrockAllFOIARequestsCollectorInputDTO
from source_collectors.muckrock.classes.MuckrockCollector import MuckrockSimpleSearchCollector, \
    MuckrockCountyLevelSearchCollector, MuckrockAllFOIARequestsCollector
from source_collectors.muckrock.schemas import MuckrockURLInfoSchema
from test_automated.integration.core.helpers import ALLEGHENY_COUNTY_MUCKROCK_ID, ALLEGHENY_COUNTY_TOWN_NAMES


def test_muckrock_simple_search_collector():

    collector = MuckrockSimpleSearchCollector(
        batch_id=1,
        dto=MuckrockSimpleSearchCollectorInputDTO(
            search_string="police",
            max_results=10
        ),
        logger=MagicMock(spec=CoreLogger),
        db_client=MagicMock(spec=DatabaseClient),
        raise_error=True
    )
    collector.run()
    schema = MuckrockURLInfoSchema(many=True)
    schema.load(collector.data["urls"])
    assert len(collector.data["urls"]) >= 10


def test_muckrock_county_level_search_collector():
    collector = MuckrockCountyLevelSearchCollector(
        batch_id=1,
        dto=MuckrockCountySearchCollectorInputDTO(
            parent_jurisdiction_id=ALLEGHENY_COUNTY_MUCKROCK_ID,
            town_names=ALLEGHENY_COUNTY_TOWN_NAMES
        ),
        logger=MagicMock(spec=CoreLogger),
        db_client=MagicMock(spec=DatabaseClient)
    )
    collector.run()
    schema = MuckrockURLInfoSchema(many=True)
    schema.load(collector.data["urls"])
    assert len(collector.data["urls"]) >= 10



def test_muckrock_full_search_collector():
    collector = MuckrockAllFOIARequestsCollector(
        batch_id=1,
        dto=MuckrockAllFOIARequestsCollectorInputDTO(
            start_page=1,
            total_pages=2
        ),
        logger=MagicMock(spec=CoreLogger),
        db_client=MagicMock(spec=DatabaseClient)
    )
    collector.run()
    assert len(collector.data["urls"]) >= 1
    schema = MuckrockURLInfoSchema(many=True)
    schema.load(collector.data["urls"])