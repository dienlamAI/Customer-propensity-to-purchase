from .models import *
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from crud.forms import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash 
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import uuid
import pandas as pd
import pickle
import numpy as np
import threading
import datetime
from .serializers import SimulationSerializer

# Register
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            try:
                user.full_clean()
                user.save()
                messages.success(request, 'Member was created successfully!')
                return HttpResponseRedirect('/register/success/')
            except ValidationError as e:
                messages.error(request, 'Error: {}'.format(e))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def register_success(request):
    return render(request, 'success.html')

# Dashboard
@login_required
def dashboard(request):
    get_simulation = Simulation.objects.all()  
    get_simulation = list(get_simulation)
    get_simulation.reverse() 
    number_user = len(get_simulation)  
    max_score = 0
    min_score = 0  
    for i in get_simulation:
        if i.score > max_score:
            max_score = i.score
        if i.score < min_score:
            min_score = i.score 
    score_counts = {'5-10': 0, '10-30': 0, '>30': 0}
    for i in get_simulation:
        if 5 <= i.score < 10:
            score_counts['5-10'] += 1
        elif 10 <= i.score <= 30:
            score_counts['10-30'] += 1
        elif i.score > 30:
            score_counts['>30'] += 1 
    counts = list(score_counts.values())
    number_potential_customers = counts[1]+counts[2]


    # percent
    selected_products = request.session.get('selected_products')
    if number_user != 0 and number_user != selected_products[0]:
        number_user_percent = round((number_user-selected_products[0])/number_user*100, 2)
        if max_score == 0:
            max_score_percent = 0
        else:
            max_score_percent = round((max_score-selected_products[1])/max_score*100, 2)
        if min_score == 0:
            min_score_percent = 0
        else:
            min_score_percent = round((min_score-selected_products[2])/min_score*100, 2)
        if number_potential_customers == 0:
            number_potential_customers_percent = 0
        else:
            number_potential_customers_percent = round((number_potential_customers-selected_products[3])/number_potential_customers*100, 2)
        request.session['selected_products'] = [number_user, max_score, min_score, number_potential_customers]
        request.session['selected_products_percent'] = [number_user_percent, max_score_percent, min_score_percent, number_potential_customers_percent]
    elif number_user == selected_products[0]:
        number_user_percent = request.session.get('selected_products_percent')[0]
        max_score_percent = request.session.get('selected_products_percent')[1]
        min_score_percent = request.session.get('selected_products_percent')[2]
        number_potential_customers_percent = request.session.get('selected_products_percent')[3]
    else:
        number_user_percent = 0
        max_score_percent = 0
        min_score_percent = 0
        number_potential_customers_percent = 0
        request.session['selected_products'] = [0, 0, 0, 0]
        request.session['selected_products_percent'] = [0, 0, 0, 0]
    context = {'get_simulation': get_simulation, 'number_user': number_user, 
               'max_score': round(max_score,2), 'min_score': round(min_score,4),
               'number_potential_customers': number_potential_customers,
               'number_user_percent': number_user_percent,
               'max_score_percent': max_score_percent,
               'min_score_percent': min_score_percent,
               'number_potential_customers_percent': number_potential_customers_percent}
    return render(request, 'dashboard.html', context)

# Upload File
def process_data_chunk(df_chunk):
    for index, row in df_chunk.iterrows(): 
        simulation = Simulation(
            user_id = row['UserID'],
            basket_icon_click = row['basket_icon_click'],
            basket_add_list = row['basket_add_list'],
            basket_add_detail = row['basket_add_detail'],
            sort_by = row['sort_by'],
            image_picker = row['image_picker'],
            account_page_click = row['account_page_click'],
            promo_banner_click = row['promo_banner_click'],
            detail_wishlist_add = row['detail_wishlist_add'],
            list_size_dropdown = row['list_size_dropdown'],
            closed_minibasket_click = row['closed_minibasket_click'],
            checked_delivery_detail = row['checked_delivery_detail'],
            checked_returns_detail = row['checked_returns_detail'],
            sign_in = row['sign_in'],
            saw_checkout = row['saw_checkout'],
            saw_sizecharts = row['saw_sizecharts'],
            saw_delivery = row['saw_delivery'],
            saw_account_upgrade = row['saw_account_upgrade'],
            saw_homepage = row['saw_homepage'],
            device_computer = row['device_computer'],
            device_tablet = row['device_tablet'],
            returning_user = row['returning_user'],
            loc_uk = row['loc_uk'], 
            propensity = row['propensity'],
            score = row['score'],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(), )
        simulation.save() 
@login_required
def fileupload(request): 
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        number = request.POST.get('extra_quantity')
        threading1 = request.POST.get('threading')
        if myfile.name.endswith('.csv') and myfile != None:   
            try:
                start = datetime.datetime.now()
                df = pd.read_csv(myfile)   
                df = df.head(int(number))
                if len(df) >= 50:
                    num_threads = int(threading1)
                    chunk_size = len(df) // num_threads 
                    chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
                    threads = []
                    for chunk in chunks:
                        t = threading.Thread(target=process_data_chunk, args=(chunk,))
                        threads.append(t)
                        t.start()
                    
                    for t in threads:
                        t.join()   
                    
                else:
                    process_data_chunk(df)
                end = datetime.datetime.now()
                t = end - start
                messages.success(request, 'File was uploaded successfully!')
                print(f'File was uploaded successfully {t}!')
                return redirect('fileupload')
            except Exception as e:
                print("Lỗi khi đọc tệp CSV:", e)
        else:
            print("Loại tệp không được chấp nhận. Hãy chọn tệp CSV.")
    get_simulation = Simulation.objects.all()  
    get_simulation = list(get_simulation)
    get_simulation.reverse() 
    context = {'get_simulation': get_simulation}
    return render(request, 'fileupload.html', context) 

# Simulation 
def convert_to_score(probability, epsilon=1e-10):
    score = np.log((probability + epsilon) / (1 - probability + epsilon))
    return score+30
 
@login_required
def simulation(request):
    columns = ["Basket icon click", "Basket add list", "Basket add detail", "Sort by", "Image picker", "Account page click", "Promo banner click", "Detail wishlist add", "List size dropdown", "Closed minibasket click", "Checked delivery detail", "Checked returns detail", "Sign in", "Saw checkout", "Saw sizecharts", "Saw delivery", "Saw account upgrade", "Saw homepage", "Device computer", "Device tablet", "Returning user", "Loc uk"]
    
    if request.method == 'POST':
        name = []
        for column in columns:
            column = column.lower().replace(" ", "_") 
            n = request.POST.get(column)
            if n == 'on':
                name.append(1)
            else:
                name.append(0)
        
        with open('D:/HK2/Kỹ_thuật_dữ_liệu/final/backend/crud/model/model_filename.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        simulation = Simulation(
            user_id = uuid.uuid4(),
            basket_icon_click = name[0],
            basket_add_list = name[1],
            basket_add_detail = name[2],
            sort_by = name[3],
            image_picker = name[4],
            account_page_click = name[5],
            promo_banner_click = name[6],
            detail_wishlist_add = name[7],
            list_size_dropdown = name[8],
            closed_minibasket_click = name[9],
            checked_delivery_detail = name[10],
            checked_returns_detail = name[11],
            sign_in = name[12],
            saw_checkout = name[13],
            saw_sizecharts = name[14],
            saw_delivery = name[15],
            saw_account_upgrade = name[16],
            saw_homepage = name[17],
            device_computer = name[18],
            device_tablet = name[19],
            returning_user = name[20],
            loc_uk = name[21],
            propensity = loaded_model.predict_proba([name])[:,1],
            score = convert_to_score(loaded_model.predict_proba([name])[:,1]),
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now()
        )
        simulation.save()
        messages.success(request, 'Simulation was created successfully!')
        return redirect('simulation') 
    get_simulation = Simulation.objects.all()  
    get_simulation = list(get_simulation)
    get_simulation.reverse() 
    context = {'columns': columns, 'get_simulation': get_simulation}
    return render(request, 'simulation.html',context)

# lưu file từ database
@login_required
# def save_file(request):
#     get_simulation = Simulation.objects.all()  
#     get_simulation = list(get_simulation)
#     serializer = SimulationSerializer(get_simulation, many=True)
#     get_simulation = serializer.data

#     print(get_simulation.columns)
#     get_simulation = pd.DataFrame(get_simulation)
#     print(get_simulation)

#     # get_simulation = get_simulation.drop(columns=['id', 'created_at', 'updated_at'])
#     # get_simulation.to_csv('D:/HK2/Kỹ_thuật_dữ_liệu/final/backend/crud/static/file/simulation.csv', index=False)
#     messages.success(request, 'File was saved successfully!')
#     return redirect('simulation')

def save_file(request):
    get_simulation = Simulation.objects.all()  
    get_simulation = list(get_simulation)
    print(get_simulation[0])
    cls = list(get_simulation[0])
    serializer = SimulationSerializer(get_simulation, many=True)
    get_simulation = serializer.data

    l = []
    for cl in cls:
        l.append([i[cl] for i in get_simulation])
    print(l)
    return redirect('database')

@login_required
def delete1(request, user_id): 
    simulation = Simulation.objects.filter(user_id=user_id).first()
    simulation.delete()
    messages.success(request, 'Data was deleted successfully!') 
    return redirect('database')

@login_required
def delete_all(request):
    Simulation.objects.all().delete()
    messages.success(request, 'All Simulations were deleted successfully!') 
    return redirect('database')

# database
@login_required
def database(request):
    get_simulation = Simulation.objects.all()  
    get_simulation = list(get_simulation)

    serializer = SimulationSerializer(get_simulation, many=True)
    get_simulation = serializer.data 
    get_simulation.reverse() 

    # Pagination
    if request.method == 'GET':
        number = request.GET.get('number', 10) 
        number = int(number)

        select = request.GET.get('fiter', 'All')
        if select == "All":
            get_simulation = get_simulation
        elif select == "Level 1":
            get_simulation = [i for i in get_simulation if i['score'] >30] 
        elif select == "Level 2":
            get_simulation = [i for i in get_simulation if 20 <= i['score'] <= 30] 
        elif select == "Level 3":
            get_simulation = [i for i in get_simulation if 10 <= i['score'] < 20]
    else:
        number = 10
    paginator = Paginator(get_simulation, number)
    page = request.GET.get('page')
    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages) 
    context = {'get_simulation': get_simulation, 'data': data, 'number': number, 'select': select}
    return render(request, 'database.html', context)

# User
@login_required
def users(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {'users': users})

@login_required
def user_delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, 'User was deleted successfully!')
    return redirect('users')

#  change password
@login_required
def changePassword(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')
        
        user = request.user
        
        # Check if the current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect.')
            return render(request, 'change_password.html')
        
        # Check if new password matches repeat password
        if new_password != repeat_password:
            messages.error(request, 'New password and repeat password do not match.')
            return render(request, 'change_password.html')
        
        # Change the password
        user.set_password(new_password)
        user.save()
         
        update_session_auth_hash(request, user)
        
        messages.success(request, 'Your password was successfully updated!')
        return redirect('change_password')
        
    return render(request, 'change_password.html')

# 404
def custom_404(request, exception):
    return render(request, '404.html', status=404)

#  API
class chartPie(APIView):  
    def get(self, request): 
        get_simulation = Simulation.objects.all()
        get_simulation = list(get_simulation)
        score_counts = {'5-10': 0, '10-30': 0, '>30': 0}
        for i in get_simulation:
            if 5 <= i.score < 10:
                score_counts['5-10'] += 1
            elif 10 <= i.score <= 30:
                score_counts['10-30'] += 1
            elif i.score > 30:
                score_counts['>30'] += 1
        scores = list(score_counts.keys())
        counts = list(score_counts.values())
        return Response({'scores': scores, 'counts': counts}, status=status.HTTP_200_OK)

class chartBar(APIView):
    def get(self, request):
        get_simulation = Simulation.objects.all()
        get_simulation = list(get_simulation)
        score_counts = {'10-20': 0, '20-30': 0, '>30': 0}
        for i in get_simulation:
            if 10 <= i.score < 20:
                score_counts['10-20'] += 1
            elif 20 <= i.score <= 30:
                score_counts['20-30'] += 1
            elif i.score > 30:
                score_counts['>30'] += 1
        scores = list(score_counts.keys())
        counts = list(score_counts.values())
        return Response({'scores': scores, 'counts': counts}, status=status.HTTP_200_OK)
    
# class getData(APIView): 
#     def post(self, request):
#         get_simulation = Simulation.objects.all()
#         # get_simulation = list(get_simulation)
#         serializer = SimulationSerializer(get_simulation, many=True)
#         get_simulation = serializer.data 
#         select = request.data.get('selected','') 
#         if select == "All":
#             return Response({'data': get_simulation}, status=status.HTTP_200_OK)
#         elif select == "Level 1":
#             get_simulation = [i for i in get_simulation if i['score'] >30]
#             return Response({'data': get_simulation}, status=status.HTTP_200_OK)
#         elif select == "Level 2":
#             get_simulation = [i for i in get_simulation if 20 <= i['score'] <= 30]
#             return Response({'data': get_simulation}, status=status.HTTP_200_OK)
#         elif select == "Level 3":
#             get_simulation = [i for i in get_simulation if 10 <= i['score'] < 20]
#             return Response({'data': get_simulation}, status=status.HTTP_200_OK)
        
#     def get(self, request):
#         get_simulation = Simulation.objects.all()
#         serializer = SimulationSerializer(get_simulation, many=True)
#         get_simulation = serializer.data
#         return Response({'data': get_simulation}, status=status.HTTP_200_OK)
    

