#coding=utf-8
import sys
import os
from   os.path import abspath, dirname
from turtle import left
sys.path.append(abspath(dirname(__file__)))
import tkinter
import tkinter.filedialog
from   tkinter import *
import Fun
import numpy as np
import pandas as pd
ElementBGArray={}  
ElementBGArray_Resize={} 
ElementBGArray_IM={} 

def Pie_29_onLoadData(uiName,widgetName,Figure):
    a = Figure.add_subplot(111)
    nums = [25,37,33,37,6]
    labels = ['A','B','C','D','E']
    a.pie(x=nums,labels=labels)
def Bar_30_onLoadData(uiName,widgetName,Figure):
    a = Figure.add_subplot(111)
    a.bar(left=(0,1),height=(8,4),width=0.55)