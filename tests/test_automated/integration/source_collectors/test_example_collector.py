import threading
import time

from collector_db.DTOs.BatchInfo import BatchInfo
from collector_manager.DTOs.ExampleInputDTO import ExampleInputDTO
from collector_manager.ExampleCollector import ExampleCollector
from core.SourceCollectorCore import SourceCollectorCore
from core.enums import BatchStatus


def test_live_example_collector_abort(test_core: SourceCollectorCore):
    core = test_core
    db_client = core.db_client

    batch_id = db_client.insert_batch(
        BatchInfo(
            strategy="example",
            status=BatchStatus.IN_PROCESS,
            parameters={},
            user_id=1
        )
    )


    dto = ExampleInputDTO(
            sleep_time=3
    )

    collector = ExampleCollector(
        batch_id=batch_id,
        dto=dto,
        logger=core.core_logger,
        db_client=db_client,
        raise_error=True
    )
    # Run collector in separate thread
    thread = threading.Thread(target=collector.run)
    thread.start()
    collector.abort()
    time.sleep(2)
    thread.join()


    assert db_client.get_batch_status(batch_id) == BatchStatus.ABORTED

