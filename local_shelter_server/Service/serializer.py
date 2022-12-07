from rest_framework import serializers
from Updator.models import Content_Description, Community, Shelter_media, Content, Comment_media, Comment, Issue_Board

class Content_Description_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Content_Description
        fields = ('id', 'upload_file', 'description', 'width', 'height', 'HVType', 'thumbnailPath', 'contentFK')


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ('id', 'name', 'createDate','lastEditDate','isUpdate','community_status','shelterFK')

class Shelter_media_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter_media
        fields = ('id', 'shelter_profile', 'contentQR', 'communityQR', 'shelterFK')

class Content_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        # fields = ('id', 'title', 'email', 'email', 'content_status', 'contentType',)
        fields =  '__all__'

class CommunityMedia_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_media
        fields = '__all__'

class CommunityComment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class Issue_Board_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Issue_Board
        fields = '__all__'