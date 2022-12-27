from pydantic import AnyUrl, BaseModel


class DatabaseConfig(BaseModel):
    DATABASE_URL: AnyUrl = (
        "postgresql://sidus:Nuwr5bbT@localhost/sidus_backend"
    )
