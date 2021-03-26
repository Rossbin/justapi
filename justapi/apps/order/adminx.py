import xadmin

# 注册banner表
from . import models

xadmin.site.register(models.Order)
xadmin.site.register(models.OrderDetail)
