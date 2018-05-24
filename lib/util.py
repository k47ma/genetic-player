import math

def in_sorted(target, sorted_list):
    """Check if target is in the given sorted list"""
    for ind in range(len(sorted_list)):
        if target == sorted_list[ind]:
            return True
        elif target > ind:
            continue
        else:
            return False
    return False

def split_list(a, n):
    """Split the given list into n parts and return a list of parts"""
    part_len = len(a) / n
    parts = []
    for i in range(n):
        start_ind = i * part_len
        end_ind = (i + 1) * part_len
        if i == n - 1:
            parts.append(a[start_ind:])
        else:
            parts.append(a[start_ind:end_ind])
    return parts

def distance(a, b):
    """Calculate the distance between point a and b"""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
