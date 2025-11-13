from typing import Any
from fastmcp import FastMCP
from api.database import database_engine as engine
from api.mappers import map_contact
from data.contact_queries import ContactQueries

mcp = FastMCP(name="Magic 8")

Data = dict[str, Any]

@mcp.tool
def get_all_contacts() -> list[Data]:
    queries = ContactQueries(engine)
    contacts = queries.get_contacts()
    return [map_contact(contact).model_dump() for contact in contacts]

@mcp.tool
def get_contacts_by_tag(tag: str) -> list[Data]:
    queries = ContactQueries(engine)
    contacts = queries.get_contacts_by_tag(tag)
    return [map_contact(contact).model_dump() for contact in contacts]
