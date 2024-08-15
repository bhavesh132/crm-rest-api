from django.utils.deprecation import MiddlewareMixin


class AuthTokenFromCookie(MiddlewareMixin):
    def process_request(self, request):
        if 'auth_token' in request.COOKIES:
            token = request.COOKIES['auth_token']
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
    