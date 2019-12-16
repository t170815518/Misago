import pytest

from ..query import resolve_auth, resolve_categories, resolve_category, resolve_settings


@pytest.mark.asyncio
async def test_auth_resolver_returns_authenticated_user(user_graphql_info, user):
    value = await resolve_auth(None, user_graphql_info)
    assert value == user


@pytest.mark.asyncio
async def test_auth_resolver_returns_none_if_no_user_is_authenticated(graphql_info):
    value = await resolve_auth(None, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_categories_resolver_returns_list_of_top_categories(
    category, child_category, graphql_info
):
    value = await resolve_categories(None, graphql_info)
    assert category in value
    assert child_category not in value


@pytest.mark.asyncio
async def test_category_resolver_returns_category_by_id(category, graphql_info):
    value = await resolve_category(None, graphql_info, id=category.id)
    assert value == category


@pytest.mark.asyncio
async def test_category_resolver_returns_none_for_nonexistant_category_id(graphql_info):
    value = await resolve_category(None, graphql_info, id=100)
    assert value is None


def test_settings_resolver_returns_settings_from_context(
    graphql_info, dynamic_settings
):
    value = resolve_settings(None, graphql_info)
    assert value is dynamic_settings
