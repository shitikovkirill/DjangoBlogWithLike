from rest_access_policy import AccessPolicy


class PostAccessPolicy(AccessPolicy):
    statements = [{"action": ["*"], "principal": "*", "effect": "allow"}]


class LikeAccessPolicy(AccessPolicy):
    statements = [{"action": ["*"], "principal": "*", "effect": "allow"}]
