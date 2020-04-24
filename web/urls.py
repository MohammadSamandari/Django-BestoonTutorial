from django.conf.urls import url
from . import views

urlpatterns = [
    # anyurl with submit/expense should run the submit_expense def in views.py
    url(r'^submit/expense/$',views.submit_expense, name='submit_expense'),
    url(r'^submit/income/$',views.submit_income, name='submit_income'),
    url(r'^accounts/register/$',views.register,name='register'),
    url(r'$',views.index,name='index')

]