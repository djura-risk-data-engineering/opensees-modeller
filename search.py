import ast
from pathlib import Path


def extract_tnodes_bnodes_from_file(file_path):
    """
    Extracts 'tnodes' and 'bnodes' by searching for 'supports' and 'floors'
    in a Python file.

    Parameters:
    ----------
    file_path : str or Path
        Path to the Python file.

    Returns:
    -------
    tuple
        A tuple containing 'tnodes' and 'bnodes'.
    """
    # Parse the file
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    supports, floors = None, None

    # Iterate through assignment nodes in the file
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == "supports":
                        supports = ast.literal_eval(node.value)
                    elif target.id == "floors":
                        floors = ast.literal_eval(node.value)

        # Stop searching if both are found
        if supports and floors:
            break

    # Compute tnodes and bnodes if supports and floors are found
    if supports and floors:
        tnodes = [floors, floors]
        bnodes = [[supports[0]] + floors[:-1], [supports[0]] + floors[:-1]]
        return tnodes, bnodes

    raise ValueError("Supports or Floors not found in the file.")


if __name__ == "__main__":
    # Path to the nspa.py file
    file_path = Path(__file__).parent / "src/mdof/nspa.py"

    try:
        tnodes, bnodes = extract_tnodes_bnodes_from_file(file_path)
        print(f"TNodes: {tnodes}")
        print(f"BNodes: {bnodes}")
    except ValueError as e:
        print(f"Error: {e}")
