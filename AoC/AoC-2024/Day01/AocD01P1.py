def calculate_total_distance(left_list, right_list):
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    
    # Calculate absolute differences between paired elements
    total_distance = sum(abs(left - right) for left, right in zip(left_sorted, right_sorted))
    
    return total_distance

# Read input from file
def read_input(filename):
    try:
        with open(filename, 'r') as file:
            # Read lines and split into two lists
            left_list, right_list = [], []
            for line in file:
                left, right = map(int, line.strip().split())
                left_list.append(left)
                right_list.append(right)
            return left_list, right_list
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return [], []
    except ValueError:
        print("Error: Invalid input format. Each line should contain two integers separated by whitespace.")
        return [], []

# Main function
def main():
    # Example input for testing
    # example_left = [3, 4, 2, 1, 3, 3]
    # example_right = [4, 3, 5, 3, 9, 3]
    
    # Calculate total distance for example
#    example_distance = calculate_total_distance(example_left, example_right)
#    print(f"Example total distance: {example_distance}")  # Should print 11
    
    # Read from input file (uncomment and set correct filename when using actual input)
    filename = 'D1.txt'
    left_list, right_list = read_input(filename)
    if left_list and right_list:
        total_distance = calculate_total_distance(left_list, right_list)
        print(f"Total distance from input: {total_distance}")

if __name__ == "__main__":
    main()