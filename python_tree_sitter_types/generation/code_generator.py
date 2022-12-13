from ast import *
import ast
from typing import Union
from python_tree_sitter_types.node_types import *
from inflection import camelize


def from_typespec(_type: TypeSpecification):
    return Constant(value=camelize(_type.type) if _type.named else "str")
    # return Name(id=camelize(_type.type) if _type.named else "str", ctx=Load())


def from_types(types: List[TypeSpecification]) -> Union[Subscript, Constant, Name]:
    gen_types = list(map(from_typespec, types))
    match len(gen_types):
        case 0:
            return none_annotation()
        case 1:
            return gen_types[0]
        case _:
            return Subscript(
                value=Name(id="Union", ctx=Load()),
                slice=Tuple(elts=gen_types, ctx=Load()),
                ctx=Load(),
            )


def wrap_it(subscript: Subscript, name: str) -> Subscript:
    return Subscript(
        value=Name(id=camelize(name), ctx=Load()), slice=subscript, ctx=Load()
    )


def none_annotation() -> Constant:
    return Constant(value=None)


def type_annotation_from_field_child(
    element: Union[FieldSpecification, ChildrenSpecification]
) -> Union[Constant, Subscript]:
    type_annotation = from_types(element.types)

    type_annotation = (
        wrap_it(type_annotation, "List") if element.multiple else type_annotation
    )
    type_annotation = (
        wrap_it(type_annotation, "Optional")
        if not element.required
        else type_annotation
    )

    return type_annotation


def from_field(name: str, field: FieldSpecification) -> AnnAssign:
    type_annotation = type_annotation_from_field_child(field)
    return AnnAssign(
        target=Name(id=name, ctx=Store()), annotation=type_annotation, simple=1
    )


def build_class_for_type(node: NodeType) -> ClassDef:
    name = node.type
    fields = node.fields or dict()
    children = node.children
    return ClassDef(
        name=camelize(name) if node.named else "Token",
        bases=[Name(id="TreeSitterNode", ctx=Load())],
        keywords=[],
        body=[field_names_class_param(node)]
        + [
            from_field(field_name, field_spec)
            for field_name, field_spec in fields.items()
        ]
        + [
            AnnAssign(
                target=Name(id="children", ctx=Store()),
                annotation=type_annotation_from_field_child(children)
                if children
                else none_annotation(),
                simple=1,
            )
        ],
        decorator_list=[],
    )


def field_names_class_param(node: NodeType):
    return Assign(
        targets=[Name(id="field_names", ctx=Store())],
        value=ast.List(
            elts=[Constant(value=name) for name in (node.fields or dict()).keys()],
            ctx=Load(),
        ),
    )


def imports():
    return ImportFrom(
        module="typing",
        names=[
            alias(name="Union"),
            alias(name="Any"),
            alias(name="Optional"),
            alias(name="List"),
        ],
        level=0,
    )


def type_name_map(nodes):
    type_names = [node.type for node in nodes if node.named]

    return Assign(
        targets=[Name(id="type_name_to_class", ctx=Store())],
        value=ast.Dict(
            keys=[Constant(value=type_name) for type_name in type_names],
            values=[
                Name(id=camelize(type_name), ctx=Load()) for type_name in type_names
            ],
        ),
    )


def base_class():
    return parse(
        """
class TreeSitterNode:
    base_node: Any
    
    def text(self):
        return self.base_node.text
    """
    ).body[0]