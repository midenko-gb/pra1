import requests 
import json
import sys
from random import randint

from datetime import datetime
from datetime import time
from datetime import date
from time import sleep

from influxdb import InfluxDBClient

from PyQt5.QtCore import Qt, QTimer, QRandomGenerator
from PyQt5.QtChart import QChartView, QLineSeries, QChart, QSplineSeries, QValueAxis
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication


class DynamicSpline(QChart):
    def __init__(self):
        super().__init__()
        self.m_step = 0
        self.m_x = 2
        self.m_y = 1
        # Инициализировать изображение
        self.series = QSplineSeries(self)
        red_pen = QPen(Qt.red)
        red_pen.setWidth(2)
        self.series.setPen(red_pen)
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        self.series.append(self.m_x, self.m_y)

        self.addSeries(self.series)
        self.addAxis(self.axisX, Qt.AlignBottom)
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)
        self.axisX.setTickCount(5)
        self.axisX.setRange(0, 10)
        self.axisY.setRange(0, 100)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.start()


    def handleTimeout(self):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y

        # В PyQt 5.11.3 и выше, QRandomGenerator.global() был переименован в global_()
        try:
            self.m_y=db_wrk()
        except :
            self.m_y = QRandomGenerator.global_().bounded(50)
        self.series.append(self.m_x, self.m_y)
        self.scroll(x, 0)
        if self.m_x >= 10:
            self.timer.stop()

    def db_wrk():

        return m_y


      

def t_db():
    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('data_set')
    client.switch_database('data_set')
    tik=0
    json_body=[]
    while tik<=10:
        for i in [j for j in range(11)]:
            little={
                    "measurement": "sec_table",
                    "tags": {
                            "param": i,
                            "tik" : tik
                    },
                    "fields": {
                        "value": int(randint(0, 100))
                    }
                }
            # print(tik,':',little['tags'],little['fields'])
            json_body.append(little)
        tik+=1
        # sleep(1)
    # print(json_body)
    client.write_points(json_body)
    results = client.query('select * from sec_table')
    points=results.get_points(tags={'tik':'1'})
    for i in points:
        print(i)
    # try:
           

    #     # print(client.get_list_database())
    # except:
    #     print('someting wrong')


def main():
    app = QApplication(sys.argv)
    chart = DynamicSpline()
    chart.setTitle("Dynamic spline chart")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing) 
    view.resize(1000, 500)
    view.show()
    sys.exit(app.exec_())
    # t_db()


if __name__ == "__main__":
    main()
