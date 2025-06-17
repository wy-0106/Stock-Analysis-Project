# views.py
from collections import defaultdict
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from plotly.offline import plot
from plotly.subplots import make_subplots
from .models import TopVolume
import pytz
import plotly.graph_objs as go

# Charts for project_tmx_money_analysis_main.html
def project_tmx_money_analysis_main(request):

    toronto_tz = pytz.timezone("America/Toronto")

    local_now = timezone.localtime(timezone.now(), toronto_tz)

    today = local_now.date()

    qs_today = TopVolume.objects.filter(Date=today)

    if not qs_today.exists():
        
        today = local_now.date() - timedelta(days=1)

    qs_today = TopVolume.objects.filter(Date=today)
    
    symbol_dict = {}

    for record in qs_today.order_by('-Percentage_Net_Change'):

        if record.Symbol not in symbol_dict:

            symbol_dict[record.Symbol] = record

        if len(symbol_dict) >= 5:

            break

    top_symbols = list(symbol_dict.keys())

    start_date = today - timedelta(days=89)

    qs_range = TopVolume.objects.filter(Symbol__in=top_symbols, Date__gte=start_date, Date__lte=today).order_by('Date')

    data_by_symbol = {}

    for record in qs_range:

        sym = record.Symbol

        if sym not in data_by_symbol:

            data_by_symbol[sym] = {'dates': [], 'prices': [], 'volumes': [], 'chg': []}

        data_by_symbol[sym]['dates'].append(record.Date)

        data_by_symbol[sym]['prices'].append(record.Price)

        data_by_symbol[sym]['volumes'].append(record.Volume)

        data_by_symbol[sym]['chg'].append(record.Percentage_Net_Change)

    # Chart 1: Price and Volume Trends
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    colors_line = ["#0ABAB5", "#EE6E00", "#E74C3C", "#2ECC71", "#9B59B6"]
    colors_bar = ["#0ABAB5", "#EE6E00", "#E74C3C", "#2ECC71", "#9B59B6"]

    for idx, (sym, data) in enumerate(data_by_symbol.items()):

        fig.add_trace(

            go.Scatter(

                x=data['dates'],

                y=data['prices'],

                mode='lines+markers',

                name=f"{sym} Price",

                line=dict(color=colors_line[idx % len(colors_line)], width=2),

                marker=dict(size=6),

                hovertemplate=f"Symbol: {sym}<br>Date: %{{x}}<br>Price: %{{y}}<extra></extra>"

            ),

            secondary_y=False
        )

        fig.add_trace(
            
            go.Bar(
                
                x=data['dates'],
                
                y=data['volumes'],
                
                name=f"{sym} Volume",
                
                marker=dict(color=colors_bar[idx % len(colors_bar)]),
                
                opacity=0.6,

                hovertemplate=f"Symbol: {sym}<br>Date: %{{x}}<br>Volume: %{{y}}<extra></extra>"
                
            ),
            
            secondary_y=True
            
        )

    range_7d = [str(today - timedelta(days=6)), str(today)]
    range_1m = [str(today - timedelta(days=29)), str(today)]
    range_3m = [str(today - timedelta(days=89)), str(today)]

    fig.update_layout(

        title=dict(text = "<b>Top 5 Volume Stocks: 7-Day Price &amp; Volume Trends</b>", 
                   x = 0.5),

        height=700,

        template="plotly_white",

        paper_bgcolor="#EEEAE6",

        plot_bgcolor="#EEEAE6",

        font=dict(family="Optima, Georgia, serif", size=16, color="#000000"),


        updatemenus=[

            {

                "type": "buttons",

                "direction": "left",

                "font": {"size": 24},

                "bgcolor": "#EEEAE6",

                "buttons": [

                    {
                        "label": "7D",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_7d,
                                  "title.text": "<b>Top 5 Volume Stocks: 7-Day Price &amp; Volume Trends</b>"}]
                    },
                    
                    {
                        "label": "1M",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_1m,
                                  "title.text": "<b>Top 5 Volume Stocks: 1-Month Price &amp; Volume Trends</b>"}]
                    },

                    {
                        "label": "3M",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_3m,
                                  "title.text": "<b>Top 5 Volume Stocks: 3-Month Price &amp; Volume Trends</b>"}]
                    }

                ],

                "pad": {"r": 10, "t": 10},

                "showactive": True,

                "x": 0.5,

                "xanchor": "center",

                "y": -0.15,

                "yanchor": "top"

            }
        ]
    )

    fig.update_xaxes(title_text="Date", showgrid=False)

    fig.update_yaxes(title_text="Price ($)", secondary_y=False, showgrid=False)

    fig.update_yaxes(title_text="Volume (Shares)", secondary_y=True, showgrid=False)

    chart_div_price_volume = plot(fig, output_type='div', include_plotlyjs=False)

    # Chart 2:  Percentage Net Change Trends
    fig2 = go.Figure()

    colors_line = ["#0ABAB5", "#EE6E00", "#E74C3C", "#2ECC71", "#9B59B6"]

    for idx, (sym, data) in enumerate(data_by_symbol.items()):

        fig2.add_trace(

            go.Scatter(

                x=data['dates'],

                y=data['chg'],

                mode='lines+markers',

                name=f"{sym} % Change",

                line=dict(color=colors_line[idx % len(colors_line)], width=2),

                marker=dict(size=6),

                hovertemplate=f"Symbol: {sym}<br>Date: %{{x}}<br>Percentage Net Change: %{{y}}%<extra></extra>"

            )

        )

    range_7d = [str(today - timedelta(days=6)), str(today)]
    range_1m = [str(today - timedelta(days=29)), str(today)]
    range_3m = [str(today - timedelta(days=89)), str(today)]

    fig2.update_layout(

        title=dict(text="<b>Top 5 Volume Stocks: 7-Day Percentage Net Change Trends</b>", x=0.5),

        height=700,

        template="plotly_white",

        paper_bgcolor="#EEEAE6",

        plot_bgcolor="#EEEAE6",

        font=dict(family="Optima, Georgia, serif", size=16, color="#000000"),

        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "font": {"size": 24},
                "bgcolor": "#EEEAE6",
                "buttons": [
                    {
                        "label": "7D",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_7d,
                                "title.text": "<b>Top 5 Volume Stocks: 7-Day Percentage Net Change Trends</b>"}]
                    },

                    {
                        "label": "1M",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_1m,
                                "title.text": "<b>Top 5 Volume Stocks: 1-Month Percentage Net Change Trends</b>"}]
                    },

                    {
                        "label": "3M",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_3m,
                                "title.text": "<b>Top 5 Volume Stocks: 3-Month Percentage Net Change Trends</b>"}]
                    }

                ],

                "pad": {"r": 10, "t": 10},

                "showactive": True,

                "x": 0.5,

                "xanchor": "center",

                "y": -0.15,

                "yanchor": "top"

            }

        ]

    )

    fig2.add_shape(

        type="line",

        xref="paper",

        x0=0,

        x1=1,

        yref="y",

        y0=0,

        y1=0,

        line=dict(color="#000000", width=2, dash="dash")

        )

    fig2.update_xaxes(title_text="Date", showgrid=False)

    fig2.update_yaxes(title_text="% Net Change", showgrid=False)

    chart_div_percentage_net_change = plot(fig2, output_type='div', include_plotlyjs=False)

    # Chart 3 Frequency: Top vs. Bottom Comparison: 

    qs_all = TopVolume.objects.all()

    total_days = TopVolume.objects.values_list('Date', flat=True).distinct().count()

    symbol_days = defaultdict(set)

    for record in qs_all:

        symbol_days[record.Symbol].add(record.Date)

    symbol_frequency = {symbol: len(days) / total_days * 100 for symbol, days in symbol_days.items()}

    sorted_symbols_desc = sorted(symbol_frequency.items(), key=lambda x: x[1], reverse=True)

    top_symbols = sorted_symbols_desc[:10]

    sorted_symbols_asc = sorted(symbol_frequency.items(), key=lambda x: x[1])

    bottom_symbols = sorted_symbols_asc[:10]

    top_sym_names = [item[0] for item in top_symbols]

    top_percentages = [item[1] for item in top_symbols]

    top_hover = [f"Symbol: {item[0]}<br>Frequency: {item[1]:.2f}%" for item in top_symbols]

    bottom_sym_names = [item[0] for item in bottom_symbols]

    bottom_percentages = [item[1] for item in bottom_symbols]

    bottom_hover = [f"Symbol: {item[0]}<br>Frequency: {item[1]:.2f}%" for item in bottom_symbols]

    max_val = max(max(top_percentages), max(bottom_percentages))

    fig3 = go.Figure()

    fig3.add_trace(

        go.Bar(

            x=top_percentages,

            y=top_sym_names,

            orientation='h',

            name='Top Frequency',

            marker=dict(

                color=top_percentages,

                colorscale=[[0, '#0ABAB5'], [1, '#0A92B1']],

                cmin=min(top_percentages),

                cmax=max(top_percentages)

            ),

            hovertemplate='%{hovertext}<extra></extra>',

            hovertext=top_hover

        )

    )

    fig3.add_trace(

        go.Bar(

            x=[-val for val in bottom_percentages],

            y=bottom_sym_names,

            orientation='h',

            name='Bottom Frequency',

            marker=dict(

                color=bottom_percentages,

                colorscale=[[0, '#EE6E00'], [1, '#E74C3C']],

                cmin=min(bottom_percentages),

                cmax=max(bottom_percentages)

            ),

            hovertemplate='%{hovertext}<extra></extra>',

            hovertext=bottom_hover

        )

    )

    fig3.update_layout(

        title=dict(text="<b>Frequency: Top vs. Bottom Comparison</b>", x=0.5),

        template="plotly_white",

        paper_bgcolor="#EEEAE6",

        plot_bgcolor="#EEEAE6",

        font=dict(family="Optima, Georgia, serif", size=16, color="#000000"),

        height=700,

        barmode='overlay'

    )

    fig3.update_xaxes(

        range=[-max_val * 1.1, max_val * 1.1],

        tickvals=[-max_val, -max_val/2, 0, max_val/2, max_val],

        ticktext=[f"{max_val:.1f}", f"{max_val/2:.1f}", "0", f"{max_val/2:.1f}", f"{max_val:.1f}"],

        title_text="Frequency (%)"

    )

    fig3.add_shape(

        type="line",

        x0=0,

        y0=-0.5,

        x1=0,

        y1=len(top_sym_names) + len(bottom_sym_names) - 0.5,

        xref="x",

        yref="y",

        line=dict(color="#000000", width=2, dash="dash")

    )

    desired_order = bottom_sym_names + top_sym_names

    fig3.update_yaxes(categoryorder="array", categoryarray=desired_order)

    chart_div_frequency = plot(fig3, output_type='div', include_plotlyjs=False)

    # Table
    latest_data = {}

    for record in qs_today:

        sym = record.Symbol

        if sym not in latest_data or record.Date > latest_data[sym].Date:

            latest_data[sym] = record

    latest_data_list = list(latest_data.values())

    context = {

        'chart_div_price_volume': chart_div_price_volume,

        'chart_div_percentage_net_change': chart_div_percentage_net_change,

        'chart_div_frequency': chart_div_frequency,

        'latest_data': latest_data_list,
    }

    return render(request, 'project_tmx_money_analysis/project_tmx_money_analysis_main.html', context)

# Charts for stock_detail.html
def stock_detail(request, symbol):

    qs = TopVolume.objects.filter(Symbol=symbol).order_by('Date')

    dates = [record.Date for record in qs]
    prices = [record.Price for record in qs]
    volumes = [record.Volume for record in qs]
    

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(

        go.Scatter(

            x=dates,

            y=prices,

            mode='lines+markers',

            name=f"{symbol} Price",

            line=dict(color="#0A92B1", width=2),

            marker=dict(size=6),

            hovertemplate=f"Date: %{{x}}<br>Price: %{{y}}<extra></extra>"

        ),

        secondary_y=False
    )
    

    fig.add_trace(

        go.Bar(

            x=dates,

            y=volumes,

            name=f"{symbol} Volume",

            marker=dict(color="#0ABAB5"),

            opacity=0.6,

            hovertemplate=f"Date: %{{x}}<br>Volume: %{{y}}<extra></extra>"

        ),

        secondary_y=True

    )
    
    today = dates[-1]
    range_7d = [str(today - timedelta(days=6)), str(today)]
    range_1m = [str(today - timedelta(days=29)), str(today)]
    range_3m = [str(today - timedelta(days=89)), str(today)]


    fig.update_layout(

        title=dict(text=f"<b>{symbol} Price and Volume Trends For 7 Days</b>", x=0.5),

        height=600,

        template="plotly_white",

        paper_bgcolor="#EEEAE6",

        plot_bgcolor="#EEEAE6",

        font=dict(family="Optima, Georgia, serif", size=16, color="#000000"),

        updatemenus=[

            {
                "type": "buttons",

                "direction": "left",

                "font": {"size": 24},

                "bgcolor": "#EEEAE6",

                "buttons": [
                    {
                        "label": "7D",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_7d,
                                  "title.text": f"<b>{symbol} Price and Volume Trends For 7 Days</b>"}]
                    },

                    {
                        "label": "1M",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_1m,
                                  "title.text": f"<b>{symbol} Price and Volume Trends For 1-Month</b>"}]
                    },

                    {
                        "label": "3M",
                        "method": "relayout",
                        "args": [{"xaxis.range": range_3m,
                                  "title.text": f"<b>{symbol} Price and Volume Trends For 3-Month</b>"}]
                    }
                ],

                "pad": {"r": 10, "t": 10},

                "showactive": True,

                "x": 0.5,

                "xanchor": "center",

                "y": -0.2,

                "yanchor": "top"
            }
        ]
    )
    
    fig.update_xaxes(title_text="Date", showgrid=False)

    fig.update_yaxes(title_text="Price ($)", secondary_y=False, showgrid=False)

    fig.update_yaxes(title_text="Volume (Shares)", secondary_y=True, showgrid=False)
    
    chart_div = plot(fig, output_type='div', include_plotlyjs=False)
    
    context = {

        'symbol': symbol,

        'chart_div': chart_div,

        'historical_data': qs,

    }
    
    return render(request, 'project_tmx_money_analysis/stock_detail.html', context)