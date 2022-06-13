# import matplotlib.pyplot as plt
# import numpy as np
# import mplcursors
#
# fig, ax = plt.subplots()
# x = [1,2,3,4,5,1,4]
# y = [6,7,8,9,10,2,3]
# ax.scatter(x, y)
#
# po_annotation = []
# for i in range(len(x)):
#     # 标注点的坐标
#     point_x = x[i]
#     point_y = y[i]
#     point, = plt.plot(point_x, point_y, 'o', c='darkgreen')
#     # 标注plt.annotate
#     annotation = plt.annotate((x[i], y[i]), xy=(x[i], y[i]), size=10)
#     # 默认鼠标未指向时不显示标注信息
#     annotation.set_visible(False)
#     po_annotation.append([point, annotation])
#
# def on_move(event):
#     visibility_changed = False
#     for point, annotation in po_annotation:
#         should_be_visible = (point.contains(event)[0] == True)
#         print(should_be_visible)
#         print('point.contains(event)[0]:', point.contains(event))
#         print('event:', event)
#         if should_be_visible != annotation.get_visible():
#             print('1234')
#             visibility_changed = True
#             annotation.set_visible(should_be_visible)
#     if visibility_changed:
#         plt.draw()
#         print('1234567890')
#         # pass
#
# on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
# plt.show()
#
#
