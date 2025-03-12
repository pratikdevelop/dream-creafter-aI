


'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Dream
from .ai_model import dream_generator

# Signup View
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        
        if not username or not password or not email:
            return Response({"error": "All fields are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username}, status=201)

# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username}, status=200)
        return Response({"error": "Invalid credentials"}, status=401)

# Existing Dream Generation View
class GenerateDreamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt required"}, status=400)
        output = dream_generator.generate_dream(prompt)
        dream = Dream(user=request.user, prompt=prompt, output=output)
        dream.save()
        return Response({"dream": output, "id": dream.id})

# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Dream
from .ai_model import dream_generator

# Signup View
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        
        if not username or not password or not email:
            return Response({"error": "All fields are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username}, status=201)

# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username}, status=200)
        return Response({"error": "Invalid credentials"}, status=401)

# Dream Generation View (HTTP-only)
class GenerateDreamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user)
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt required"}, status=400)
        output = dream_generator.generate_dream(prompt)
        dream = Dream(user=request.user, text=prompt, output=output)
        dream.save()
        return Response({"dream": output, "id": dream.id})
'''


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from .models import Dream
# from .ai_model import dream_generator

# # Existing Views (Signup, Login, GenerateDream)
# class SignupView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         email = request.data.get("email")
#         if not username or not password or not email:
#             return Response({"error": "All fields are required"}, status=400)
#         if User.objects.filter(username=username).exists():
#             return Response({"error": "Username already exists"}, status=400)
#         user = User.objects.create_user(username=username, email=email, password=password)
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key, "username": user.username}, status=201)

# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         if not username or not password:
#             return Response({"error": "Username and password required"}, status=400)
#         user = authenticate(username=username, password=password)
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key, "username": user.username}, status=200)
#         return Response({"error": "Invalid credentials"}, status=401)

# class GenerateDreamView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         prompt = request.data.get("prompt")
#         if not prompt:
#             return Response({"error": "Prompt required"}, status=400)
#         output = dream_generator.generate_dream(prompt)
#         dream = Dream(user=request.user, text=prompt, output=output)
#         dream.save()
#         return Response({"dream": output, "id": dream.id})

# # New Dream History View
# class DreamHistoryView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         dreams = Dream.objects.filter(user=request.user).order_by('-created_at')
#         dream_data = [
#             {"id": dream.id, "text": dream.text, "output": dream.output, "created_at": dream.created_at}
#             for dream in dreams
#         ]
#         return Response(dream_data)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Dream
from .ai_model import dream_generator

# Existing Views (Signup, Login, GenerateDream, DreamHistory)
class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if not username or not password or not email:
            return Response({"error": "All fields are required"}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username}, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username}, status=200)
        return Response({"error": "Invalid credentials"}, status=401)

class GenerateDreamView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        prompt = request.data.get("prompt")
        style = request.data.get("style", "default")  # New: Accept style parameter
        if not prompt:
            return Response({"error": "Prompt required"}, status=400)
        output = dream_generator.generate_dream(prompt, style=style)  # Pass style to generator
        dream = Dream(user=request.user, text=prompt, output=output)
        dream.save()
        return Response({"dream": output, "id": dream.id})

class DreamHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        per_page = 5  # Dreams per page
        dreams = Dream.objects.filter(user=request.user).order_by('-created_at')
        total = dreams.count()
        start = (page - 1) * per_page
        end = start + per_page
        paginated_dreams = dreams[start:end]
        dream_data = [
            {"id": dream.id, "prompt": dream.text, "output": dream.output, "created_at": dream.created_at}
            for dream in paginated_dreams
        ]
        return Response({
            "dreams": dream_data,
            "total": total,
            "page": page,
            "per_page": per_page
        })

# New Delete Dream View
class DeleteDreamView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, dream_id):
        dream = get_object_or_404(Dream, id=dream_id, user=request.user)
        dream.delete()
        return Response({"message": "Dream deleted"}, status=204)