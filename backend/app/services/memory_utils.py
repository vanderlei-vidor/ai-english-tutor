def get_top_errors(common_errors, limit=3):

    sorted_errors = sorted(
        common_errors.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        error[0]
        for error in sorted_errors[:limit]
    ]