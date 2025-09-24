import asyncio
import functools


def fix_exec_time(time):

	def decorator(func):

		@functools.wraps(func)
		async def wrapper(*args, **kwargs):
			sleep_task = asyncio.create_task(asyncio.sleep(time))
			coro_response = await func(*args, **kwargs)
			await sleep_task

			return coro_response

		return wrapper

	return decorator
