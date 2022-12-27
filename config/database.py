from pydantic import AnyUrl, BaseModel


class DatabaseConfig(BaseModel):
    DATABASE_URL: AnyUrl = (
        "postgresql://sidus:$uwr5bbT@localhost/sidus_backend"
    )
