# REST DJANGO ECOMMERCE

#### I. Set up the project django-ecommerce rest
1. Run environment
2. pip install Django
3. pip install djangorestframework
4. pip install markdown       # Markdown support for the browsable API.
5. pip install django-filter  # Filtering support
6. pip install django-cors-headers # security headers
7. pip install djoser # endpoint api
8. pip install pillow # image processing
9. pip install stripe # payment gateway - options: stripe, paypal, braintree
10. pip install django-autoslug
11. Add to __INSTALLED_APPS__  in setting.py
    ```
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser'
    ```
12. Add to AUTH_USER_MODEL in settings.py
    ```
    AUTH_USER_MODEL = 'djoser.User'
    CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
    ```

13. Add middleware to  __MIDDLEWARE__ in settings.py

    ```
     'corsheaders.middleware.CorsMiddleware',
    ```
14. Import include in urls.py file
    ```
    from django.conf.urls import url, include
    ```
15. Add to url in urls.py file
    ```
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    ```
16. Make migration
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
17. Create admin user
    ```
    python manage.py createsuperuser
    ```
18. Run server
    ```
    python manage.py runserver
    ```

#### II. Set up frontend - Vue
1. npm install -g @vue/cli
2. vue create project-name
   ```
    ? Please pick a preset: Manually select features 
    ? Check the features needed for your project: Babel, Router, Vuex, CSS Pre-processors
    ? Choose a version of Vue.js that you want to start the project with 3.x
    ? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
    ? Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default): Sass/SCSS (with dart-sass)
    ? Where do you prefer placing config for Babel, ESLint, etc.? In dedicated config files
    ? Save this as a preset for future projects? No
   ```
3. cd project-name
4. npm install axios
5. npm install bulma
6. npm install bulma-toast
7. npm run serve




#### III. Include fontawaesome

#### IV. Set up base template

#### V. Create django app and models for products
    
```python manage.py startapp product```

Create model category
Register __app product__ to settings.py in __INSTALLED_APPS__        

    INSTALLED_APPS = [
    ...    
    'product',
    ]
    
Make migration

    python manage.py makemigrations
    python manage.py migrate

Import io,PIL,File in models.py

    from io import BytesIO
    from PIL import Image
    from django.core.files import File
Register model in  admin.py

    from product.models import Category, Product
    admin.site.register(Category)
    admin.site.register(Product)
Add media url to  settings.py

    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

Edit urls.py

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
    # ... the rest of your URLconf goes here ...
    ] 
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#### VI. Create serializer and views for products
Create serializer.py in product app

    from rest_framework import serializers
    from .models import Category, Product

    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ('id', 'name')

    class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ('id', 'name', 'get_absolute_url', 'description', 'price', 'get_image', 'get_thumbnail')

Import  serializers, APIView, response to views.py

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from .models import Product
    from .serializers import CategorySerializer, ProductSerializer

Make view for Latest Products List

    class LatestProductsList(APIView):
        def get(self, request):
            products = Product.objects.all()[:4]
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

Create urls.py file
    
    from django.urls import path, include
    from product import views

    urlpatterns = [
        path('latest-products/', views.LatestProductsList.as_view()),
    ]

Add path to urls.py in admin

    urlpatterns += [
        path('api/v1/', include('product.urls')),
    ]

#### VII. Create simple front page

#### VIII.View a product

#### IX.Sette opp Vuex / State

#### X.Make it possible to add to cart