from rest_access_policy import AccessPolicy


class PostAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["list", "retrieve"], "principal": "*", "effect": "allow"},
        {
            "action": ["create", "like", "unlike", "delete_reaction"],
            "principal": "authenticated",
            "effect": "allow",
        },
    ]


class LikeAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        }
    ]
