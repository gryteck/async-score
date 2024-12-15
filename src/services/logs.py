from src.database.logs_crud import LogsCRUD
from src.models.logs import Log, LogResponse, LogsListResponse
from src.models.messages import Messages


class LogsService:
    logs_crud = LogsCRUD()

    async def get_run_log_last(self, run_id: int) -> LogResponse:
        return await self.logs_crud.get_run_log_last(run_id)

    async def get_run_logs_list(
            self, run_id: int, page_num: int, page_size: int
    ) -> LogsListResponse:
        logs_list = await self.logs_crud.get_client_logs_list(
            run_id=run_id,
            page_num=page_num,
            page_size=page_size)

        return LogsListResponse(**logs_list)

    async def add_log(self, log_data: Log):
        await self.logs_crud.add_log(**log_data.model_dump())

    async def add_from_kafka(self, msg: Messages):
        log = Log(
            cadastral_number=msg.cadastral_number,
            run_id=msg.run_id,
            status=msg.status,
        )
        await self.add_log(log)
