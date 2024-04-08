from rest_framework import serializers

from api.models import Diary, Note, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id",)


class DiarySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Diary
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        return Diary.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            instance.save()
            return instance


class NoteSerializer(serializers.ModelSerializer):
    diary = DiarySerializer(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("id",)
