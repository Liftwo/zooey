from rest_framework import serializers
from .models import *
from reward.models import Present
from drfuser.models import User
from drffollow.models import Follow
from drfworks.models import WorksV2
from django.forms.models import model_to_dict
from django.db.models import Avg
from django.db.models.functions import Round
from drfshow.models import Designer
from drfuser.models import PrivateSetting
from drfplatform.models import YtChannel


class KhandsStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhandsStar
        fields = '__all__'


class PrivateSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateSetting
        fields = "__all__"
        read_only_fields = ['user', 'message', 'audio', 'followsMes', 'rewardMes', 'bulletin', 'attention', 'sponsor', 'chatTips', 'friendRequest']


class ChatUserInfoSerializer(serializers.ModelSerializer):
    introduce = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'avatar', 'uuid', 'nickname', 'introduce', 'identity', 'donateStatus']

    def get_introduce(self, obj):
        return ''


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ["uuid", "avatar", "nickname", "introduce", "identity"]


class UserForSearchSerializer(serializers.ModelSerializer):
    kind = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = "__all__"
        fields = ["id", "avatar", "nickname", "introduce", "identity", "uuid", "kind", "views"]

    def get_kind(self, obj):
        return 2


class OffcialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "avatar", "nickname", "introduce"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreatorDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CreatorDetails
        fields = '__all__'


class ShowBindWorksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorDetails
        fields = ['Pid', 'platform', 'is_show']
        read_only_fields = fields


class BindWorksViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorDetails
        fields = ['id', 'title', 'avatar', 'Pid', 'platform']


class UserIntroductCreatorplatform(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'introduce', 'nickname', 'avatar']


class CreatorplatformSerializer(serializers.ModelSerializer):
    user = UserIntroductCreatorplatform()

    class Meta:
        model = CreatorDetails
        fields = ['user', 'title', 'avatar', 'fans']


class spider_CreatorplatformSerializer(serializers.ModelSerializer):
    user = UserIntroductCreatorplatform()

    class Meta:
        model = CreatorDetails
        fields = ['Pid', 'id', 'user', 'title', 'avatar', 'access_token', 'open_id']
        read_only_fields = fields


class CreatorDetailsViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CreatorDetails
        # fields = '__all__'
        fields = ['user', 'title', 'avatar', 'fans', 'avgViews', 'avgComments', 'avgInteractions', 'fansGrouth',
                  'efficiency',
                  'Pid', 'platform']


class vlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'avatar', 'introduce', 'nickname', 'identity']


class CreatorUseridTagSerializer(serializers.ModelSerializer):
    user = vlogUserSerializer()

    class Meta:
        model = CreatorDetails
        fields = ['id', 'user', 'title', 'Pid', 'is_show', 'fans', 'avatar', 'platform']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name', 'id')
        read_only_fields = fields


class CreatorTagsSerializer(serializers.ModelSerializer):
    # tags = TagsSerializer()
    creator = CreatorUseridTagSerializer()
    designer = serializers.SerializerMethodField()

    class Meta:
        model = CreatorTags
        fields = '__all__'

    def get_designer(self, obj):
        d = Designer.objects.filter(user_id=obj.creator.user_id)
        if d.exists() and obj.creator.user.identity == 4:
            return 'designer'
        elif d.exists() and obj.creator.user.identity == 2:
            return 'both'
        else:
            return 'creator'


class CreatorDetailCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorDetails
        fields = ['avatar', 'platform', 'title']
        read_only_fields = fields


class OfficialSerializer(serializers.ModelSerializer):
    """ 官方推薦12 序列器"""
    user = OffcialUserSerializer()

    class Meta:
        model = OfficialRecommendList
        fields = '__all__'


class TagsFilterSerializer(serializers.ModelSerializer):
    tags = TagsSerializer()

    class Meta:
        model = CreatorTags
        fields = ['tags', 'creator']
        read_only_fields = fields


class BindWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorDetails
        fields = ['title', 'is_show', 'platform']


class ShowBindPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorDetails
        fields = ['title', 'avatar', 'is_show', 'platform']


class CreatorFilterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['introduce', 'nickname', 'avatar', 'isYt_bind', 'isFb_bind', 'isTw_bind', 'isIg_bind', 'emailStatus',
                  'donateStatus']


class CreatorFilterSerializer(serializers.ModelSerializer):
    creator = CreatorUseridTagSerializer()

    class Meta:
        model = CreatorTags
        fields = ['title', 'user', 'avatar', 'platform']


class CreatorDetailSerializer(serializers.ModelSerializer):
    user = CreatorFilterUserSerializer()

    class Meta:
        model = CreatorDetails
        fields = '__all__'
        read_only_fields = ['avatar', 'fans', 'user', 'platform', 'is_show', 'Pid', 'title']


# class chcek(serializers.ModelSerializer): # 檢查帳號用
#     class Meta:
#         model = CreatorDetails
#         fields = '__all__'
class CreatorIdUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['avatar', 'uuid', 'nickname', 'is_act']


class CreatorIdSerializer(serializers.ModelSerializer):
    user = CreatorIdUserSerializer()

    class Meta:
        model = CreatorDetails
        read_only_fields = ['user']


class testSerializer(serializers.Serializer):
    user__uuid = serializers.SerializerMethodField(read_only=True)
    user__avatar = serializers.SerializerMethodField(read_only=True)
    user__nickname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User

    def get_user__uuid(self, obj):
        return obj.uuid

    def get_user__avatar(self, obj):
        return obj.avatar

    def get_user__nickname(self, obj):
        return obj.nickname


class RandomSerializer(serializers.Serializer):
    works = serializers.SerializerMethodField(read_only=True)
    anchor__uuid = serializers.CharField(read_only=True)
    anchor__introduce = serializers.CharField(read_only=True)
    anchor__nickname = serializers.CharField(read_only=True)
    anchor__avatar = serializers.CharField(read_only=True)
    anchor__identity = serializers.IntegerField(read_only=True)
    follows = serializers.IntegerField(read_only=True)

    def get_works(self, obj):
        data = WorksV2.objects.filter(creator=obj.get('anchor__uuid'))[:3]
        return [model_to_dict(i, fields=['imgUrl']) for i in data]


class RandomUser(serializers.ModelSerializer):
    kind = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    is_follow = serializers.SerializerMethodField(read_only=True)
    platform = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        read_only_fields = ['uuid', 'nickname', 'introduce', 'avatar', 'is_main', 'donateStatus', 'emailStatus', 'is_follow',
                  'platform', 'kind', 'works']

    def get_works(self, obj):
        data = WorksV2.objects.filter(creator=obj.uuid)[:3]
        return [model_to_dict(i, fields=['imgUrl']) for i in data]

    # def get_fans(self,obj):
    #     data = Follow.objects.filter(anchor_id=obj.id,is_delete=False).count()
    #     return data

    def get_is_follow(self, obj):
        user = self.context.get('request')
        # print('user_uuid',user)
        if user == None:
            return False
        try:
            is_follow = Follow.objects.get(user__uuid=user, anchor_id=obj.id)
            print('ffff', is_follow)
            if is_follow.is_delete == True:
                return False
            else:
                return True
        except Follow.DoesNotExist:
            print('not exist')
            return False

    def get_platform(self, obj):
        data = obj.creator_detail.filter(platform__in=['yt', 'tw', 'fb', 'ig'])
        return [{i.platform: i.Pid, 'fans': i.fans} for i in data]

    # def get_popular(self,obj):
    #     data = CreatorDetails.objects.filter(platform__in=['yt', 'fb', 'tw', 'ig']).values('user_id').aggregate(
    #         popular=Round(Avg('fans')))
    #     return data
    def get_kind(self, obj):
        return 2


class RandomUserV2(serializers.Serializer):
    uuid = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    introduce = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    is_main = serializers.SerializerMethodField(read_only=True)
    donateStatus = serializers.SerializerMethodField(read_only=True)
    emailStatus = serializers.SerializerMethodField(read_only=True)
    is_podCast = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)
    is_follow = serializers.SerializerMethodField(read_only=True)
    platform = serializers.SerializerMethodField(read_only=True)

    def get_uuid(self, obj):
        try:
            return obj.user.uuid
        except:
            return obj.uuid

    def get_nickname(self, obj):
        try:
            return obj.user.nickname
        except:
            return obj.nickname

    def get_introduce(self, obj):
        try:
            return obj.user.introduce
        except:
            return obj.introduce

    def get_avatar(self, obj):
        try:
            return obj.user.avatar
        except:
            return obj.avatar

    def get_is_main(self, obj):
        try:
            return obj.user.is_main
        except:
            return obj.is_main

    def get_donateStatus(self, obj):
        try:
            return obj.user.donateStatus
        except:
            return obj.donateStatus

    def get_emailStatus(self, obj):
        try:
            return obj.user.emailStatus
        except:
            return obj.emailStatus

    def get_is_podCast(self, obj):
        try:
            return obj.user.isPc_bind
        except:
            return obj.isPc_bind

    def get_kind(self, obj):
        return 2

    def get_is_follow(self, obj):
        user = self.context.get('request')
        if user == None:
            return False
        try:
            aid = obj.user.id
        except:
            aid = obj.id
        try:
            is_follow = Follow.objects.get(user__uuid=user, anchor_id=aid)
            if is_follow.is_delete == True:
                return False
            else:
                return True
        except Follow.DoesNotExist:
            print('not exist')
            return False

    def get_platform(self, obj):
        try:
            uid = obj.user.id
        except:
            uid = obj.id
        data = CreatorDetails.objects.filter(user_id=uid, platform__in=['yt', 'tw', 'fb', 'ig']).values('platform',
                                                                                                        'Pid', 'fans')
        return [{i['platform']: i['Pid'], 'fans': i['fans']} for i in data]


class ShuffleSerialize(serializers.Serializer):
    user__uuid = serializers.CharField(read_only=True)
    user__nickname = serializers.CharField(read_only=True)
    user__avatar = serializers.CharField(read_only=True)
    user__views = serializers.IntegerField(read_only=True)
    fansCount = serializers.IntegerField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = '__all__'

    def get_kind(self, obj):
        return 2


"""
class PopularCreatorWorksV2Serialize(serializers.Serializer):
    user__uuid = serializers.CharField()
    user__nickname = serializers.CharField()
    user__avatar = serializers.CharField()
    user__views = serializers.IntegerField()
    works = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()
    class Meta:
        fields = '__all__'

    def get_works(self,obj):
        if obj['user__is_main'] in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])

        res = [i for i in work]
        return res

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'],anchor__uuid=obj['user__uuid'],is_delete=False)
        if not f.exists():
            return True
        return False

    def get_kind(self,obj):
        return 2
"""


class PopularCreatorWorksV2Serialize(serializers.Serializer):
    user__uuid = serializers.SerializerMethodField(read_only=True)
    user__nickname = serializers.SerializerMethodField(read_only=True)
    user__avatar = serializers.SerializerMethodField(read_only=True)
    user__views = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_user__uuid(self, obj):
        return str(obj['anchor__uuid'])

    def get_user__nickname(self, obj):
        return obj['anchor__nickname']

    def get_user__avatar(self, obj):
        return obj['anchor__avatar']

    def get_user__views(self, obj):
        return obj['anchor__views']

    def get_works(self, obj):
        if obj['anchor__is_main'] in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj['anchor__uuid']), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj['anchor__uuid']), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])

        res = [i for i in work]
        return res

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'], anchor__uuid=obj['anchor__uuid'], is_delete=False)
        if not f.exists():
            return True
        return False

    def get_kind(self, obj):
        return 2

class PopularCreatorKhandsStarWorksV3Serialize(serializers.Serializer):
    user__uuid = serializers.SerializerMethodField(read_only=True)
    user__nickname = serializers.SerializerMethodField(read_only=True)
    user__avatar = serializers.SerializerMethodField(read_only=True)
    user__views = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_user__uuid(self, obj):
        return obj['user__uuid']

    def get_user__nickname(self, obj):
        return obj['user__nickname']

    def get_user__avatar(self, obj):
        return obj['user__avatar']

    def get_works(self, obj):
        if obj['user__is_main'] in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        res = [i.get('_id') for i in work]
        return res

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'], anchor__uuid=obj['user__uuid'], is_delete=False)
        if not f.exists():
            return True
        return False

    def get_kind(self, obj):
        return 2

    def get_user__views(self, obj):
        return 0

class PopularCreatorKhandsStarWorksV2Serialize(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    uuid = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_uuid(self, obj):
        return obj['user__uuid']

    def get_nickname(self, obj):
        return obj['user__nickname']

    def get_avatar(self, obj):
        return obj['user__avatar']

    def get_works(self, obj):
        if obj['user__is_main'] in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        res = [i.get('_id') for i in work]
        return res

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'], anchor__uuid=obj['user__uuid'], is_delete=False)
        if not f.exists():
            return True
        return False

    def get_kind(self, obj):
        return 2


class FollowedCreatorDynamicSerialize(serializers.Serializer):
    uuid = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_uuid(self, obj):
        return obj.anchor.uuid

    def get_avatar(self, obj):
        return obj.anchor.avatar

    def get_nickname(self, obj):
        return obj.anchor.nickname

    def get_views(self, obj):
        return obj.anchor.views

    def get_works(self, obj):
        if obj.anchor.is_main in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj.anchor.uuid), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj.anchor.uuid), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])

        res = [i for i in work]
        return res

    def get_kind(self, obj):
        return 2


class MostFollowedCreatorSerialize(serializers.Serializer):
    anchor = serializers.SerializerMethodField(read_only=True)

    def get_anchor(self, obj):
        obj['isFollow'] = True
        obj['kind'] = 2
        f = Follow.objects.filter(user__uuid=self.context.get('user'), anchor_id=obj['anchor_id'], is_delete=False)
        if not f:
            obj['isFollow'] = False
        return obj


class StreamShiftTableSerialize(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    uuid = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)
    roomImg = serializers.SerializerMethodField(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)

    # class Meta:
    #     model=StreamShiftTable
    #     fields=['id','uuid','title','avatar','link','views','roomImg','kind']
    def get_id(self, obj):
        return obj.id

    def get_uuid(self, obj):
        return obj.user.uuid

    def get_title(self, obj):
        return obj.user.nickname

    def get_avatar(self, obj):
        return obj.user.avatar

    def get_kind(self, obj):
        return 9

    def get_link(self, obj):
        return obj.link

    def get_views(self, obj):
        return obj.views

    def get_roomImg(self, obj):
        return obj.roomImg


class RecommendAnchorSerialize(serializers.Serializer):
    uuid = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    fans = serializers.SerializerMethodField(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'], anchor__uuid=obj.user.uuid, is_delete=False)
        if not f.exists():
            return True
        return False

    def get_uuid(self, obj):
        return obj.user.uuid

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_avatar(self, obj):
        return obj.user.avatar

    def get_fans(self, obj):
        fans = obj.user.creator_detail.all().values_list('fans', flat=True)
        return sum(fans)

    def get_link(self, obj):
        return obj.link

    def get_views(self, obj):
        return obj.views

    def get_kind(self, obj):
        return 9


class PopularCreatorDynamicSerialize(serializers.Serializer):
    uuid = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    is_main = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_uuid(self, obj):
        return obj['user__uuid']

    def get_nickname(self, obj):

        return obj['user__nickname']

    def get_avatar(self, obj):
        return obj['user__avatar']

    def get_views(self, obj):
        return obj['user__views']

    def get_is_main(self, obj):
        return obj['user__is_main']

    def get_works(self, obj):
        if obj['user__is_main'] in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj['user__uuid']), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        res = [i for i in work]
        return res

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'], anchor__uuid=obj['user__uuid'], is_delete=False)
        if not f.exists():
            return True
        return False

    def get_kind(self, obj):
        return 2


class VlogRecommendCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'avatar', 'uuid']
        read_only_fields = fields


class UserRankSerialize(serializers.Serializer):
    user__uuid = serializers.SerializerMethodField(read_only=True)
    user__nickname = serializers.SerializerMethodField(read_only=True)
    user__avatar = serializers.SerializerMethodField(read_only=True)
    popular = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_user__uuid(self, obj):
        return obj.user.uuid

    def get_user__nickname(self, obj):
        return obj.user.nickname

    def get_user__avatar(self, obj):
        return obj.user.avatar

    def get_popular(self, obj):
        return obj.fans

    def get_kind(self, obj):
        return 2

    def get_kind(self, obj):
        return 2

    def get_kind(self, obj):
        return 2


class WorksWallSerialize(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)
    uuid = serializers.SerializerMethodField(read_only=True)
    urlLink = serializers.CharField(read_only=True)
    imgUrl = serializers.CharField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_creator(self, obj):
        return self.context.get('anchor').get(obj.get('creator'))

    def get_uuid(self, obj):
        return obj.get("creator")

    def get_type(self, obj):
        if obj.get('platform') in ['yt', 'tw']:
            return 'video'
        return 'image'

    def get_kind(self, obj):
        return 7


class ShuffleV2Serialize(serializers.Serializer):
    user__uuid = serializers.SerializerMethodField(read_only=True)
    user__nickname = serializers.SerializerMethodField(read_only=True)
    user__avatar = serializers.SerializerMethodField(read_only=True)
    user__views = serializers.SerializerMethodField(read_only=True)
    fansCount = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_user__uuid(self, obj):
        return obj.user.uuid

    def get_user__nickname(self, obj):
        return obj.user.nickname

    def get_user__avatar(self, obj):
        return obj.user.avatar

    def get_user__views(self, obj):
        return obj.user.views

    def get_fansCount(self, obj):
        fans = CreatorDetails.objects.filter(user_id=obj.user_id).values_list('fans', flat=True)
        return sum(fans)

    def get_kind(self, obj):
        return 2


class EmergingCreatorsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    uuid = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    identity = serializers.SerializerMethodField(read_only=True)
    introduce = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj.user_id

    def get_uuid(self, obj):
        return obj.user.uuid

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_avatar(self, obj):
        return obj.user.avatar

    def get_identity(self, obj):
        return obj.user.identity

    def get_introduce(self, obj):
        return obj.user.introduce

    def get_views(self, obj):
        return obj.user.views

    def get_kind(self, obj):
        return 2


class PopularChannelSerializer(serializers.ModelSerializer):
    _id = serializers.CharField()
    kind = serializers.SerializerMethodField()

    class Meta:
        model = YtChannel
        fields = "__all__"

    def get_kind(self, obj):
        return 3


class PcdV3Serialize(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    uuid = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj['anchor_id']

    def get_uuid(self, obj):
        return str(obj['anchor__uuid'])

    def get_nickname(self, obj):
        return obj['anchor__nickname']

    def get_avatar(self, obj):
        return obj['anchor__avatar']

    def get_views(self, obj):
        return obj['anchor__views']

    def get_works(self, obj):
        if obj['anchor__is_main'] in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj['anchor__uuid']), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj['anchor__uuid']), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])

        res = [i for i in work]
        return res

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'], anchor__uuid=obj['anchor__uuid'], is_delete=False)
        if not f.exists():
            return True
        return False

    def get_kind(self, obj):
        return 2


class PcdSampleV3Serialize(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    uuid = serializers.SerializerMethodField(read_only=True)
    nickname = serializers.SerializerMethodField(read_only=True)
    views = serializers.SerializerMethodField(read_only=True)
    works = serializers.SerializerMethodField(read_only=True)
    follows = serializers.SerializerMethodField(read_only=True)
    kind = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        print(obj.user.id)
        return obj.user.id

    def get_uuid(self, obj):
        return str(obj.user.uuid)

    def get_nickname(self, obj):
        return obj.user.nickname

    def get_avatar(self, obj):
        return obj.user.avatar

    def get_views(self, obj):
        return obj.user.views

    def get_works(self, obj):
        if obj.user.is_main in ['yt', 'tw']:
            match = {'$match': {'creator': str(obj.user.uuid), "platform": {"$in": ['yt', 'tw']}}}
            group = {"$group": {"_id": "$imgUrl"}}
            sample = {"$sample": {"size": 1}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])
        else:
            match = {'$match': {'creator': str(obj.user.uuid), "platform": {"$in": ['fb', 'ig']}}}
            sample = {"$sample": {"size": 3}}
            group = {"$group": {"_id": "$imgUrl"}}
            work = WorksV2.objects.mongo_aggregate([match, group, sample])

        res = [i for i in work]
        return res

    def get_follows(self, obj):
        if not self.context['user']:
            return True
        f = Follow.objects.filter(user__uuid=self.context['user'], anchor__uuid=str(obj.user.uuid), is_delete=False)
        if not f.exists():
            return True
        return False

    def get_kind(self, obj):
        return 2