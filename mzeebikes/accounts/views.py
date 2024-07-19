from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer,BicycleSerializer,CartItemSerializer,CartSerializer
from .models import User,Bicycle,Cart,CartItem
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.views.decorators.csrf import csrf_exempt
from  rest_framework import status



@csrf_exempt
@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=400)

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

    response = Response({'jwt': token})
    response.set_cookie(key='jwt', value=token, httponly=True)
    return response


@api_view(['GET'])
def user_view(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("Unauthenticated!")

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)


@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    response = Response({'message': 'success'})
    response.delete_cookie('jwt')
    return response


@csrf_exempt
@api_view(['GET'])
def  bicycle_list(request):
    if request.method == 'GET': 
        bicycles = Bicycle.objects.all().order_by('id')
        serializer  = BicycleSerializer(bicycles, many=True)
        return  Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def post_bicycle(request):
    # Check if the bicycle already exists
    existing_bicycle = Bicycle.objects.filter(name=request.data.get('name')).first()
    
    if existing_bicycle:
        # If the bicycle already exists in database, return a 409 Conflict status
        return Response({'error': 'Bicycle with this name already exists'}, status=status.HTTP_409_CONFLICT)
    
    # If the bicycle does not exist, proceed with creating it
    serializer = BicycleSerializer(data=request.data)
    #creating ana instance of class BicycleSeriallizer and passing data to it
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT'])
def update_bicycle(request, pk):
    try:
        bicycle  = Bicycle.objects.get(pk=pk)
    except Bicycle.DoesNotExist:
        return Response({'error', 'Bicyle not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer =  BicycleSerializer(bicycle, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



@csrf_exempt
@api_view(['DELETE'])
def delete_bicycle(request,pk):
    try:
        bicycle  = Bicycle.objects.get(pk=pk)
    except Bicycle.DoesNotExist:
        return Response({'error':'Bicycle not found'}, status=status.HTTP_404_FOUND) 

    bicycle.delete()
    return Response({'message': 'Bicycle deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)   


@api_view(['GET','POST'])
def  cart_list(request):
    if request.method  == 'GET':
        carts = Cart.objects.all()
        serializer  = CartSerializer(carts, many=True)
        return  Response(serializer.data)
    

    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#retieving getting, updating and  Deleting a Cart
@api_view(['GET','PUT','DELETE'])
def cart_detail(request, pk):
    try:
        cart = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    elif request.method  == 'PUT':
        serializer  = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif  request.method  == 'DELETE':
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#listing and creating cartitems


@api_view(['GET','POST'])
def  cartitem_list(request):
    if request.method  == 'GET':
        cartitems  = CartItem.objects.all()
        serializer  = CartSerializer(cartitems, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    



#Retreiving,Updating and deletin a Cartitem

@api_view(['GET','PUT','DELETE'])
def  cartitem_detail(request, pk):
    try:
        cartitem = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        return  Response(status=status.HTTP_404_NOT_FOUND)

    if request.method  == 'GET':
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data)


    elif request.method == 'PUT':      
        serializer  = CartItemSerializer(cartitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method  == 'DELETE':
        cartitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
     


