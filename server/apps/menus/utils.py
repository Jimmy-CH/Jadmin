

def build_tree(nodes, parent_id=None):
    tree = []
    node_map = {node.id: node for node in nodes}
    for node in nodes:
        node.children = []

    for node in nodes:
        if node.parent_id == parent_id:
            tree.append(node)
        else:
            parent = node_map.get(node.parent_id)
            if parent is not None:
                parent.children.append(node)

    # 递归排序子节点
    def sort_children(item):
        item.children.sort(key=lambda x: (x.sort, x.id))
        for child in item.children:
            sort_children(child)

    for root in tree:
        sort_children(root)

    tree.sort(key=lambda x: (x.sort, x.id))
    return tree

