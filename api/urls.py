from django.urls import path
from .views import SignupView, LoginView, GenerateDreamView, DreamHistoryView, DeleteDreamView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("generate/", GenerateDreamView.as_view(), name="generate_dream"),
    path("dreams/", DreamHistoryView.as_view(), name="dream_history"),
    path("dreams/<int:dream_id>/", DeleteDreamView.as_view(), name="delete_dream"),
]