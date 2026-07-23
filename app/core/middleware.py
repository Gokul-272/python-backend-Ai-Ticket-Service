# from time import perf_counter
# from urllib import response
# from fastapi import Request


# async def add_response_time(request: Request, call_next):
#     start = perf_counter()
#     response = await call_next(request) 
#     response.headers["Response-Time-taken"] = (f"{(perf_counter() - start) * 1000:.2f}ms")
#     response.headers["Application"] = "AI Service Desk"
#     return response 

import datetime
from fileinput import filename
from time import perf_counter
from fastapi import Request
import cProfile

async def add_response_time(request: Request, call_next):
    profiler = cProfile.Profile()

    start = perf_counter()
    profiler.enable()

    response = await call_next(request)

    profiler.disable()

    elapsed = (perf_counter() - start) * 1000

    response.headers["Response-Time-Taken"] = f"{elapsed:.2f} ms"
    response.headers["Application"] = "AI Service Desk"
    filename = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.prof"
    profiler.dump_stats(filename)

    return response