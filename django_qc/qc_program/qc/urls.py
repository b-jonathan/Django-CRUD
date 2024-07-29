#!C:/Users/user/AppData/Local/Programs/Python/Python310/python.exe
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path("login/", views.loginRequest, name="login"),
    path('logout/',views.logoutView, name='logout'),
    path('complains/<int:id>', views.complainsView, name='viewcomplains'),
    path('details/', views.showDetails, name='showdetails'),
    path('details/filter/', views.FilteredArticles.as_view(), name='filteredarticles'),
    path('complains/', views.showComplains, name='showcomplains'),
    path('complains/filter/', views.FilteredComplains.as_view(), name='filteredcomplains'),
    path('analysis/', views.showAnalysis, name='showanalysis'),
    path('analysis/filter/', views.FilteredAnalysis.as_view(), name='filteredanalysis'),
    path('complains/create/', views.createComplains, name='createcomplains'),
    path('complains/create/details',  views.detailView, name='detailview'),
    path('complains/create/details/temp', views.CreateDetails.as_view(), name='createdetails'),
    path('complains/save/',  views.saveComplains, name='savecomplains'),
    path('complain/create/details/update', views.UpdateDetails.as_view(), name='updatedetails'),
    path('complain/create/details/delete', views.DeleteDetails.as_view(), name='deletedetails'),  
    path('analysis/create/',views.createAnalysis, name='createanalysis'),
    path('analysis/create/problemanalysis',views.problemAnalysisView, name='problemanalysisview'),
    path('analysis/create/problemanalysis/temp', views.CreateProblemAnalysis.as_view(), name='createproblemanalysis'),
    path('analysis/create/problemanalysis/update', views.UpdateProblemAnalysis.as_view(), name='updateproblemanalysis'),
    path('analysis/create/problemanalysis/delete', views.DeleteProblemAnalysis.as_view(), name='deleteproblemanalysis'),
    path('analysis/create/capa/temp', views.CreateCapa.as_view(), name='createcapa'),
    path('analysis/create/capa/update', views.UpdateCapa.as_view(), name='updatecapa'),
    path('analysis/create/capa/delete', views.DeleteCapa.as_view(), name='deletecapa'),
    path('analysis/save/',  views.saveAnalysis, name='saveanalysis'),
]