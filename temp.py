    path("Khands/list/", views.KhandsStarListView.as_view()),
    path('Khands/search/', views.KhandsStarSearch.as_view()),  # 搜尋使用者
    path("Khands/update/", views.KhandsStarUpdateView.as_view()),  # 新興創作者 - 更新
    path('Khands/updategroup/', views.KhandsStarUpdateGroupView.as_view()),  # 更新Khands名單
    path('Khands/updatesingle/', views.KhandsStarUpdateSingleView.as_view()), # 更新單筆khands
    path('Khands/delete/', views.KhandsStarDeleteView.as_view()),  # 刪除單筆新星推薦
    path('stream/shiftCreate/', views.NotStreamShiftCreateView.as_view()), # 直播推薦(StreamShiftTable) - 上方新增
    path('stream/shiftList/', views.NotStreamShiftListView.as_view()), # 直播推薦(StreamShiftTable) - 上方列表
    path("stream/list/", views.RecommendAnchorView.as_view()),  # 直播推薦(StreamShiftTable) - 列表
    path('stream/create/', views.StreamCreateSingleView.as_view()),  # 單筆直播推薦(StreamShiftTable) - 新增
    path('stream/update/<int:pk>/', views.StreamUpdateView.as_view()),  # 單筆直播推薦(StreamShiftTable) - 編輯
    path('stream/delete/<int:pk>/', views.StreamDeleteView.as_view()),  # 單筆直播推薦(StreamShiftTable) - 刪除
]

class KhandsStarDeleteView(APIView):
    """ 刪除單筆khands """
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            obj = KhandsStar.objects.get(user_id=data['user_id'])
        except KhandsStar.DoesNotExist:
            return Response({'code': 4442, 'data': '找不到帳號'}, status=status.HTTP_200_OK)
        obj.delete()
        return Response({'code': 0, 'data': '完成刪除'}, status=status.HTTP_200_OK)


class StreamCreateSingleView(APIView):
    """ 新增單筆stream """
    # permission_classes = []
    # authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
        except:
            return Response({'code': 1, 'data': None})

        object, create =  StreamShiftTable.objects.get_or_create(user_id=user.id, link=request.data['link'], type=request.data['type'])
        if create:
            return Response({'code':0, 'data':'成功創建'}, status=status.HTTP_200_OK)
        return Response({'code': 1, 'data': '此人已存在'}, status=status.HTTP_200_OK)


class StreamUpdateSingleView(APIView):
    """ 更新單筆stream """
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        try:
            user = User.objects.get(username=username)
        except:
            return Response({'code': 1, 'data': None})

        object, create =  StreamShiftTable.objects.get_or_create(user_id=user.id, link=request.data['link'], type=request.data['type'])
        if create:
            return Response({'code':0, 'data':'成功創建'}, status=status.HTTP_200_OK)
        return Response({'code': 1, 'data': '此人已存在'}, status=status.HTTP_200_OK)


class StreamUpdateView(APIView):
    """ 編輯單筆直播推薦 """
    # permission_classes = []
    # authentication_classes = []
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        data = request.data
        StreamShiftTable.objects.filter(id=id).update(link=data['link'])
        return Response({'code':0, 'data':'編輯成功'}, status=status.HTTP_200_OK)


class StreamDeleteView(APIView):
    """ 刪除單筆直播推薦 """
    # permission_classes = []
    # authentication_classes = []
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        try:
            StreamShiftTable.objects.get(id=id).delete()
        except StreamShiftTable.DoesNotExist:
            return Response({'code': 4442, 'data': '找不到帳號'}, status=status.HTTP_200_OK)
        return Response({'code': 0, 'data': '完成刪除'}, status=status.HTTP_200_OK)