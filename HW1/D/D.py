def solution(total):
    hours = total // 60
    minutes = total % 60
    if hours >= 24:
        hours = hours % 24
    if minutes == 0:
        minutes = "00"
    result = f"{hours} {minutes}"
    return result
