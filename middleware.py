import json
from jose import jwt
from urllib.request import urlopen
from django.conf import settings
from django.http import JsonResponse

def get_token_auth_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    if not auth:
        raise Exception("Authorization header is expected")

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise Exception("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise Exception("Token not found")
    elif len(parts) > 2:
        raise Exception("Authorization header must be Bearer token")

    token = parts[1]
    return token

def requires_auth(f):
    def decorated(request, *args, **kwargs):
        token = get_token_auth_header(request)
        jsonurl = urlopen("https://"+settings.AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=settings.AUTH0_CLIENT_ID,
                    issuer="https://"+settings.AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                return JsonResponse({'message': 'token is expired'}, status=401)
            except jwt.JWTClaimsError:
                return JsonResponse({'message': 'incorrect claims, please check the audience and issuer'}, status=401)
            except Exception:
                return JsonResponse({'message': 'Unable to parse authentication token.'}, status=401)

            request.user = payload
            return f(request, *args, **kwargs)
        return JsonResponse({'message': 'Unable to find appropriate key'}, status=401)
    return decorated