from flask import Flask
from flask import request
from flask import render_template
import json

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def about():
    f = open("data/CommutingModes.json","r")
    data = json.load(f)
    f.close()


    return render_template('about.html')

@app.route('/macro')
def macro():
    f = open("data/CommutingModes.json","r")
    data = json.load(f)
    f.close()

    boroughs = data["2017-21"]["Borough"].keys()
    CTV_borough_data = {}
    for borough in boroughs:
        CTV_borough_data[borough] = data["2017-21"]["Borough"][borough]["Car_truck_van_Percent"]

    #define legend 
    percent_range = [
        (0,12), (13, 24), (25, 36), (37, 48), (49, 60), (61, 72), (73, 84), (84, float("inf"))
    ]
    #labels on legend
    legend_increments = []
    for lo, hi in percent_range: 
        if lo == -float("inf"):
            label = f"<{hi}"
        elif hi == float("inf"):
            label = f">{lo}"
        else:
            label = f"{lo}-{hi - 1}"
        legend_increments.append(label)
    #define legend colors
    legend_color = []
    for i, _ in enumerate(legend_increments):
        color_saturation = f"hsl(120,{int(100 / len(legend_increments) * (i + 1))}%,{100-int(100 / len(legend_increments) * (i + 1))}%)"
        legend_color.append(color_saturation)

    min, max = None, None
    min_borough, max_borough = None, None
    three_take_aways = []

    #match borough to color
    borough_color = {}
    for borough in CTV_borough_data:
        CVT_percent = float(CTV_borough_data[borough])
        #max and min statistics
        if max is None or CVT_percent > max:
            max, max_borough = CVT_percent, borough
        if min is None or CVT_percent < min:
            min, min_borough = CVT_percent, borough
        #color
        for i, (lower, upper) in enumerate(percent_range):
            if lower <= float(CTV_borough_data[borough]) <= upper:
                borough_color[borough] = legend_color[i]
        #matching borough percent to its color
        for i, (lower, upper) in enumerate(percent_range):
            if lower <= float(CTV_borough_data[borough]) <= upper:
                borough_color[borough] = legend_color[i]

        text_based_interpretation = [f'''Noticeably, {str(max_borough)}, with a percent of {str(max)}%, has the greatest percent 
                                 of people who use cars, vans, or trucks to commute to work, whereas {str(min_borough)}, with a percent of {min}% 
                                 has the lowest percent of people who use these motor vehicles to commute to work.''']
    
    return render_template(
        'macro.html',
        three_take_aways = three_take_aways,
        text_based_interpretation=text_based_interpretation,
        max_borough=max_borough,
        min_borough=min_borough, 
        manhattan_color=borough_color["Manhattan"], 
        brooklyn_color=borough_color["Brooklyn"], 
        bronx_color=borough_color["Bronx"], 
        queens_color=borough_color["Queens"],
        staten_island_color=borough_color["Staten Island"],
        legend_color=legend_color,
        legend_increments=legend_increments
    )
    
@app.route('/micro/<borough>')
def micro(borough):
    f = open("data/CommutingModes.json","r")
    data = json.load(f)
    f.close()


    #bar chart data:
    #identify which borough + gather data for the barchart
    if borough != "statenisland":
        requested_borough = borough.capitalize()
    elif borough == "statenisland": 
        requested_borough = "Staten Island"
    needed_inner_dictionary = data["2017-21"]["Borough"][requested_borough]

    CVT_percent = float(needed_inner_dictionary["Car_truck_van_Percent"])
    Bicycle_percent = float(needed_inner_dictionary["Bicycle_Percent"])
    Public_transportation_Percent = float(needed_inner_dictionary["Public_transportation_Percent"])
    Walked_Percent = float(needed_inner_dictionary["Walked_Percent"])
    
    #calculate datapoints
    bar_labels = [CVT_percent,Public_transportation_Percent, Walked_Percent,Bicycle_percent]
    percentages = []
    for transport_mode_percent in bar_labels:
        y_value = transport_mode_percent*5
        percentages.append(y_value)


    #calculate average statistics
    boroughs = data["2017-21"]["Borough"].keys()

    CTV_borough_data = {}
    for borough in boroughs:
        CTV_borough_data[borough] = data["2017-21"]["Borough"][borough]["Car_truck_van_Percent"]
    total = 0
    for borough in CTV_borough_data:
        total += float(CTV_borough_data[borough])
    average = total/5
    #auto generate qualitative analysis
    average_stats = [] 
    for borough in CTV_borough_data:
        CVT_percent = float(CTV_borough_data[borough])
        if CVT_percent >= (average+20):
            analysis = f" the percent of people in {borough} who commute to work using these motor vehicles is significantly greater than the average"
            average_stats.append(analysis) 
        elif average < CVT_percent < (average+20):
            analysis = f" the percent of people in {borough} who commute to work using these motor vehicles is slightly greater than the average"
            average_stats.append(analysis) 
        elif (average-5) < CVT_percent <= average:
            analysis = f" the percent of people in {borough} who commute to work using these motor vehicles is slightly lower than the average"
            average_stats.append(analysis)
        elif (average-30) < CVT_percent <= (average-5):
            analysis = f" the percent of people in {borough} who commute to work using these motor vehicles is significantly lower than the average"
            average_stats.append(analysis)
        elif CVT_percent == average:
            analysis = f" the percent of people in {borough} who commute to work using these motor vehicles is equal to the average"
            average_stats.append(analysis)
        
    all_borough_CVT_average_comparison = [f'''The average percent of people across all the boroughs of New York City who commute to work using 
                            cars, vans, or trucks is {average}%. Considering each borough, 
                            {average_stats[0]},
                            {average_stats[1]},
                            {average_stats[2]},
                            {average_stats[3]},
                            {average_stats[4]}.
                            ''']
    
    autogenerated_textbased_fragment = "test"
    for stat in average_stats:
        words = stat.split()
        if requested_borough != "Staten Island":
            if requested_borough in words:
                autogenerated_textbased_fragment = stat
        elif requested_borough == "Staten Island":
            if "Staten" in words:
                autogenerated_textbased_fragment = stat

    autogenerated_textbased_interpretation = f'''The average percent of people across all the boroughs of New York City who commute to work using 
                            cars, vans, or trucks is {average}%. Here, we see that {autogenerated_textbased_fragment}.'''

    x_axis_increments = ["Cars, Vans, or Trucks","Public Transportation","Walking","Bicycling"]
    y_axis_increments = [10,20,30,40,50,60,70,80]

    return render_template('micro.html',
                           x_axis_increments = x_axis_increments,
                           y_axis_increments = y_axis_increments,
                           requested_borough=requested_borough,
                           boroughs=boroughs,
                           autogenerated_textbased_interpretation=autogenerated_textbased_interpretation,
                           bar_y_values = percentages,                          
                           bar_labels = bar_labels
    )

app.run(debug=True, port = 1243)
