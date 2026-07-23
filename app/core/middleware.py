from time import perf_counter
from urllib import response
from fastapi import Request


async def add_response_time(request: Request, call_next):
    start = perf_counter()
    response = await call_next(request) 
    response.headers["Response-Time-taken"] = (f"{(perf_counter() - start) * 1000:.2f}ms")
    response.headers["Application"] = "AI Service Desk"
    return response 
