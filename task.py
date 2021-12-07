@shared_task
def distributeGet_size(data):
    get_data = cache.get('V3pcws_%d'%data['page'] + str(data['uid']))
    if get_data:
        return get_data
    queryset = Follow.objects.select_related('anchor').filter(is_delete=False).values('anchor_id').annotate(
        fansCount=Count('id')).order_by('-fansCount').values('anchor__uuid', 'anchor__nickname', 'anchor__avatar',
                                                             'anchor__views', 'anchor__is_main')[:data['size']]
    ser = PopularCreatorWorksV2Serialize(queryset, many=True, context={'user': data['uid']})
    data_ = ser.data
    cache.set('V3pcws_%d'%data['page'] + str(data['uid']), data_, 60 * 30)
    return data_

    else:
        fid = data['fid'].split(',')
        queryset = KhandsStar.objects.select_related('user').exclude(id__in=fid).filter(homePage=True).values('id',
                                                                                                              'user__uuid',
                                                                                                              'user__nickname',
                                                                                                              'user__avatar',
                                                                                                              'user__is_main').order_by('?')[:data['size']]
    ser = PopularCreatorKhandsStarWorksV2Serialize(queryset, many=True, context={'user': data['uid']})
    data_ = ser.data
    cache.set('V3pcws_%d'%data['page'] + str(data['uid']), data_, 60 * 30)
    return data_