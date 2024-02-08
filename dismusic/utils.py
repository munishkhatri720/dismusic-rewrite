def format_millisecond(duration_ms : int)-> str:
    seconds, milliseconds = divmod(duration_ms, 1000)
    minutes, seconds = divmod( seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        time_format = f"{hours}:{minutes:02}:{seconds:02}"
    else:
        time_format = f"{minutes}:{seconds:02}"
    return time_format