from pydantic import BaseModel, parse_obj_as
from typing import List, Dict, Optional


class TypeSpecification(BaseModel):
    type: str
    named: bool


class ChildrenSpecification(BaseModel):
    multiple: bool
    required: bool
    types: List[TypeSpecification]


class FieldSpecification(ChildrenSpecification):
    pass


class NodeType(BaseModel):
    type: str
    named: bool
    fields: Optional[Dict[str, FieldSpecification]]
    children: Optional[ChildrenSpecification]


class NodeTypeList(BaseModel):
    __root__: List[NodeType]


def nodes_from_json(json_str: str) -> List[NodeType]:
    return NodeTypeList.parse_raw(json_str).__root__
