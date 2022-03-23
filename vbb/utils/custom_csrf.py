from rest_framework.authentication import SessionAuthentication


class CsrfHTTPOnlySessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        # reference: https://stackoverflow.com/questions/30871033/django-rest-framework-remove-csrf
        # TODO check that the httponly csrf cookie is valid
        return  # To not perform the csrf check previously happening
