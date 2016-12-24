from rest_framework import serializers
from poster.models import PostableItem, PostableAttr, AD_TYPE_CHOICES , PRICE_TYPE_CHOICES

class PostableAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostableAttr
        fields = ('key', 'val')

class PostableItemSerializer(serializers.ModelSerializer): 
    attr = PostableAttrSerializer(many=True)
    class Meta:
        model = PostableItem
        fields = ('id', 'address', 'title', 'description', 'photo1','photo2','photo3','photo4','photo5', 'photo6','photo7','photo8', 'photo9','photo10', 'categoryId', 'adType', 'priceType', 'attr', 'priceAmount', 'locationId', 'username', 'password', 'repostWaitInterval')

    ###Write custom create/update method because of nested attributes
    def create(self, validated_data):
        all_attr_data = validated_data.pop('attr')
        item = PostableItem.objects.create(**validated_data)
        for attr_data in all_attr_data:
            PostableAttr.objects.create(related_item=item, **track_data)
        return item


    def update(self, item, validated_data):
        if ('attr' in validated_data):
            all_attr_data = validated_data.pop('attr')
            item.attr.all().delete()
            for attr_data in all_attr_data:
                PostableAttr.objects.create(related_item=item, **attr_data)
        #print(**validated_data)
        item.__dict__.update(**validated_data)
        item.save()
        return item






