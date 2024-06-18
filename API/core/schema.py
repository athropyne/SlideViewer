from sqlalchemy import Table, Column, String, MetaData, UUID

metadata = MetaData()

slides = Table(
    "slides",
    metadata,
    Column("ID", UUID(as_uuid=True), primary_key=True),
    Column("title", String(100)),
    Column("description", String(3000)),
    Column("original_name", String, nullable=False),
    Column("ext", String, nullable=False)
)
