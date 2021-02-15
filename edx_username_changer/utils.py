"""
Utility methods for edx-username-changer plugin
"""

from django.contrib.auth import get_user_model
from django.db import transaction

from social_django.models import UserSocialAuth

from common.djangoapps.student.models import CourseEnrollment
from openedx.core.djangoapps.django_comment_common.comment_client.utils import perform_request as perform_forum_request
from openedx.core.djangoapps.django_comment_common.comment_client.user import User as CommentUser
from openedx.core.djangoapps.django_comment_common.comment_client.thread import Thread
from openedx.core.djangoapps.django_comment_common.comment_client.comment import Comment

from edx_username_changer.exceptions import UpdateFailedException


User = get_user_model()
COMMENT_TYPE = "comment"
THREAD_TYPE = "thread"


class EdxUsernameChanger():
    """
    Execeptions for edx-username-changer plugin
    """
    def __init__(self, old_username, new_username):
        self.old_username = old_username
        self.new_username = new_username

    def update_username_in_forum(self):
        """
        Changes username in Discussion-Forum service
        """
        user = User.objects.get(username=self.new_username)
        comment_user = CommentUser.from_django_user(user)
        update_comment_user_username(comment_user, self.new_username)
        enrolled_course_ids = get_enrolled_course_ids(user)
        authored_items = get_authored_threads_and_comments(comment_user, enrolled_course_ids)

        for authored_item in authored_items:
            item_id = authored_item["id"]
            item_type = str(authored_item.get("type"))
            if item_type == THREAD_TYPE:
                update_thread_username(item_id, self.new_username)
            elif item_type == COMMENT_TYPE:
                update_comment_username(item_id, self.new_username)

    def update_user_social_auth_uid(self):
        """
        Changes uid in django-social-auth for oauth based user accounts
        iff uid is based upon username else doesn't make any effect
        """
        with transaction.atomic():
            UserSocialAuth.objects.filter(uid=self.old_username).update(uid=self.new_username)


def get_enrolled_course_ids(user):
    """
    Returns course ids of all the active enrollments of the provided user
    """
    return [
        str(enrollment.course_id)
        for enrollment in CourseEnrollment.enrollments_for_user(user)
        if enrollment.is_active is True
    ]


def get_authored_threads_and_comments(comment_user, course_ids):
    """
    Returns an iterator of all the discussion-forum threads and comments of provided user and course
    """
    for course_id in course_ids:
        involved_threads = [
            Thread.find(id=thread["id"]).retrieve(with_responses=True, recursive=True, mark_as_read=False)
            for thread in Thread.search({"course_id": course_id, "user_id": comment_user.id}).collection
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



