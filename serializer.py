from django.db.models import Q
class MenuV2Serializer(serializers.Serializer):
    name = serializers.CharField(required=False,allow_null=True)
    mainMenu = serializers.CharField(required=False,allow_null=True)
    route = serializers.CharField(required=False,allow_null=True)
    # class Meta:
    #     model = Menu
    #     fields = "__all__"

    def validate(self, attrs):
        if self.context.get('method')=='create':
            if not attrs.get('name'):
                raise serializers.ValidationError('not null')
        elif self.context.get('method')=='update':
            query=Q()
            query.connector='OR'
            [query.children.append((k,v)) for k,v in attrs.items()]
            menu=Menu.objects.filter(query)
            if menu.exists():
                raise serializers.ValidationError('duplicate params')
        return attrs

    def create(self, validated_data):
        data,created = Menu.objects.get_or_create(name=validated_data['name'],defaults=validated_data)
        return data

    def update(self, instance, validated_data):
        name=validated_data.get('name')
        mainMenu = validated_data.get('mainMenu')
        route = validated_data.get('route')
        print(route)
        if name:
            instance.name=name
        if mainMenu:
            instance.mainMenu=mainMenu
        if route:
            instance.route=route
        instance.save()
        return instance


from .serializers import MenuV2Serializer
class MenuCreateV2View(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        ser=MenuV2Serializer(data=request.data,context={'method':'create'})
        if ser.is_valid():
            ser.save()
            return Response(ser.validated_data)
        return Response(ser.errors)

class MenuUpdateV2View(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self,request,*args,**kwargs):
        pk=self.kwargs.get('pk')
        menu=Menu.objects.get(id=pk)
        ser=MenuV2Serializer(menu,data=request.data,context={'method':'update'})
        if ser.is_valid():
            ser.save()
            return Response(ser.validated_data)
        return Response(ser.errors)
