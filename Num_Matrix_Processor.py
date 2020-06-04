# Procedural version

def check_len_for_add(a_matrix, b_matrix):
    """
    Takes in two matrices.
    Returns True if the matrices are of same length.
    """
    return [len(i) for i in a_matrix] == [len(j) for j in b_matrix]

def check_len_for_mult(a_matrix, b_matrix):
    """
    Takes in two matrices.
    Returns True if the columns in the first matrix are of same length as the rows in the second matrix.
    """
    return len(a_matrix[0]) == len(b_matrix)

def check_size_for_det(matrix):
    return len(matrix[0]) == len(matrix)

def create_matrix(num):
    """
    Takes in user input:
        the size of the matrix (entered as two numbers)
        the matrix itself
    Returns the created matrix.
    """
    nums = {0: "", 1: " first", 2: " second"}
    matrices = []
    start = 1 if num > 0 else 0
    for i in range(start, num+1):
        try:
            print(f"Enter size of{nums[i]} matrix: ")
            row, col = input().split()
        except ValueError:
            print("Invalid input.\n")
            return create_matrix(num)
        print(f"Enter{nums[i]} matrix:")
        matrix = [[num for num in input().split()] for _i in range(int(row))]
        int_or_float = int
        for j in matrix:
            if any(map(lambda x: "." in x, j)):
                int_or_float = float
        matrix = [[int_or_float(num) for num in row] for row in matrix]
        if not all([len(i) == int(col) for i in matrix]) or len(matrix) != int(row):
            print("Invalid input.\n")
            return create_matrix(num)
        matrices.append(matrix)
    return matrices

def add_two_matrices(a_matrix, b_matrix):
    """
    Takes in two matrices.
    Returns a new matrix, which is the result of the two matrices added together.
    """
    if not check_len_for_add(a_matrix, b_matrix):
        return "ERROR"
    a_plus_b_matrix = []
    for r in range(len(a_matrix)):
        rows = []
        for c in range(len(a_matrix[0])):
            rows.append(a_matrix[r][c] + b_matrix[r][c])
        a_plus_b_matrix.append(rows)
    return a_plus_b_matrix

def multiply_matrix_by_constant(matrix):
    """
    Takes in a matrix and a constant.
    Returns a new matrix with each element multiplied by the constant.
    """
    print("Enter constant: ")
    constant = int(input())
    return [[constant*num for num in row] for row in matrix]

def multiply_two_matrices(a_matrix, b_matrix):
    """
    Takes in two matrices.
    Returns a new matrix which is the result of first matrix multiplied by the second matrix.
    """
    if not check_len_for_mult(a_matrix, b_matrix):
        return "The operation cannot be performed."
    # Creating a tuple of the positions of the elements in the second matrix to iterate over the inner loop.
    b_rows = tuple(i for i in range(len(b_matrix[0])) for i in range(len(b_matrix)))
    b_cols = tuple(x for x in range(len(b_matrix[0])) for i in range(len(b_matrix)))
    b_rows_cols = tuple(zip(b_rows, b_cols))
    # Multiplying each element of first to the corresponding element of the second list.
    # Saving the results of the multiplication to one single list.
    elements = []
    for i in range(len(a_matrix)):
        for j in b_rows_cols:
            new_element = a_matrix[i][j[0]] * b_matrix[j[0]][j[1]]
            elements.append(new_element)
    # Splitting the 'elements' list into lists corresponding to the num of rows in first matrix,
    # in order to calculate their sum and obtain the elements of the new list.
    ab_matrix = [elements[i:i+len(a_matrix[0])] for i in range(0, len(elements), len(a_matrix[0]))]
    ab_matrix = [sum(i) for i in ab_matrix]
    # Creating the new matrix by separating the list into multiple lists
    # corresponding to the number of elements of the second matrix.
    return [ab_matrix[i:i+len(b_matrix[0])] for i in range(0, len(ab_matrix), len(b_matrix[0]))]

def transpose_matrix():
    """
    Creates a matrix and
    returns a transposed version of the matrix:
    on the main diagonal, side diagonal, vertical line or horizontal line.
    """
    print("1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line")
    transposition_type = int(input())
    print(f"Your choice: {transposition_type}")
    matrix = create_matrix(0)[0]
    if transposition_type == 1:
        return main_diagonal(matrix)
    elif transposition_type == 2:
        return side_diagonal(matrix)
    elif transposition_type == 3:
        return vertical_line(matrix)
    elif transposition_type == 4:
        return horizontal_line(matrix)

def main_diagonal(matrix):
    """Takes in a matrix and returns a transposed matrix on the main diagonal"""
    transposed_matrix = []
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            transposed_matrix.append(matrix[j][i])
    transposed_matrix = [transposed_matrix[i:i + len(matrix)] for i in range(0, len(transposed_matrix), len(matrix))]
    return transposed_matrix

def side_diagonal(matrix):
    """Takes in a matrix and returns a transposed matrix on the side diagonal"""
    return horizontal_line(vertical_line(main_diagonal(matrix)))

def vertical_line(matrix):
    """Takes in a matrix and returns a transposed matrix on the vertical line"""
    return [item[::-1] for item in matrix]

def horizontal_line(matrix):
    """Takes in a matrix and returns a transposed matrix on the horizontal line line"""
    return matrix[::-1]

def find_determinant(matrix):
    """Takes in a matrix.
        Returns the determinant of the matrix"""
    if not check_size_for_det(matrix):
        return "The determinant can only be defined for square matrices."
    elif len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif len(matrix) > 2:
        determinant = 0
        first_row = matrix[0]
        det_matrix = main_diagonal(matrix[1:])
        for idx, item in enumerate(first_row):
            det_submatrix = [i for i_idx, i in enumerate(det_matrix) if i_idx != idx]
            sign = (-1) ** (idx)
            element = item * find_determinant(det_submatrix)
            if sign > 0:
                determinant += element
            else:
                determinant -= element
        return determinant

def inverse_matrix(matrix):
    """
    Takes in a matrix.
    Returns the inverse of the matrix.
    """
    if not check_size_for_det(matrix):
        return "Only square matrices can be inversed."
    det = find_determinant(matrix)
    if det == 0:
        return "This matrix doesn't have an inverse."
    adjoint = []
    for i_idx, item in enumerate(matrix):
        _first_row = matrix[i_idx]
        det_matrix = main_diagonal([i for idx, i in enumerate(matrix) if idx != i_idx])
        rows = []
        for e_idx, element in enumerate(item):
            det_submatrix = [el for idx, el in enumerate(det_matrix) if idx != e_idx]
            cof_sign = (-1) ** (i_idx + e_idx)
            cofactor = cof_sign * find_determinant(det_submatrix)
            rows.append(cofactor)
        adjoint.append(rows)
    constant = 1/det
    inversed_matrix = main_diagonal([[constant*num for num in row] for row in adjoint])
    return inversed_matrix


choice = ""
choices = {1: add_two_matrices, 2: multiply_matrix_by_constant, 3: multiply_two_matrices, 0:quit}
while True:
    print("1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices\n4. Transpose matrix\n"
          "5. Calculate a determinant\n6. Inverse matrix.\n0. Exit")
    choice = int(input())
    print(f"Your choice: {choice}")
    if choice == 0:
        break
    elif choice == 1:
        m = create_matrix(2)
        m1, m2 = m[0], m[1]
        result = add_two_matrices(m1, m2)
    elif choice == 2:
        m = create_matrix(0)[0]
        result = multiply_matrix_by_constant(m)
    elif choice == 3:
        m = create_matrix(2)
        m1, m2 = m[0], m[1]
        result = multiply_two_matrices(m1, m2)
    elif choice == 4:
        result = transpose_matrix()
    elif choice == 5:
        m = create_matrix(0)[0]
        result = find_determinant(m)
    elif choice == 6:
        m = create_matrix(0)[0]
        result = inverse_matrix(m)
    if type(result) == int or type(result) == float:
        print(f"The result is:\n{result}")
    elif type(result) == list:
        print("\n".join(" ".join([str(round(el+0,4)) for el in row]) for row in result))
    else:
        print(result)
    print()