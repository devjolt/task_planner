from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
import re

def home(request):
    try:
        request.COOKIES['todo_list']#see if cookie exists
    except:
        response = HttpResponseRedirect('/todo')#if not make it
        response.set_cookie('todo_list', '', None)
        return response

    print('all cookies as they hit view', request.COOKIES)
    print('todo_list as it hits view:', request.COOKIES['todo_list'])
    if request.method == 'POST':
        try:
            request.POST['item']#see if an item is being posted
            if request.POST['item'] == '':#if no item posted, just reload page, no changes.
                HttpResponseRedirect('/todo')
            #if it is, get the string stored in todo list
            print(todo_list)
            todo_list = request.COOKIES['todo_list']
            if len(todo_list) < 2:#if no items in this string
                todo_list = request.POST['item']#add item to todo list
            else:
                add_item = ',' + request.POST['item']#add comma first then item from post
                todo_list += add_item#add this todo list
            response = HttpResponseRedirect('/todo')
            response.set_cookie('todo_list', todo_list, None)#assign new value to cookie
            return response
        except:#if an item is not being posted
            todo_list = request.COOKIES['todo_list'].split(',')#turn cookie string into a list
            for key in request.POST.keys():
                if key in todo_list:#see what the key is for item which has been deleted
                    todo_list.remove(key)#remove that item from created list
                    response = HttpResponseRedirect('/todo')
                    response.set_cookie('todo_list', ','.join(todo_list), None)#make this listinto a string seperated by commas again and add this to cookie
                    return response
                elif key == 'delete_all':#need to make this!
                    response = HttpResponseRedirect('/todo')
                    response.delete_cookie('todo_list')
                    return response
       
    else:
        if len(request.COOKIES['todo_list']) < 2:
            todo_list = None#display prompt to add something
        else:
            todo_list = request.COOKIES['todo_list'].split(',')#distplay todo list
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

def multi_category_todo(request):
    if request.method == 'POST':
        #(possibilities are: creating a new list, deleting a list, adding an item to a list, deleting an item from a list)
        print('post:', request.POST)
        #print(request.COOKIES)
        try:
            request.POST['create_list']
            if request.POST['create_list'] == '':#if empty, don't do anything
                return HttpResponseRedirect('/todo')
            cookie_to_create = request.POST['create_list']
            cookie_to_create = re.sub(' ', '-', cookie_to_create)
            response = HttpResponseRedirect('/todo')#if not make it
            response.set_cookie(cookie_to_create, '', None)#make a cookie of name request.POST['create_list']
            return response #return request to make cookie 
        except:
            print(request.POST)
            for key, value in request.POST.items():
                if key[:2]=='dI':
                    item, list_name = key[2:].split('?')#split contents into cookie name and list
                    print('item to delete and list', item, list_name)
                    todo_list = request.COOKIES[list_name].split(',')#turn cookie string into a list
                    todo_list.remove(item)#remove that item from created list
                    response = HttpResponseRedirect('/todo')
                    response.set_cookie(list_name, ','.join(todo_list), None)#make this listinto a string seperated by commas again and add this to cookie
                    return response
                elif key[:2]=='dL':
                    cookie_to_delete = key[2:]
                    response = HttpResponseRedirect('/todo')
                    response.delete_cookie(cookie_to_delete)#delete cookie of name request.POST['delete_list']
                    return response#return request to delete cookie
                elif key[:2]=='aD':
                    if request.POST[key]=='':
                        return HttpResponseRedirect('/todo')
                    list_name = key[2:]
                    item = request.POST[key]
                    todo_list = request.COOKIES[list_name]
                    if len(todo_list) < 2:#if no items in this string
                        todo_list = item#add item to todo list
                    else:
                        add_item = ',' + item#add comma first then item from post
                        todo_list += add_item#add this todo list
                    response = HttpResponseRedirect('/todo')
                    response.set_cookie(list_name, todo_list, None)#assign new value to cookie
                    return response
    else:
        context = {'lists':[]}
        if request.COOKIES:
            for key, value in request.COOKIES.items():#make contents into list format
                if key == 'csrftoken':
                    pass
                elif len(value) > 2:#if len(contents) > 2:
                    todo_list = value.split(',')
                    todo_dict_list = []
                    for i, item in enumerate(todo_list):
                        todo_dict_list.append({'item':item, 'num':str(i)})
                        todo_list = todo_dict_list
                        
                    item = {'list_name':key, 'list':todo_list}
                    context['lists'].append(item)
                else:
                    item = {'list_name':key, 'list':None}
                    context['lists'].append(item)
        else:
            context['lists'] = None
    print('context', context)         
    return render(request, 'todo_cookies/todo_multi.html', context)

#lists
#{'lists':[{'name of list': 'name', 'list':list }, {'name of list': 'name', 'list':list}...]}

def kill_all(request):
    response = HttpResponseRedirect('/todo')
    for key, value in request.COOKIES.items():
        response.delete_cookie(key)
    return response
