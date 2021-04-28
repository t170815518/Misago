from typing import List, Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ..types import ParsedMarkupMetadata


class MarkdownAction(Protocol):
    def __call__(
        self, context: GraphQLContext, markup: str, metadata: ParsedMarkupMetadata
    ) -> List[dict]:
        ...


class MarkdownFilter(Protocol):
    def __call__(
        self,
        action: MarkdownAction,
        context: GraphQLContext,
        markup: str,
        metadata: ParsedMarkupMetadata,
    ) -> List[dict]:
        ...


class MarkdownHook(FilterHook[MarkdownAction, MarkdownFilter]):
    is_async = False

    def call_action(
        self,
        action: MarkdownAction,
        context: GraphQLContext,
        markup: str,
        metadata: ParsedMarkupMetadata,
    ) -> List[dict]:
        return self.filter(action, context, markup, metadata)


markdown_hook = MarkdownHook()