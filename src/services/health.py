class HealthService:

    @classmethod
    async def get_health(cls):
        return {"detail": "App is alive"}
