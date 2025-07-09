from rest_framework.pagination import PageNumberPagination

# from foodgram.constants import MAX_LIMIT_PAGE_SIZE


class LimitPagination(PageNumberPagination):
    """Пагинация пользователей."""

    page_size_query_param = 'limit'
    max_page_size = 100

