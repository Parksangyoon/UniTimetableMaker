from django_tables2 import RequestConfig

PER_PAGE = 100


def request_table_config(request, table):
    # sort by field
    RequestConfig(request).configure(table)
    # paginate
    RequestConfig(request, paginate={'per_page': PER_PAGE}).configure(table)
