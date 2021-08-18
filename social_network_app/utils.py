def like_analytics(serializer):
    likes_per_day = {}
    for el in serializer.data:
        k = el['created_at'][:10]
        likes_per_day[k] = []
    for el in serializer.data:
        k = el['created_at'][:10]
        if k in likes_per_day:
            likes_per_day[k].append(el)
    response = {
        'total_likes': len(serializer.data),
        'likes_per_day': likes_per_day
    }

    return response
