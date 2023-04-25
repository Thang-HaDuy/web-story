from rest_framework import pagination


class StoryPaginator(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'page'

class SearchPaginator(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'page'

class ChapterPaginator(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'page'

class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'page'