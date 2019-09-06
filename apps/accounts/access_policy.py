from rest_access_policy import AccessPolicy


class UserAccessPolicy(AccessPolicy):
    statements = [{"action": ["create"], "principal": "anonymous", "effect": "allow"}]
