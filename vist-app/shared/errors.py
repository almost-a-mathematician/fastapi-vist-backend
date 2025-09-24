from asyncpg import UniqueViolationError


def is_unique_error(error: BaseException):
	original_error = error.__cause__.__cause__

	if isinstance(original_error, UniqueViolationError):
		return original_error
	else:
		return None
