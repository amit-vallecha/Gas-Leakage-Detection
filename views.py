# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import requests
import json

@login_required(login_url="/login/")
def index(request):
    URL="https://api.thingspeak.com/channels/1414739/feeds.json?api_key="
    Key="NEABWQON525YO11Q"
    
    Timezone="&timezone=Asia/Kolkata"
    NEW_URL=URL+Key+Timezone
    print(NEW_URL)

    get_data=requests.get(NEW_URL).json()
    #print(get_data)

    channel_id=get_data['channel']['id']

    feild_1=get_data['feeds']
    print(feild_1)

    temp=[]
    for x in feild_1:
        #print(x['field1'])
        temp.append(x['field1'])

    humidity=[]
    for x in feild_1:
        #print(x['field1'])
        humidity.append(x['field2'])

    
    mq6=[]
    for x in feild_1:
        #print(x['field1'])
        mq6.append(x['field3'])

    
    timestemp=[]
    for x in feild_1:
        #print(x['field1'])
        timestemp.append(x['created_at'])

    

    h_var='Temprature'
    v_var='Humidity'

    data1=[['Gado',h_var,v_var]]
    for k,l,t in zip(temp,humidity,timestemp):
        data1.append([t,int(k),int(l)])    
   
    h_var_JSON=json.dumps(h_var)
    v_var_JSON=json.dumps(v_var)
    modified_data=json.dumps(data1)

    
    v_var2="temp"
    h_var2='mq6'
    
    data2=[['Gado',h_var2,v_var2]]
    for k,l,t in zip(mq6,humidity,timestemp):
        data2.append([t,int(k),int(l)])    
   
    h_var2_JSON=json.dumps(h_var2)
    v_var2_JSON=json.dumps(h_var2)
    modified_data2=json.dumps(data2)

    context={
        'values':modified_data,
        'values2':modified_data2,
        'h_title':h_var_JSON,
        'v_title':v_var_JSON,
        'h_title2':h_var2_JSON,
        'v_title2':v_var2_JSON,
        'segment':'index'
        
        }
    
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
