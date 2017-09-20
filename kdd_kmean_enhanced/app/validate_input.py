# Purpose: Validate user input in console window

# Validate input as integer within [start, end] inclusive
def validate_int_in_range_inc(start,end,message):
    input_str = input(message)  # check input validation later
    input_int = validate_int(input_str,message)

    # Check value in range (1, num_records) inclusive
    while not (input_int in range(start, end + 1)):
        print("You must select an integer in range (1:{}) inclusive".format(end))
        input_str = input(message)
        input_int = validate_int(input_str, message)
    return input_int

# Sub-function to valide interger input
def validate_int(input_str, message):
    valid_input_k_bool = False
    while not valid_input_k_bool:
        try:
            number_input = int(input_str)
            valid_input_k_bool = True
        except Exception:
            print("Bad input, it must be an integer")
            input_str = input(message)
    return  number_input