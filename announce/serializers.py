from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Announce, AnnounceImage, AnnounceFile, Comment


# Serializer for the Announce model
class AnnounceSerializer(serializers.ModelSerializer):
    # Return the computed number of readers as a read-only field
    number_of_reader = serializers.IntegerField(
        source="number_of_reader", read_only=True
    )
    # Return the list of readers' usernames for better readability
    reads = serializers.SerializerMethodField()
    # Represent author using its string representation (username)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Announce
        fields = [
            "id",
            "is_type",
            "status",
            "author",
            "title",
            "detail",
            "created_at",
            "updated_at",
            "is_delete",
            "reads",
            "number_of_reader",
        ]

    def get_reads(self, obj):
        """
        Returns a list of usernames for the readers associated with the announce.
        """
        return [user.username for user in obj.reads.all()]


# Serializer for the AnnounceImage model
class AnnounceImageSerializer(serializers.ModelSerializer):
    # Represent the linked announce using its string representation.
    announce = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AnnounceImage
        fields = ["id", "announce", "images"]


# Serializer for the AnnounceFile model
class AnnounceFileSerializer(serializers.ModelSerializer):
    announce = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AnnounceFile
        fields = ["id", "announce", "files"]


# Serializer for the Comment model
class CommentSerializer(serializers.ModelSerializer):
    # Represent both author and announce as strings for clarity.
    author = serializers.StringRelatedField(read_only=True)
    announce = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "announce", "author", "comment", "created_at"]
