#coding: utf-8

from django.contrib.auth.models import Group, Permission


def isModels(user):

    if user.is_active:
        return ['all']

    permissions = Permission.objects.raw(u"""
        SELECT
            *
        FROM
            `auth_permission`
            INNER JOIN `auth_user_user_permissions` ON (`auth_permission`.`id` = `auth_user_user_permissions`.`permission_id`)
            INNER JOIN `django_content_type` ON (`auth_permission`.`content_type_id` = `django_content_type`.`id`)
        WHERE
            (`auth_user_user_permissions`.`user_id` = %s )
    """, [user.id])

    list = []

    if permissions:
        for permission in permissions:
            list.append(permission.codename)

    groups = Group.objects.raw(u"""
        SELECT
            *
        FROM
            `auth_group`
            INNER JOIN `auth_user_groups` ON (`auth_group`.`id` = `auth_user_groups`.`group_id`)
            INNER JOIN `auth_group_permissions` ON (`auth_group`.`id` = `auth_group_permissions`.`group_id`)
            INNER JOIN `auth_permission` ON (`auth_group_permissions`.`permission_id` = `auth_permission`.`id`)
            INNER JOIN `django_content_type` ON (`auth_permission`.`content_type_id` = `django_content_type`.`id`)
        WHERE
            (`auth_user_groups`.`user_id` = %s )
    """, [user.id])

    if groups:
        for group in groups:
            list.append(group.codename)

    return False if len(list) == 0 else list

