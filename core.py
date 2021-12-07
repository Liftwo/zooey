def get(self, request, *args, **kwargs):
    s = {}
    s['page'] = int(self.request.query_params.get('page', '1'))
    s['uid'] = request.META.get('HTTP_USERID')
    s['size'] = int(self.request.query_params.get('size', '8'))
    if s['page'] > 10:
        return Response({'code': 0, 'data': []}, status=status.HTTP_200_OK)
    if s['page'] == 1:
        res = distributeGet_size.delay(s)
        obj = AsyncResult(id=res.id, app=app)
        return Response({'code': 0, 'data': obj.get()}, status=status.HTTP_200_OK)

    fid = self.request.query_params.get('previous', '')
    if fid:
        s['fid'] = fid
    res = distributeKhandsStarGet.delay(s)
    obj = AsyncResult(id=res.id, app=app)
    return Response({'code': 0, 'data': obj.get()}, status=status.HTTP_200_OK)