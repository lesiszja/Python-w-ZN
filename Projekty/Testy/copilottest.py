def generate_tree(height):
    for i in range(height):
        print(' ' * (height - i - 1) + '*' * (2 * i + 1))

if __name__ == "__main__":
    tree_height = int(input("Enter the height of the tree: "))
    generate_tree(tree_height)