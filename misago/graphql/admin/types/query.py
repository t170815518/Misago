from typing import Awaitable, List

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ....loaders import load_root_categories
from ....types import Category
from ..decorators import admin_query

query_type = QueryType()


@query_type.field("categories")
@admin_query
def resolve_categories(_, info: GraphQLResolveInfo) -> Awaitable[List[Category]]:
    return load_root_categories(info.context)