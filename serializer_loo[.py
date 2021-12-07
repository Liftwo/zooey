class KhandsStarUpdateGroupView(APIView):
    """ 更新Khands表 """
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        # 先將type2改為0
        KhandsStar.objects.filter(type=2).update(type=0)
        # 再把type1移為2
        KhandsStar.objects.filter(type=1).update(type=2)
        # 將進來的名單，建立為1
        obj_list = []
        for i in data:
            obj = KhandsStar.objects.update_or_create(user_id=i['user_id'], defaults={'type':i['type'], 'homePage':i['homepage']})
            obj_list.append(obj[0])  # 這部最為重要
        ser = KhandsHomepageRecommendSerializer(obj_list, many=True)
        return Response({'code': 0, 'data': ser.data}, status=status.HTTP_200_OK)