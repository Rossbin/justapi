import xadmin
from xadmin import views


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "Just-city 在线教育平台"  # 设置站点标题
    site_footer = "江苏省镇江市江苏科技大学"  # 设置站点的页脚
    # menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)

# 默认xadmin就已经把权限6表注册了
