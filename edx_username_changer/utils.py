"""
Utility methods for edx-username-changer plugin
"""

from django.contrib.auth import get_user_model
from django.db import transaction

from social_django.models import UserSocialAuth  # pylint: disable=import-error

from common.djangoapps.student.models import (  # pylint: disable=import-error
    CourseEnrollment,
)
from openedx.core.djangoapps.django_comment_common.comment_client.utils import (  # pylint: disable=import-error
    perform_request as perform_forum_request,
)
from openedx.core.djangoapps.django_comment_common.comment_client.thread import (  # pylint: disable=import-error
    Thread,
)
from openedx.core.djangoapps.django_comment_common.comment_client.comment import (  # pylint: disable=import-error
    Comment,
)

from edx_username_changer.exceptions import UpdateFailedException


User = get_user_model()


def update_user_social_auth_uid(old_username, new_username):
    """
    Changes uid in django-social-auth for OAuth based user accounts
    iff uid is based on username otherwise it doesn't make any effect
    """
    with transaction.atomic():
        UserSocialAuth.objects.filter(uid=old_username).update(uid=new_username)


def get_enrolled_course_ids(user):
    """
    Returns course ids of all the active enrollments of the provided user
    """
    return [
        str(enrollment.course_id)
        for enrollment in CourseEnrollment.enrollments_for_user(user)
    ]


def get_authored_threads_and_comments(comment_user, course_ids):
    """
    Returns an iterator of all the discussion-forum threads and comments of provided user and course
    """
    for course_id in course_ids:
        involved_threads = [
            Thread.find(id=thread["id"]).retrieve(
                with_responses=True, recursive=True, mark_as_read=False
            )
            for thread in Thread.search(
                {"course_id": course_id, "user_id": comment_user.id}
            ).collection
        ]
        for thread in involved_threads:
            if thread["user_id"] == comment_user.id:
                yield thread.to_dict()
            children_to_scan = thread["children"]
            while children_to_scan:
                child = children_to_scan.pop(0)
                children_to_scan.extend(child["children"])
                if child["user_id"] == comment_user.id:
                    yield child


def update_comment_user_username(comment_user, new_username):
    """
    Updates username for discussion-forum comment-users via Forum APIs
    """
    user_detail_url = comment_user.url_with_id(params={"id": comment_user.id})
    response_data = perform_forum_request(
        "put",
        user_detail_url,
        data_or_params={u"username": new_username},
    )
    if response_data[u"username"] != new_username:
        raise UpdateFailedException(url=user_detail_url, new_username=new_username)


def update_thread_username(thread_id, new_username):
    """
    Updates username for discussion-forum threads via Forum APIs
    """
    thread_detail_url = Thread.url_with_id(params={"id": thread_id})
    response_data = perform_forum_request(
        "put",
        thread_detail_url,
        data_or_params={u"username": new_username},
    )
    if response_data[u"username"] != new_username:
        raise UpdateFailedException(url=thread_detail_url, new_username=new_username)


def update_comment_username(comment_id, new_username):
    """
    Updates username for discussion-forum comments via Forum APIs
    """
    comment_detail_url = Comment.url_for_comments(params={"parent_id": comment_id})
    response_data = perform_forum_request(
        "put",
        comment_detail_url,
        data_or_params={u"username": new_username},
    )
    if response_data[u"username"] != new_username:
        raise UpdateFailedException(url=comment_detail_url, new_username=new_username)
