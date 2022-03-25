"""build_mmt_datasetv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from annotation.views import show, api, first_page, annot
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', first_page.first_page),
    path('show/<int:image_id>/', show.show),
    path('annotation_with_image/', annot.annotation_with_image),
    
    path('api/show_zh_table/', api.show_zh_table),
    path('api/show_en_table/', api.show_en_table),
    path('api/login/', api.login),
]
