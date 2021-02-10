DEBUGGER = True


def print_debug(*args, **kwargs):
    if DEBUGGER:
        print(*args, **kwargs)
