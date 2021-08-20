def like_analytics(serializer):
    """This function creates from serializer's data a dict which keys are dates
    and values are amount of likes.
    """
    likes_per_day = {}
    for data in serializer.data:
        k = data['created_at'][:10]
        likes_per_day[k] = 0
    for data in serializer.data:
        k = data['created_at'][:10]
        if k in likes_per_day:
            likes_per_day[k] += 1
    response = {
        'total_likes': len(serializer.data),
        'likes_per_day': likes_per_day
    }

    return response
