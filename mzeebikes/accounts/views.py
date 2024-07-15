from django.shortcuts import render
from  rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime






class RegisterView(APIView):
    def post(self, request):
        serializer  = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




class LoginView(APIView):
    def post(self, request):
        # Retrieving email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Checking if email and password are provided
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=400)
        
        # Finding the user
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        return response


    #Authenticating User
class UserView(APIView):
        def get(self,request):
            token = request.COOKIES.get('jwt')

            if not token:
                raise AuthenticationFailed("unauthicated!")
            try:
                payload = jwt.decode(token,'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:    
                raise  AuthenticationFailed('unauthicated!')
            
            #getting the user
            user  = User.objects.filter(id=payload['id']).first()

            serializer  = UserSerializer(user)
            #serializing the retrieved user
            return Response(serializer.data)
    
        



class LogOutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = { 
            'message':'success'
        }
        return response


# # python3 -m pip install PyJWT