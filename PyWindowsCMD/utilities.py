def count_parameters(*args) -> int:
	"""
	Counts the number of non-empty parameters passed to the function.

	Args:
		*args: Variable number of arguments of any type.

	Returns:
		int: The number of non-empty arguments.

	:Usage:
		count = count_parameters(1, "", "hello", None, [], 0)  # Returns 2
	"""
	return len(list(filter(lambda x: bool(x), [*args])))
