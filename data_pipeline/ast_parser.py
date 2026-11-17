import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

def parse_code(code_str: str):
    tree = parser.parse(bytes(code_str, "utf8"))
    
    def walk(node, depth):
        node_count = 1
        max_depth = depth
        for child in node.children:
            c_count, c_depth = walk(child, depth + 1)
            node_count += c_count
            max_depth = max(max_depth, c_depth)
        return node_count, max_depth
    
    total_nodes, depth = walk(tree.root_node, 1)
    
    return {
        "ast_node_count": total_nodes,
        "ast_max_depth": depth,
    }

def get_ast_similarity(code1, code2):
    try:
        f1 = parse_code(code1)
        f2 = parse_code(code2)
        diff_nodes = abs(f1['ast_node_count'] - f2['ast_node_count'])
        diff_depth = abs(f1['ast_max_depth'] - f2['ast_max_depth'])
        return 1.0 / (1.0 + diff_nodes + diff_depth)
    except Exception:
        return 0.5
