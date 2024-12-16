import logging
from datetime import datetime, UTC
from http.client import HTTPException

from starlette.exceptions import HTTPException

from src.database.runs_crud import RunsCRUD
from src.models.messages import Messages
from src.models.runs import Run, Status


class RunsService:
    runs_crud = RunsCRUD()
    model = Run

    async def get_run(self, run_id: int) -> Run:
        return await self.runs_crud.get_by_id(run_id)

    async def get_pending(self):
        return await self.runs_crud.get_pending()

    async def add(self, run_data: Run):
        await self.runs_crud.add(**run_data.model_dump())
        return await self.get_run(run_data.run_id)

    async def update(self, run_id: int, run_data: Run):
        await self.runs_crud.update(run_id, **run_data.model_dump(exclude_unset=True))
        return await self.get_run(run_id)

    async def get_result(self, run_id: str) -> float | None:
        run = await self.runs_crud.get_by_id(run_id)
        if run:
            return run.result
        else:
            raise HTTPException(status_code=404, detail="Run not found")

    async def add_from_kafka(self, msg: Messages):
        logging.info("Starting adding run in db")
        if msg.status == Status.scheduled.value:
            run = Run(
                id=msg.run_id,
                cadastral_number=msg.cadastral_number,
                params=msg.params,
                status=Status.processing,
                run_type=msg.run_type,
                start_time=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            )
            await self.runs_crud.add(**run.model_dump())

        else:
            run = Run(
                id=msg.run_id,
                status=msg.status,
                run_type=msg.run_type,
                result=msg.result,
            )
            await self.runs_crud.update(msg.run_id, **run.model_dump(exclude_unset=True))
