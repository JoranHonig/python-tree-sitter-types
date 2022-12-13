from toolz import curry


def dfs_walk(cursor):
    """Walk a raw tree-sitter tree in depth-first order."""
    step = cursor.goto_first_child()
    if step:
        return step

    step = cursor.goto_next_sibling()
    if step:
        return step

    step = None
    while step is None:
        cursor.goto_parent()
        step = cursor.goto_next_sibling()
    return step


def dfs_generator(tree):
    """Generator that walks a tree-sitter tree in depth-first order."""
    cursor = tree.walk()

    yield cursor.node

    while dfs_walk(cursor):
        yield cursor.node


def get_constructor(type_name, wrappers):
    """Gets the constructor for a node of the appropriate type."""
    return wrappers[type_name]


@curry
def parse_node(wrappers, node):
    """Parse a node into a typed Python object.

    wrappers: A dictionary mapping node type names to constructors provided by the generated python code
    node: The root node of a tree-sitter ast

    :returns A typed Python object representing the tree-sitter ast
    """
    inner_parse_node = parse_node(wrappers)

    type_name = node.type
    fields = {}
    all_children = []
    children = []
    if not node.children:
        new_node = get_constructor(type_name, wrappers)
        new_node.base_node = node
        return new_node

    for field_name in wrappers.get(type_name).field_names:
        field_children = list(map(inner_parse_node, node.children_by_field_name(field_name)))
        fields[field_name] = field_children
        all_children += field_children or []

    for child in node.named_children:
        if child in all_children:
            pass
        children += [inner_parse_node(child)]

    fields["children"] = children

    new_node = get_constructor(type_name, wrappers)

    for key, value in fields.items():
        setattr(new_node, key, value)

    new_node.children = children
    new_node.base_node = node

    return new_node

# TODO: allow users to specify literals
# TODO: sanity check input for field names "children" and "field_names" and "base_node"
# TODO: create clean way of initialising fields
