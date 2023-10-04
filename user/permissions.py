from rest_framework.permissions import BasePermission


class IsSuperUserOrReadOnly(BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        id_in_url = view.kwargs.get("pk")
        print("id in url", id_in_url)
        # Seul le super utilisateur peut accéder à la liste des utilisateurs, au détail d'un utilisateur,
        # créer, modifier ou supprimer un utilisateur
        if request.user.is_superuser:
            return True

        if id_in_url is not None and request.user.is_authenticated:
            print("EditMethod")
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            print("PermAuteursuperuser")
            return True

        # un utilisateur peut lire, modifier ou supprimer ses données
        # conformément au RGPD (droit à l’accès et à la rectification et droit à l'oubli)
        if obj == request.user:
            print("permAuteurObjAuthor", obj, "request.user: ", request.user)
            return True

        return False
