import click
from pathlib import Path
from astor import to_source
from tree_sitter_types.node_types import nodes_from_json
from tree_sitter_types.generation.code_generator import (
    build_class_for_type,
    imports,
    import_library,
    type_name_map,
    base_class,
)
from black import format_str, FileMode


@click.command()
@click.argument("type-file")
@click.argument("target")
def generate_types(type_file, target):
    """Generate Python classes for tree-sitter types.

    TYPE_FILE is the path to the JSON file containing the tree-sitter types.
    TARGET is the path to the file where the generated classes will be written.
    """
    file = Path(type_file)

    if not file.exists():
        click.echo(f"File {type_file} does not exist.")
        exit(1)

    type_json = file.read_text(encoding="utf-8")

    nodes = nodes_from_json(type_json)

    target = Path(target)

    file = [
        to_source(imports()),
        to_source(import_library()),
        to_source(base_class()),
    ] + [to_source(build_class_for_type(node)) for node in nodes if node.named] + [
        to_source(type_name_map(nodes))
    ]

    with target.open("w") as f:
        f.write(format_str("\n".join(file), mode=FileMode()))


if __name__ == "__main__":
    generate_types()
