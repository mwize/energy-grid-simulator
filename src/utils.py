def clamp(n, smallest, largest):
    """helper function to clamp n between smallest and largest"""
    return max(smallest, min(n, largest))