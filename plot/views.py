import pandas as pd
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm, UploadFileForm2
from django import forms
import plotly.graph_objects as pg
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt

def final_output_graph(dataframes):
    new_data = pd.merge(dataframes['file1'],dataframes['file2'],on='time')
    new_data = pd.merge(new_data,dataframes['file3'],on='time')
    new_data.rename(columns={'open_x':'open_base','close_x':'close_base','open_y':'open_1','close_y':'close_1','open':'open_2','close':'close_2'},inplace=True)
    new_data['base_vs_d1'] = ((new_data['open_1'] - new_data['open_base'])/new_data['open_base'])*100
    new_data['base_vs_d2'] = ((new_data['open_2'] - new_data['open_base'])/new_data['open_base'])*100
    new_data['cbase_vs_cd1'] = ((new_data['close_1'] - new_data['close_base'])/new_data['close_base'])*100
    new_data['cbase_vs_cd2'] = ((new_data['close_2'] - new_data['close_base'])/new_data['close_base'])*100
    new_data['time'] = new_data['time'].apply(lambda x: x.strip())
    new_data['year'] = new_data['time'].apply(lambda x: x[-4:])
    return new_data

def generate_html_plot(final_data,x_axis,y_axis):
    fig = pg.Figure(data=pg.Scatter(
    x=final_data[x_axis], 
    y=final_data[y_axis],
    mode='markers+lines'))
    plot_html = pio.to_html(fig,full_html = False)
    return plot_html
    
def plotly_plot(request):
    final_data = request.session.get('final_data')
    final_data = pd.read_json(final_data)
    if request.method == 'POST':
        form = UploadFileForm2(request.POST,final_data)
        if form.is_valid():
            x_axis = form.cleaned_data['x_axis']
            y_axis = form.cleaned_data['y_axis']
            year_val = int(form.cleaned_data['year'])
            final_data = request.session.get('final_data')
            final_data = pd.read_json(final_data)
            final_data = final_data.loc[final_data['year']==year_val]
            plot_html = generate_html_plot(final_data,x_axis,y_axis)
            context = {'form': form, 'plot_html':plot_html}   
            return render(request,'plot.html',context)
            # context = {'form': form,'df':final_data.head().to_html}
            # return render(request,'upload.html',context)
    else:
        form = UploadFileForm2()
    return render(request,'plot.html',{'form':form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        dataframes = {}
        if form.is_valid():
            for i in request.FILES.keys():
                uploaded_file = request.FILES[i]
                fs = FileSystemStorage()
                file_path = fs.save(uploaded_file.name, uploaded_file)
                file_url = fs.url(file_path)
            
            # Reading the uploaded file into a pandas DataFrame
                file_location = fs.path(file_path)
                dataframes[i] = pd.read_csv(file_location)  # Adjust this line based on the file type

            # You can now use the DataFrame `df` as needed
            final_data = final_output_graph(dataframes)
            request.session['final_data'] = final_data.to_json()
            choice_list = final_data.columns
            # context = {'form': form, 'df': final_data.head().to_html()}  # Display the first few rows in HTML
            return redirect(reverse('plot_data'))
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
