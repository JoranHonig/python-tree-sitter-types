import click
from pathlib import Path
from astor import to_source
from python_tree_sitter_types.node_types import nodes_from_json
from python_tree_sitter_types.generation.transformer import build_class_for_type, imports, type_name_map, base_class


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

    type_json = file.read_text(encoding='utf-8')

    nodes = nodes_from_json(type_json)

    target = Path(target)
    with target.open('w') as f:
        f.write(to_source(imports()))
        f.write(to_source(base_class()))
        for node in nodes:
            if node.named:
                f.write(to_source(build_class_for_type(node)))
        f.write(to_source(type_name_map(nodes)))


if __name__ == "__main__":
    generate_types()
