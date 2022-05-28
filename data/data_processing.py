import csv
from fileinput import filename
from numpy import asarray, save,load
from numpy import savetxt
from dash import Dash, html, dcc
import plotly.graph_objs as go
import pandas as pd
import datetime
import numpy as np
from py import process

def getPrice(string):
    return float(string.replace('$', ''))

def getDataFromMulipleCsv(filearray):
        filenamePrefix = 'daily_sales_data_'
        filenames = [filenamePrefix + str(i) + '.csv' for i in filearray]
        return filenames

def getDataFromCSV(filename):
        filenames = getDataFromMulipleCsv(filename)
        productsInfo = []
        for filename in filenames:
                with open(filename, 'r') as csvFile:
                        csvReader = csv.reader(csvFile)
                        for row in csvReader:
                                if row[0] != 'pink morsel': 
                                        continue
                                processedRow = processCsvData(row)
                                productsInfo.append(processedRow)
        return productsInfo

def processCsvData(row):
        sales = getPrice(row[1]) * int(row[2])
        return  [sales, row[3], row[4]]
         
def storeData(data, filename='result.npy'):
        # data = asarray(data)
        save(filename, data)

def getData(filename='result.npy'):
        return load(filename)

def createLinearGraph(elements):
        x = [element[1] for element in elements]
        y = [element[0] for element in elements]
        fig = go.Figure(data=[go.Scatter(x=x, y=y)])
        return fig

def RenderGraph(fig, header):
        headerComponent=  html.H1(header)
        graphComponent = dcc.Graph(
        id='example-graph',
        figure=fig
        )
        return html.Div([headerComponent, graphComponent])

def arrayValuesToFloat(array):
        return [[float(element[0]),element[1],element[2]] for element in array]

if __name__ == '__main__':
    app = Dash(__name__)
    productsInfo = getDataFromCSV([0,1,2])
    storeData(productsInfo)
    data = np.ndarray.tolist(getData())
    data = arrayValuesToFloat(data)
    sorted(productsInfo, key=lambda x: datetime.datetime.strptime(x[1], '%Y-%m-%d'))
    fig=createLinearGraph(productsInfo)
    app.layout = RenderGraph(fig, header='Linear Graph of pink morsel sales')
    app.run_server(debug=True)


