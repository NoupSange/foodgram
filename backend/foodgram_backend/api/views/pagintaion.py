from rest_framework.pagination import PageNumberPagination


class LimitPagination(PageNumberPagination):
    """Пагинация пользователей."""

    page_size_query_param = 'limit'
    max_page_size = 100
