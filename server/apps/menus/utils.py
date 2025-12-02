# utils.py

def build_tree(nodes):
    """
    将扁平的节点列表构造成具有父子关系的树形结构。
    此函数不修改原始 ORM 对象的 RelatedManager (e.g., node.children)，
    而是为每个节点添加一个 '_cached_children' 属性来存储其子节点。
    序列化器需要相应地读取这个属性。
    """
    if not nodes:
        return []

    # 创建一个映射，方便快速查找节点
    node_map = {node.id: node for node in nodes}
    root_nodes = []

    # 初始化所有节点的 _cached_children 列表
    for node in nodes:
        node._cached_children = [] # 使用临时属性存储子节点

    # 构建父子关系
    for node in nodes:
        if node.parent_id is None:
            root_nodes.append(node)
        else:
            parent_node = node_map.get(node.parent_id)
            if parent_node:
                # 将当前节点添加到其父节点的 _cached_children 列表中
                parent_node._cached_children.append(node)

    return root_nodes

