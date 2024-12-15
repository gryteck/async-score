from datetime import datetime, UTC

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

    async def get_result(self, run_id: int) -> float:
        run = await self.runs_crud.get_by_id(run_id)
        return run.result

    async def add_from_kafka(self, msg: Messages):
        if msg.status == Status.scheduled.value:
            run = Run(
                run_id=msg.run_id,
                cadastral_number=msg.cadastral_number,
                params=msg.params,
                status=Status.processing,
                run_type=msg.run_type,
                start_time=datetime.now(UTC),
            )
            await self.runs_crud.add(**run.model_dump())

        else:
            run = Run(
                run_id=msg.run_id,
                status=msg.status,
                run_type=msg.run_type,
                result=msg.result,
            )
            await self.runs_crud.update(msg.run_id, **run.model_dump(exclude_unset=True))
