from typing import Optional, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt

from ....auth import get_authenticated_user
from ....validation import (
    UserExistsValidator,
    validate_data,
    validate_model,
)
from ....threads.delete import delete_user_posts, delete_user_threads
from ....users.errors import CantDeleteSelfError, UserIsProtectedError
from ....users.hooks.deleteuser import delete_user_hook
from ....users.hooks.deleteusercontent import delete_user_content_hook
from ....users.models import User
from ... import GraphQLContext
from ...errorhandler import error_handler
from ..decorators import admin_mutation

delete_user_mutation = MutationType()


@delete_user_mutation.field("deleteUser")
@error_handler
@admin_mutation
@convert_kwargs_to_snake_case
async def resolve_delete_user(
    _,
    info: GraphQLResolveInfo,
    *,
    user: str,
    delete_content: Optional[bool] = False,
):
    input_data = {
        "user": user,
        "delete_content": delete_content,
    }

    cleaned_data, errors = validate_model(DeleteUserInputModel, input_data)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {
            "user": [
                UserExistsValidator(info.context),
                user_can_be_deleted_validator(info.context),
            ],
        },
        errors,
    )

    if errors:
        return {"errors": errors, "deleted": False}

    if delete_content:

        async def delete_user_content(user, *args, **kwargs):
            await delete_user_threads(user)
            await delete_user_posts(user)

        await delete_user_content_hook.call_action(
            delete_user_content, cleaned_data["user"], context=info.context
        )

    def delete_user(user, *args, **kwargs):
        return cleaned_data["user"].delete()

    await delete_user_hook.call_action(
        delete_user, cleaned_data["user"], context=info.context
    )

    return {"deleted": True}


class DeleteUserInputModel(BaseModel):  # type: ignore
    user: PositiveInt
    delete_content: bool


def user_can_be_deleted_validator(context: GraphQLContext):
    async def validate_delete_user(user: User, errors, field_name):
        context_user = cast(User, await get_authenticated_user(context))
        if user.id == context_user.id:
            raise CantDeleteSelfError()
        if user.is_administrator:
            raise UserIsProtectedError(user_id=user.id)

        return user

    return validate_delete_user