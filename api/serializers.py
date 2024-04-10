from rest_framework import serializers

from api.models import Diary, Note, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("login", "password", "username")
        read_only_fields = ("id",)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DiarySerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Diary
        fields = "__all__"
        read_only_fields = ("id",)

    def validate(self, data):
        expiration = data.get("expiration")
        kind = data.get("kind")

        if not expiration and self.instance:
            expiration = self.instance.expiration

        if expiration and kind == "PUBLIC":
            raise serializers.ValidationError(
                'The field "expiration" must be set only for PUBLIC diary'
            )
        return data

    def create(self, validated_data):
        return Diary.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            instance.save()
            return instance


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("id",)
