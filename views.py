from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.

def home(request):
    try:
        request.COOKIES['todo_list']
    except:
        response = HttpResponseRedirect('/todo')
        response.set_cookie('todo_list', '', None)
        return response

    print('all cookies as they hit view', request.COOKIES)
    print('todo_list as it hits view:', request.COOKIES['todo_list'])
    if request.method == 'POST':
        try:
            request.POST['item']
            todo_list = request.COOKIES['todo_list']
            print(todo_list)
            if len(todo_list) < 2:
                todo_list = request.POST['item']
            else:
                add_item = ',' + request.POST['item']
                todo_list += add_item
            response = HttpResponseRedirect('/todo')
            response.set_cookie('todo_list', todo_list, None)
            return response
        except:
            todo_list = request.COOKIES['todo_list'].split(',')
            for key in request.POST.keys():
                if key in todo_list:
                    todo_list.remove(key)
                    response = HttpResponseRedirect('/todo')
                    response.set_cookie('todo_list', ','.join(todo_list), None)
                    return response
                elif key == 'delete_all':
                    response = HttpResponseRedirect('/todo')
                    response.delete_cookie('todo_list')
                    return response
       
    else:
        if len(request.COOKIES['todo_list']) < 2:
            todo_list = None
        else:
            todo_list = request.COOKIES['todo_list'].split(',')
            count = 0
            todo_dict_list = []
            for i, item in enumerate(todo_list):
                count+=1
                todo_dict_list.append({'item':item, 'num':str(i)})

            todo_list = todo_dict_list
                
            #count = [i+1 for i in range(len(todo_list))]
            #todo_list = zip(count, todo_list)



    context = {'todo_list':todo_list}
    print('context on way to template', context)
    return render(request, 'todo_cookies/todo_home.html', context)
