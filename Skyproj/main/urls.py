from django.urls import path, include
from rest_framework import routers
from .views import UserRegisterView, MaterialViewSet, TestViewSet, QuestionViewSet, ChoiceViewSet

router = routers.DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('', include(router.urls)),
]