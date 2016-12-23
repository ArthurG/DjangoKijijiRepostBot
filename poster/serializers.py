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
        fields = ('id', 'address', 'title', 'description', 'categoryId', 'adType', 'priceType', 'attr', 'priceAmount', 'locationId', 'username', 'password')

    ###Write custom create/update method because of nested attributes
    def create(self, validated_data):
        all_attr_data = validated_data.pop('attr')
        item = PostableItem.objects.create(**validated_data)
        for attr_data in all_attr_data:
            PostableAttr.objects.create(related_item=item, **track_data)
        return item


    def update(self, item, validated_data):
        all_attr_data = validated_data.pop('attr')
        PostableItem.objects.filter(id=item.id).update(**validated_data)
        attrs = item.attr.all()
        attrs.delete()
        for attr_data in all_attr_data:
            PostableAttr.objects.create(related_item=item, **attr_data)
        return item






