from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Material, Test, Question, Choice,User
from .serializers import MaterialSerializer, TestSerializer, QuestionSerializer, ChoiceSerializer, UserSerializer
class UserRegisterView(APIView):
    """
    Этот класс представления обрабатывает регистрацию пользователей, принимая пользовательские данные,
    проверяя их на валидность и создавая новый экземпляр пользователя после успешной валидации.
    """

    def post(self, request):
        """
        Принимает данные пользователя, проверяет их и создает нового пользователя.

        Параметры:
            request: Объект HTTP-запроса, содержащий данные для регистрации пользователя.

        Возвращает:
            HTTP-ответ с данными только что созданного пользователя или ошибками валидации.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    """
    Этот класс обеспечивает представление списка пользователей с возможностью фильтрации.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['username', 'email'] # Поля, по которым можно фильтровать список пользователей

    def get(self, request, *args, **kwargs):
        """
        Возвращает список пользователей, с возможностью фильтрации.
        Параметры фильтрации и сортировки могут быть заданы в параметрах запроса.

        Параметры:
            request: Объект HTTP-запроса.

        Возвращает:
            HTTP-ответ со списком пользователей, отфильтрованным на основании параметров запроса.
        """
        return self.list(request, *args, **kwargs)

class MaterialViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с материалами. Поддерживается фильтрация по названию и автору.
    Доступные методы: GET, POST, PUT, PATCH, DELETE.
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title', 'section']
    # добавьте `ordering_fields` если хотите уточнить, по каким полям можно упорядочивать результаты

class TestViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с тестами. Поддерживается фильтрация по названию теста и уровню сложности.
    Доступные методы: GET, POST, PUT, PATCH, DELETE.
    """
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['material', 'title']

class QuestionViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с вопросами. Поддерживается фильтрация по названию и принадлежности к тесту.
    Доступные методы: GET, POST, PUT, PATCH, DELETE.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['text', 'test']

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с вариантами ответов. Поддерживается фильтрация по принадлежности к вопросу и корректности ответа.
    Доступные методы: GET, POST, PUT, PATCH, DELETE.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['question', 'is_correct']
