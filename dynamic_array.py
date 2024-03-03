# Name: Haedon Kaufman
# OSU Email: kaufmhae@gmail.com
# Course: CS261 - Data Structures
# Assignment: Assignment 2
# Due Date: 02/05/24
# Description: The DynamicArray class offers a resizable array-like structure, ensuring efficient append operations.
# Built atop a static array, its capacity grows automatically when needed. Methods enable element access, modification,
# and iteration, maintaining the dynamic adjustment of its size.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resize the storage of the dynamic array (self._data)
        to the given new_capacity. If the new capacity is not valid, the method
        does nothing.
        """

        # Check if new_capacity is a positive number greater than the current size of the dynamic array
        if new_capacity > self._size > 0:

            new_array = StaticArray(new_capacity)

            # Copy elements from the original array
            for i in range(self._size):
                new_array.set(i, self._data.get(i))

            # Update the reference to the new array and set the new capacity
            self._data = new_array
            self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Adds a new value at the end of the dynamic array.
        If the internal storage is full, it doubles its capacity.
        """
        # If the dynamic array is full, double its capacity
        if self._size == self._capacity:
            self.resize(2 * self._capacity)

        # Set the new value at the next available position
        self._data.set(self._size, value)

        # Increment the size
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Insert the given value at the specified index in the dynamic array. If the internal storage is full,
        double it before adding the new value.
        """

        # Check for valid index range
        if index < 0 or index > self._size:
            raise DynamicArrayException("Invalid index provided")

        # If the array is full double its capacity
        if self._size == self._capacity:
            self.resize(2 * self._capacity)

        # Shift elements to the right of the index
        for i in range(self._size, index, -1):
            self._data.set(i, self._data.get(i - 1))

        self._data.set(index, value)

        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Remove the given value at the specified index in the dynamic array. If the internal storage is full,
        double it before adding the new value.
        """
        if index < 0 or index >= self.length():
            raise DynamicArrayException("Invalid index")

        # Check if we need to reduce the capacity before we remove
        if self.length() < 0.25 * self.get_capacity() and self.get_capacity() > 10:
            new_capacity = 2 * self.length()
            if new_capacity < 10:
                new_capacity = 10
            self.resize(new_capacity)

        # Remove element at the index
        for i in range(index, self.length() - 1):
            self._data.set(i, self._data.get(i + 1))

        # Decrement size
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Slice the given value at the specified index in the dynamic array.
        """
        # Check if start_index is valid
        if start_index < 0 or start_index >= self.length():
            raise DynamicArrayException("Invalid start index")

        # Check if size is valid
        if size < 0 or start_index + size > self.length():
            raise DynamicArrayException("Invalid size for slice")

        # Create new DynamicArray
        new_array = DynamicArray()

        # Add the elements to the new DynamicArray
        for i in range(size):
            new_array.append(self._data.get(start_index + i))

        return new_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merge two arrays keeping order of both
        """
        for i in range(second_da.length()):
            self.append(second_da.get_at_index(i))

    def map(self, map_func) -> "DynamicArray":
        """
        Maps the values of an array to a new array depending on the provided function
        """
        # Create a new empty DynamicArray
        new_da = DynamicArray()

        # Iterate through the current DynamicArray
        for i in range(self.length()):
            new_da.append(map_func(self._data.get(i)))

        return new_da

    def filter(self, filter_func) -> "DynamicArray":
        """
        Filters an array to a new array depending on the filter function
        """
        # Create an empty dynamic array to hold the filtered results
        result = DynamicArray()

        for i in range(self.length()):
            # If the filter function returns True for the current element,
            # append it to the result dynamic array
            if filter_func(self._data[i]):
                result.append(self._data[i])

        return result

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Reduces a given dynamic array to a new array applying the reduce function
        """
        # If the array is empty and no initializer is provided
        if self.length() == 0 and initializer is None:
            return None

        # If the array is empty but an initializer is provided
        if self.length() == 0:
            return initializer

        # Start reducing
        if initializer is None:
            # If no initializer is provided, use the first element of the array
            result = self._data.get(0)
            start_index = 1
        else:
            # If an initializer is provided, use it as the starting point
            result = initializer
            start_index = 0

        # apply the reduce_func
        for i in range(start_index, self.length()):
            result = reduce_func(result, self._data.get(i))

        return result


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a function that has already been sorted and returns the mode 
    """
    current_count = 1
    max_count = 1
    last_value = arr.get_at_index(0)

    modes = DynamicArray()
    modes.append(last_value)

    for i in range(1, arr.length()):
        # If the current element is the same as the previous one, increment the current count
        if arr.get_at_index(i) == last_value:
            current_count += 1
        else:
            # If the current count is higher than the highest count found so far
            if current_count > max_count:
                max_count = current_count
                modes = DynamicArray()
                modes.append(last_value)
            # If current_count equals max_count, add to the modes array
            elif current_count == max_count:
                modes.append(last_value)

            current_count = 1
            last_value = arr.get_at_index(i)

    # Handle the last group of numbers
    if current_count > max_count:
        modes = DynamicArray()
        modes.append(last_value)
    elif current_count == max_count:
        modes.append(last_value)

    return modes, max_count


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(8)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
