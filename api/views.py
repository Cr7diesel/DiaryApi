import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User, Diary, Note
from .permissions import IsOwner
from .serializers import DiarySerializer, NoteSerializer


logger = logging.getLogger(__name__)


class ReadDiaryViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DiarySerializer
    queryset = Diary.objects.select_related("user").all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("title", "expiration", "kind", "user")
    search_fields = ("title", "expiration", "kind", "user")
    pagination_class = PageNumberPagination


class DiaryView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = DiarySerializer

    def post(self, request):
        try:
            serializer = DiarySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={"New diary": serializer.data}, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            logger.exception(
                "Validation error for user.pk=%s. Error: %s", request.user.pk, str(e)
            )
            return Response(data={"Error": str(e.args)}, status=e.status_code)
        except PermissionDenied as e:
            logger.exception("Permission denied for user.pk=%s", request.user.pk)
            return Response(data={"Error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception("Error for user.pk=%s. Error: %s", request.user.pk, str(e))
            return Response(
                data={"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, **kwargs):
        try:
            diary_id = kwargs.get("diary_id")
            if not diary_id:
                return Response(
                    data={"Error": "diary_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            diary = Diary.objects.select_related("user").get(pk=diary_id)
            serializer = DiarySerializer(data=request.data, instance=diary)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={"Diary is updated": serializer.data}, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            logger.exception("User doesn't exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "user does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied as e:
            logger.exception("Permission denied for user.pk=%s", request.user.pk)
            return Response(data={"Error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Diary.DoesNotExist:
            logger.exception("Diary does not exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "diary does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            logger.exception(
                "Validation error for user.pk=%s. Error: %s", request.user.pk, str(e)
            )
            return Response(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error for user.pk=%s. Error: %s", request.user.pk, str(e))
            return Response(
                data={"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, **kwargs):
        try:
            diary_id = kwargs.get("diary_id")
            if not diary_id:
                return Response(
                    data={"Error": "diary_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            diary = Diary.objects.select_related("user").get(pk=diary_id)
            diary.delete()
            return Response(
                data={"Message": "Successfully deleted item"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except User.DoesNotExist:
            logger.exception("User doesn't exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "user does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied as e:
            logger.exception("Permission denied for user.pk=%s", request.user.pk)
            return Response(data={"Error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Diary.DoesNotExist:
            logger.exception("Diary does not exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "diary does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            logger.exception(
                "Validation error for user.pk=%s. Error: %s", request.user.pk, str(e)
            )
            return Response(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error for user.pk=%s. Error: %s", request.user.pk, str(e))
            return Response(
                data={"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReadNoteViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer
    queryset = Note.objects.select_related("user", "diary").all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("text", "diary")
    search_fields = ("text", "diary")
    pagination_class = PageNumberPagination


class NoteView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = NoteSerializer

    def post(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={"New Note": serializer.data}, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            logger.exception(
                "Validation error for user.pk=%s. Error: %s", request.user.pk, str(e)
            )
            return Response(data={"Error": str(e.args)}, status=e.status_code)
        except PermissionDenied as e:
            logger.exception("Permission denied for user.pk=%s", request.user.pk)
            return Response(data={"Error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception("Error for user.pk=%s. Error: %s", request.user.pk, str(e))
            return Response(
                data={"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, **kwargs):
        try:
            note_id = kwargs.get("note_id")
            if not note_id:
                return Response(
                    data={"Error": "note_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            note = Note.objects.select_related("user", "diary").get(pk=note_id)
            serializer = NoteSerializer(data=request.data, instance=note)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={"Note is updated": serializer.data}, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            logger.exception("User doesn't exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied as e:
            logger.exception("Permission denied for user.pk=%s", request.user.pk)
            return Response(data={"Error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            logger.exception("Note does not exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "Note does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            logger.exception(
                "Validation error for user.pk=%s. Error: %s", request.user.pk, str(e)
            )
            return Response(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error for user.pk=%s. Error: %s", request.user.pk, str(e))
            return Response(
                data={"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, **kwargs):
        try:
            note_id = kwargs.get("note_id")
            if not note_id:
                return Response(
                    data={"Error": "note_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            note = Note.objects.select_related("user", "diary").get(pk=note_id)
            note.delete()
            return Response(
                data={"Message": "Successfully deleted Note"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except User.DoesNotExist:
            logger.exception("User doesn't exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied as e:
            logger.exception("Permission denied for user.pk=%s", request.user.pk)
            return Response(data={"Error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            logger.exception("Note does not exist. user.pk=%s", request.user.pk)
            return Response(
                data={"Error": "Note does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            logger.exception(
                "Validation error for user.pk=%s. Error: %s", request.user.pk, str(e)
            )
            return Response(data={"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error for user.pk=%s. Error: %s", request.user.pk, str(e))
            return Response(
                data={"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
