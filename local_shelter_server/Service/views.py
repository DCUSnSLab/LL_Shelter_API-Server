import os.path

import os

from django.shortcuts import render, redirect

from Updator.models import Shelter, Shelter_media, Content, Content_Description, \
    Advertisement, Advertisement_media, Comment, Comment_media, \
    Community, Daily_Board, Issue_Board

from Service.models import Drawing

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from Service.serializer import Content_Description_Serializer, CommunitySerializer, Shelter_media_Serializer, Content_Serializer, CommunityMedia_Serializer, CommunityComment_Serializer, Issue_Board_Serializer
from Updator.models import Content_Description, Community, Shelter_media, Content


from django.core.serializers.json import DjangoJSONEncoder

from datetime import datetime
import json, base64, io
from PIL import Image
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = Path(__file__).resolve().parent.parent

class IssueBoardAPI(APIView):
    arser_classes = (MultiPartParser, FormParser)

    def get(request, *args, **kwargs):
        issuelist = Issue_Board.objects.all()
        serializer = Issue_Board_Serializer(issuelist, many=True)
        return Response(serializer.data)

class CommunityCommentAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(request, *args, **kwargs):
        media = Comment.objects.all()
        serializer = CommunityComment_Serializer(media, many=True)
        return Response(serializer.data)

class commentMediaAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(request, *args, **kwargs):
        media = Comment_media.objects.all()
        serializer = CommunityMedia_Serializer(media, many=True)
        return Response(serializer.data)

class ContentViewAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):

        # sort_by use Content_Detail tables column.
        sort_by = request.GET.get('sort_by')
        order = request.GET.get('order')

        content = Content_Description.objects.all().select_related('contentFK')

        if sort_by:
            if order == 'ascend':
                content = Content_Description.objects.all().order_by('contentFK__' + sort_by)
                # content = Content_Description.objects.all().select_related('contentFK').order_by('hits')
            else:
                content = Content_Description.objects.all().order_by('-contentFK__' + sort_by)
                # content = Content_Description.objects.all().select_related('contentFK').order_by('-hits')

        for instance in content:
            instance.contentFK.hits = int(instance.contentFK.hits)
            instance.contentFK.likes = int(instance.contentFK.likes)
            instance.save()

        serializer = Content_Description_Serializer(content, many=True)
        return Response(serializer.data)

def Idle(request):

    # print("Idle Page")

    return render(request, 'Service/Idle.html')

# class ContenViewSet(viewsets.ModelViewSet):
#     queryset = Content_Description.objects.all()
#     serializer_class = Content_Description_Serializer
class SignageViewAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(request, *args, **kwargs):
        posts = Content_Description.objects.all().order_by('id')
        serializer = Content_Description_Serializer(posts, many=True)
        return Response(serializer.data)

        # print("signageView")
        #     img_list = Content.objects.filter(contentType='Image')

            # img_description = None
            # for idx, img in enumerate(img_list):
            #
            #     img_description = Content_Description.objects.get(contentFK=img)
            #     img.upload_file = img_description.upload_file
            #
            # vod_list = Content.objects.filter(contentType='Video')
            #
            # vod_description = None
            # for idx, vod in enumerate(vod_list):
            #
            #     vod_description = Content_Description.objects.get(contentFK=vod)
            #     vod.upload_file = vod_description.upload_file
            #     vod.thumbnailPath = vod_description.thumbnailPath

            # thumbnail_list = Content_Description.objects.exclude(thumbnailPath=None).values('thumbnailPath')

            # 업로드 이미지는 익명성이 있어 업로더를 파악할 수 없음
            # 이전 구현 내용 경우 업로드의 사용자명과 별명 등을 표기했으나 변경된 기능에서는 필요없음

            # for idx, img in enumerate(img_list):
            #
            #     usernickname = CustomUser.objects.get(user_id=img.userFK_id)
            #     img.nickname = usernickname.nickname

            # for idx, vod in enumerate(vod_list):
            #     # print("vod {0}".format(vod))
            #     vod.thumbnail = thumbnail_list[idx]['thumbnailPath']
            #     # usernickname = CustomUser.objects.get(user_id=vod.userFK_id)
            #     # vod.nickname = usernickname.nickname

            # with open('./ShelterInfo/shelter_info.json', 'r') as f:
            #     json_data = json.load(f)
            #
            # shelter_id = json_data['shelter_id']
            #
            # contentQR = Shelter_media.objects.filter(id=shelter_id).values_list('contentQR')
            #
            # print("111", contentQR[0][0])
            # context = {
            #     "img_list": img_list,
            #     "vod_list": vod_list,
            #     "contentQR": contentQR[0][0]
            # }

            # return render(request, 'Service/signageShow.html', context)

def contentDetailView(request, id):

    content = Content.objects.get(id=id)
    print(type(content))
    # cont_user_id = Content.objects.filter(id=id).values("userFK")
    # description_user = CustomUser.objects.filter(user__in=cont_user_id).values('user_description')
    # user_img = CustomUser.objects.filter(user__in=cont_user_id).values('user_profile')

    description = Content_Description.objects.get(contentFK=content)
    print(type(description))
    # theme_list = Theme.objects.all()

    content.hits += 1
    content.save()

    # c = Content.objects.filter(id=id).values("theme_id")
    # contents_in_theme = Theme.objects.get(id__in=c)
    # contents_in_themeValue = contents_in_theme.themeValue

    # nickname = CustomUser.objects.get(user_id=contents.userFK_id)
    # contents.nickname = nickname

    # 미디어 스트리밍 추가 예정
    # content2server = list(Content.objects.filter(id=id).values('id', 'title', 'upload_file'))

    # context = {
    #     "contents_info": contents,
    #     "description_info": description,
    #     'theme_list': theme_list,
    #     'contents_in_themeValue': contents_in_themeValue,
    #     'description_user': description_user,
    #     'content2server': content2server,
    #     'user_img': user_img,
    #     # 'user_list': user_list,
    # }

    # print("c", content)
    # print("d", description)

    context = {
        "content_info": content,
        "description_info": description,

        # 'content2server': content2server,
    }

    return render(request, 'Service/contentDetailView.html', context)

@api_view(['GET', 'POST'])
def ContentLike(request, id):
    print("contents like")

    contents = Content.objects.get(id=id)

    contents.likes += 1
    contents.save()

    # return Response({'Success'})
    return Response({'like': int(contents.likes)})
    # return redirect('display:picture', contents.id)

@api_view(['GET', 'POST'])
def ContentHits(request, id):
    print("contents hits")

    contents = Content.objects.get(id=id)

    contents.hits += 1
    contents.save()

    # return Response({'Success'})
    return Response({'hits': int(contents.hits)})

def VODLike(request, id):
    print("VODLike ")

    contents = Content.objects.get(id=id)

    contents.likes += 1
    contents.save()

    return redirect('display:media', contents.id)

# 커뮤니티 메인 게시판
class CommunityViewAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(request, *args, **kwargs):
        comment = Community.objects.all()
        serializer = CommunitySerializer(comment, many=True)
        return Response(serializer.data)

    # def get(requste, *args, **kwargs):
    #     with open('./ShelterInfo/shelter_info.json', 'r') as f:
    #         json_data = json.load(f)
    #     shelter_id = json_data['shelter_id']
    #     communityQR = Shelter_media.objects.filter(id=shelter_id).values_list('communityQR')
    #     communityQR: communityQR[0][0]
    #     serializer = Shelter_media_Serializer(shelter_id, communityQR, many=True)
    #     return Response(serializer.data)


    def community(request):
        print("community")

        with open('./ShelterInfo/shelter_info.json', 'r') as f:
            json_data = json.load(f)

        shelter_id = json_data['shelter_id']

        communityQR = Shelter_media.objects.filter(id=shelter_id).values_list('communityQR')

        context = {

            "communityQR": communityQR[0][0]
        }


        return render(request, 'Service/community.html', context)

def IssueBoard(request):
    # UI 디자인 제외, 댓글 출력만 하기

    with open('./ShelterInfo/shelter_info.json', 'r') as f:
        json_data = json.load(f)

    print("json", json_data['shelter_id'])

    shelter_id = json_data['shelter_id']

    community_id = shelter_id

    community = Community.objects.filter(id=community_id).values_list('id')

    board = Issue_Board.objects.filter(id=community[0][0]).values_list('id')

    comments = Comment.objects.filter(iboardFK=board[0][0])

    comments_media = None
    for idx, comment in enumerate(comments):
        comments_media = Comment_media.objects.get(commentFK=comment)
        comment.image = comments_media.image

    context = {
        'comments': comments
    }

    return render(request, 'Service/IssueBoard.html', context)

def DailyBoard(request):
    # UI 디자인 제외, 댓글 출력만 하기

    with open('./ShelterInfo/shelter_info.json', 'r') as f:
        json_data = json.load(f)

    print("json", json_data['shelter_id'])

    shelter_id = json_data['shelter_id']

    community_id = shelter_id

    community = Community.objects.filter(id=community_id).values_list('id')

    board = Daily_Board.objects.filter(id=community[0][0]).values_list('id')

    comments = Comment.objects.filter(dboardFK=board[0][0])

    comments_media = None
    for idx, comment in enumerate(comments):
        comments_media = Comment_media.objects.get(commentFK=comment)
        comment.image = comments_media.image

    context = {
        'comments': comments,
    }

    return render(request, 'Service/DailyBoard.html', context)

# 그림판
def paint(request):

    ip_address = os.environ['CMS_SHELTER_IP']

    context = {
        'Ipaddr': ip_address,
    }

    return render(request, 'Service/paint.html', context)

@csrf_exempt
def paintlist(request):

    picture = Drawing()
    getPicture = Drawing.objects.all()
    print("getPicture", getPicture)

    if request.method == 'POST':
        # print(json.loads(request.body))
        requestImg = json.loads(request.body)
        byteImg = bytes(requestImg['imgBase64'], 'utf-8')
        imgDecode = base64.b64decode(byteImg)
        image = Image.open(io.BytesIO(imgDecode))
        filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
        # imagePath = './media/community/drawing/{0}.png'.format(filename1)

        pictureDir = os.path.join(BASE_DIR, 'media/community/drawing')
        print("pictureDir", pictureDir)

        # 디렉토리 존재 여부 확인
        flag = os.path.isdir(pictureDir)
        if flag == True:
            print("경로있다")
        else:
            os.makedirs(pictureDir)
            print("경로없다")

        imagePath = os.path.join(BASE_DIR, 'media/community/drawing/{0}.png'.format(filename1))
        image.save(imagePath, 'png')

        savePath = 'media/community/drawing/{0}.png'.format(filename1)
        picture.path = savePath
        picture.save()

    ip_address = os.environ['CMS_SHELTER_IP']

    context = {
        'Picture': getPicture,
        'Ipaddr': ip_address,
    }

    return render(request, 'Service/paintlist.html', context)

def ViewPaint(request, id):

    ip_address = os.environ['CMS_SHELTER_IP']

    print("ViewPaint")

    pic = Drawing.objects.get(id=id)

    context = {
        'Picture': pic,
        'Ipaddr': ip_address,
    }

    return render(request, 'Service/ViewPaint.html', context)
