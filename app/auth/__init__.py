# coding=utf-8
from flask import Blueprint

auth=Blueprint("auth",__name__) # 创建蓝本
from . import views