"""
    pbm.views
    
"""
import logging
import pytz
from datetime import datetime, timedelta

from django.db.models import Count, Sum
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader

from .models import DailyLog
from .utils import CATEGORY_LABELS, PLOT_TITLES, PLOT_UNITS, COLORS, \
defaultDatetimeFormat, configure, configure_plot, \
prepare_data_for_piechart, prepare_colors_for_piechart, \
data_plot_groupby_category, plot

_logger = logging.getLogger('bigpandamon-pbm')


def index(request):
    """
        index -- pbm's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    ### configure time interval for queries
    startdate, enddate, ndays, errors_GET = configure(request.GET)

    ### start the query parameters
    query={}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]

    ### filter category__in
    query['category__in'] = ['A', 'B', 'C']

    ### User selected a site/User selected a cloud/Panda Brokerage decision
    ###     Plot 1: [User selected a site/User selected a cloud/Panda Brokerage decision] on Jobs
    data01, colors01, title01, unit01 = plot('01', query)

    ###     Plot 2: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobDef
    data02, colors02, title02, unit02 = plot('02', query)

    ###     Plot 3: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobSet
    data03, colors03, title03, unit03 = plot('03', query)


    ### User selected a site - Top sites > 1 %
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'A'
    query['category'] = 'A'
    ###     Plot 4: [User selected a site] on Jobs - Top sites > 1 %
    data04, colors04, title04, unit04 = plot('04', query)

    ###     Plot 5: [User selected a site] on jobDef - Top sites > 1 %
    data05, colors05, title05, unit05 = plot('05', query)

    ###     Plot 6: [User selected a site] on jobSet - Top sites > 1 %
    data06, colors06, title06, unit06 = plot('06', query)


#    ### User selected a site - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'A'
    query['category'] = 'A'
    ###     Plot 7: [User selected a site] on Jobs - Per cloud
    data07, colors07, title07, unit07 = plot('07', query)

    ###     Plot 8: [User selected a site] on jobDef - Per cloud
    data08, colors08, title08, unit08 = plot('08', query)

    ###     Plot 9: [User selected a site] on jobSet - Per cloud
    data09, colors09, title09, unit09 = plot('09', query)


    ### User selected a cloud - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'B'
    query['category'] = 'B'
    ###     Plot 13: [User selected a cloud] on Jobs - Per cloud
    data13, colors13, title13, unit13 = plot('13', query)

    ###     Plot 14: [User selected a cloud] on jobDef - Per cloud
    data14, colors14, title14, unit14 = plot('14', query)

    ###     Plot 15: [User selected a cloud] on jobSet - Per cloud
    data15, colors15, title15, unit15 = plot('15', query)


    ### PanDA Brokerage decision - Top sites with share > 1 %
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'B'
    query['category'] = 'C'
    ###     Plot 16: PanDA Brokerage decision on Jobs - Top sites with share > 1 %
    data16, colors16, title16, unit16 = plot('16', query)

    ###     Plot 17: PanDA Brokerage decision on JobDefs - Top sites with share > 1 %
    data17, colors17, title17, unit17 = plot('17', query)


    ### PanDA Brokerage decision  - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'C'
    query['category'] = 'C'
    ###     Plot 18: PanDA Brokerage decision  on Jobs - Per cloud
    data18, colors18, title18, unit18 = plot('18', query)

    ###     Plot 19: PanDA Brokerage decision  on jobDef - Per cloud
    data19, colors19, title19, unit19 = plot('19', query)


    ### User excluded a site on distinct jobSet - With exclude / Without exclude
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['A', 'B', 'C', 'E']
    ###     Plot 20: User excluded a site on distinct jobSet - With exclude / Without exclude
    data20, colors20, title20, unit20 = plot('20', query)


    ### User excluded a site on jobSet - Top sites with share > 1 %
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['E']
    ###     Plot 21: User excluded a site on jobSet - Top sites with share > 1 %
    data21, colors21, title21, unit21 = plot('21', query)

    ###     Plot 22: User excluded a site on distinct DnUser - Top sites with share > 1 %
    data22, colors22, title22, unit22 = plot('22', query)


    ### User excluded a site on jobSet - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['E']
    ###     Plot 23: User excluded a site on jobSet - Per cloud
    data23, colors23, title23, unit23 = plot('23', query)

    ###     Plot 24: User excluded a site on distinct DnUser - Per cloud
    data24, colors24, title24, unit24 = plot('24', query)


    ### Submitted by Country (from UserDN)
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['A', 'B', 'C', 'E']
    ###     Plot 25: Jobs submitted by Country
    data25, colors25, title25, unit25 = plot('25', query)


    ###     Plot 26: JobDefs submitted by Country
    data26, colors26, title26, unit26 = plot('26', query)


    ###     Plot 27: JobSets submitted by Country
    data27, colors27, title27, unit27 = plot('27', query)


    ### set request response data
    data = { \
        'errors_GET': errors_GET,
        'startdate': startdate,
        'enddate': enddate,
        'ndays': ndays,

        'data01': prepare_data_for_piechart(data=data01, unit=unit01),
        'title01': title01,
        'colors01': colors01,
        'data02': prepare_data_for_piechart(data=data02, unit=unit02),
        'title02': title02,
        'colors02': colors02,
        'data03': prepare_data_for_piechart(data=data03, unit=unit03),
        'title03': title03,
        'colors03': colors03,

        'data04': prepare_data_for_piechart(data=data04, unit=unit04, cutoff=1.0),
        'title04': title04,
        'colors04': colors04,
        'data05': prepare_data_for_piechart(data=data05, unit=unit05),
        'title05': title05,
        'colors05': colors05,
        'data06': prepare_data_for_piechart(data=data06, unit=unit06),
        'title06': title06,
        'colors06': colors06,

        'data07': prepare_data_for_piechart(data=data07, unit=unit07),
        'title07': title07,
        'colors07': colors07,
        'data08': prepare_data_for_piechart(data=data08, unit=unit08),
        'title08': title08,
        'colors08': colors08,
        'data09': prepare_data_for_piechart(data=data09, unit=unit09),
        'title09': title09,
        'colors09': colors09,

        'data13': prepare_data_for_piechart(data=data13, unit=unit13),
        'title13': title13,
        'colors13': colors13,
        'data14': prepare_data_for_piechart(data=data14, unit=unit14),
        'title14': title14,
        'colors14': colors14,
        'data15': prepare_data_for_piechart(data=data15, unit=unit15),
        'title15': title15,
        'colors15': colors15,

        'data16': prepare_data_for_piechart(data=data16, unit=unit16, cutoff=1.0),
        'title16': title16,
        'colors16': colors16,
        'data17': prepare_data_for_piechart(data=data17, unit=unit17, cutoff=1.0),
        'title17': title17,
        'colors17': colors17,

        'data18': prepare_data_for_piechart(data=data18, unit=unit18),
        'title18': title18,
        'colors18': colors18,
        'data19': prepare_data_for_piechart(data=data19, unit=unit19),
        'title19': title19,
        'colors19': colors19,

        'data20': prepare_data_for_piechart(data=data20, unit=unit20),
        'title20': title20,
        'colors20': colors20,

        'data21': prepare_data_for_piechart(data=data21, unit=unit21, cutoff=1.0),
        'title21': title21,
        'colors21': colors21,
        'data22': prepare_data_for_piechart(data=data22, unit=unit22, cutoff=1.0),
        'title22': title22,
        'colors22': colors22,
        'data23': prepare_data_for_piechart(data=data23, unit=unit23),
        'title23': title23,
        'colors23': colors23,
        'data24': prepare_data_for_piechart(data=data24, unit=unit24),
        'title24': title24,
        'colors24': colors24,

        'data25': prepare_data_for_piechart(data=data25, unit=unit25, cutoff=1.0),
        'title25': title25,
        'colors25': colors25,
        'data26': prepare_data_for_piechart(data=data26, unit=unit26, cutoff=1.0),
        'title26': title26,
        'colors26': colors26,
        'data27': prepare_data_for_piechart(data=data27, unit=unit27, cutoff=1.0),
        'title27': title27,
        'colors27': colors27,

    }
    return render_to_response('pbm/index.html', data, RequestContext(request))


def single_plot(request):
    """
        single_plot -- pbm's page to view 1 plot
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    ### configure time interval for queries
    startdate, enddate, ndays, errors_GET = configure(request.GET)
    plotid = configure_plot(request.GET)

    ### start the query parameters
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]

    dataX, colorsX, titleX, unitX = plot(plotid, query)


    ### set request response data
    data = { \
        'errors_GET': errors_GET,
        'startdate': startdate,
        'enddate': enddate,
        'ndays': ndays,

        'dataX': prepare_data_for_piechart(data=dataX, unit=unitX),
        'titleX': titleX,
        'colorsX': colorsX,
        'plotid': plotid,

}
    return render_to_response('pbm/plot.html', data, RequestContext(request))


def single_table(request):
    """
        single_table -- pbm's page to view tabular data of a plot
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    ### configure time interval for queries
    startdate, enddate, ndays, errors_GET = configure(request.GET)
    plotid = configure_plot(request.GET)

    ### start the query parameters
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]

    dataX, colorsX, titleX, unitX = plot(plotid, query)


    ### set request response data
    data = { \
        'errors_GET': errors_GET,
        'startdate': startdate,
        'enddate': enddate,
        'ndays': ndays,

        'dataX': prepare_data_for_piechart(data=dataX, unit=unitX),
        'titleX': titleX,
        'colorsX': colorsX,
        'plotid': plotid,

}
    return render_to_response('pbm/table.html', data, RequestContext(request))


