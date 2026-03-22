from pydantic import BaseModel


class RelationshipCreate(BaseModel):
    id: str
    from_type: str
    from_id: str
    to_type: str
    to_id: str
    relationship_type: str


class RelationshipResponse(RelationshipCreate):
    model_config = {"from_attributes": True}
