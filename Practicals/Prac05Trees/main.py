from trees import DSABinarySearchTree

def main():
    """
    An interactive menu to demonstrate the binary search tree.
    """
    tree = DSABinarySearchTree()

    while True:
        print("\n### Binary Search Tree Menu ###")
        print("1. Add a node")
        print("2. Delete a node")
        print("3. Display the tree")
        print("4. Find min, max, height, and balance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                key = int(input("Enter key (integer): "))
                value = input("Enter value: ")
                tree.insert(key, value)
                print(f"Node with key {key} added.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            try:
                key = int(input("Enter key to delete: "))
                tree.delete(key)
                print(f"Node with key {key} deleted.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '3':
            print("\n--- Display Options ---")
            print("a. Inorder traversal")
            print("b. Preorder traversal")
            print("c. Postorder traversal")
            display_choice = input("Enter display choice: ")

            if display_choice == 'a':
                print("Inorder:", tree.inorder_traversal())
            elif display_choice == 'b':
                print("Preorder:", tree.preorder_traversal())
            elif display_choice == 'c':
                print("Postorder:", tree.postorder_traversal())
            else:
                print("Invalid display choice.")
        elif choice == '4':
            print(f"Min key: {tree.min()}")
            print(f"Max key: {tree.max()}")
            print(f"Height: {tree.height()}")
            print(f"Balance: {tree.balance():.2f}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()