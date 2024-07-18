from rest_framework import serializers
from   .models import User,Bicycle



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  = ['id', 'name','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }


    #Hashing password
    def  create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if  password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        

class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Bicycle
        fields = ['id','name','description','price','category','brand', 'availability']  


