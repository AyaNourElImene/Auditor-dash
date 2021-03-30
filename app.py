

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, ClientsideFunction

import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib
import dash_table as dtt
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()




# Read data
# ads= pd.read_csv(DATA_PATH.joinpath("ads.csv"))
ads= pd.read_json(DATA_PATH.joinpath("ads_data.json"))

advertiser_list=ads["title"].unique().tolist()
ads['label'] = ads['label'].map({'str_p':'Strong Political (fraction=1)',
                             'str_np':'Non-political (fraction=0 ) ',
                             'p':'Political (1 < fraction <= 0.5)',
                             'np':'Marginally Political  (0.5< fraction <0)'},
                             na_action=None)
label_list=ads["label"].unique().tolist()  
#ads['paid_for_by'] = ads['paid_for_by'].replace(['this is empty'],['None'])
                            
paid_list=ads["paid_for_by"].unique().tolist() 
ads['fin_ctg'] = ads['fin_ctg'].replace(['disagreement','This ad is about environmental politics','This ad is about education','This ad is about civil and social rights','This ad is about health' , 'This ad is about economy' , 'This ad is about immigration', 'This ad is about security and foreign policy' , 'This ad is about crime', 'This ad is about political values and governance', 'This ad is about guns' ], ['Disagreement','Social Issue : Environmental Politics','Social Issue : Education','Social Issue : Civil and Social Rights','Social Issue : Health', 'Social Issue : Economy' , 'Social Issue : Immigration' , 'Social Issue : Security and Foreign Policy','Social Issue : Crime','Social Issue : Political Values and Governance', 'Social Issue : Guns'] )
ctg_list=ads["fin_ctg"].unique().tolist()     

# ads["created_at"] = ads["created_at"].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))

ads.fr=ads.fr*100
ads.fr=ads.fr.apply(np.floor)
ads.fr
fr_list=ads["fr"].tolist()   

ads['sponsor']=ads['paid_for_by']
ads['sponsor'] = ads['sponsor'].replace(['this is empty'],['None'])
ads.loc[ads.paid_for_by != 'this is empty','paid_for_by']='Yes'
ads.loc[ads.paid_for_by != 'Yes','paid_for_by']='No'


advcategory_list=ads['categories_1'].unique().tolist()

data_columns = ['Ad message','Advertiser', 'Labeled as political by advertiser',  'Advertiser Webpage','Targeting' ,'Fraction of political votes from citizens(%)']
df_columns = ['text','title', 'paid_for_by', 'page','targets', 'fr']





all_departments = ads.to_dict(orient="records")
 

wait_time_inputs = [] #[Input((i + "_wait_time_graph"), "selectedData") for i in ["1,2",]]
score_inputs = []# [Input((i + "_score_graph"), "selectedData") for i in ["er",]]




def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            #html.H5("Political Ads Analytics"),
            html.H3("Welcome to the Political ads Dashboard"),
            html.Div(
                id="intro",
                children="Explore what ads are labeled as political by citizens and advertisers.",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """

     

    return html.Div(
        id="control-card",
        children=[
            
            html.P("Dissagreement among citizens"),
 
            html.Div(children='(Fraction of political votes from citizens) ', style={
        'textAlign': 'left',
        'color':'rgb(128,128,128)',
    }),

            dcc.Dropdown(
                id="Label_select",
                options=[{"label": i, "value": i} for i in sorted(ads["label"].unique().tolist())],
                multi=True,
                value=[],
                                 style={'width': '350px'},


               
            ),
            html.Br(),
             html.P("Social or Political issue "),
            dcc.Dropdown(
                id="category_select",
                options=[{"label": i, "value": i} for i in sorted(ads["fin_ctg"].unique().tolist())],
                value=[],
                                 style={'width': '350px'},

                
                multi=True,
                
            ),
            html.Br(),
            html.P("Advertiser Category"),
            dcc.Dropdown(
                id="advcategory_select",
                 value=[],
                options=[{"label": i, "value": i} for i in sorted(ads["categories_1"].unique().tolist())],
                 style={'width': '350px'},
                multi=True,
            ),
            
            html.Br(),
           html.P("Advertiser"),
            dcc.Dropdown(
                id="advertiser_select",
                 value=[],
                options=[{"label":"All","value":"all"},*[{"label": i, "value": i} for i in sorted(ads["title"].unique().tolist())]],
                 style={'width': '350px'},
                multi=True,
            ),
            html.Br(),
            html.P("Labeled as Political by advertiser "),
            dcc.Checklist(
                id="labeled_by_advertiser_select",
                value=[],
                options=[{"label": i, "value": i} for i in ads["paid_for_by"].unique().tolist()],
                 style={'width': '400px',
      },
               labelStyle={'width': '100px','display': 'inline-block'},
               
                #optionHeight=55
            ),
             html.Br(),
             html.P("Sponsor "),
           dcc.Dropdown(
               id="paid_select",
                        
                         options=[{"label": i, "value": i} for i in sorted(ads["sponsor"].unique().tolist())],
                      value=[],
                 style={'width': '350px' ,  'wordBreak': 'break-all'},
                multi=True,
           ),
           html.Br(),

          
           
          
         
        ],
    )






app.layout = html.Div(
    id="app-container",
    children=[
     
  html.Div(
               
                className="banner",
                id="app-header",
                style={"background-color": "#f9f9f9"},
                children=[
                    html.A(
                        [
                                         html.Img( 
                                            #  src='https://pbs.twimg.com/profile_images/1216754056619864064/YgAhO3fC_400x400.jpg',
                                            src='https://www.univ-grenoble-alpes.fr/uas/SITEUI/LOGO/logo+bleu.svg',

                                         style={'height':'100px', 'width':'100px',"margin-top":"22px",'textAlign': 'left'}
                                         ),

                        ],
                       
                        className="four columns header_img",
                         href='https://www.univ-grenoble-alpes.fr',
                    ),
                    html.Div(
                        [
                            html.H2(
                                "Explore disagreement in political ads labeling ",
                                className="header_title",
                                id="app-title",
                            ) , 
                        ],
                       style={'textAlign': 'center', 'color' : 'rgb(44, 140, 255)' }
                    ),
                ],
            ),
        
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
            
        ),
        # Right column
        
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                                html.Div( 
                                    children=[
                                        html.H4("Results for Political ads"),
                                        html.P(children=[
                                            html.Span("0 ",id="count"),
                                            html.Span("ads found ."),
                                            ],id="count-container")
                                     ]),


                # Patient Wait time by Department
                html.Div(
                    id="wait_time_card",
                    children=[
                        
                        html.Hr(),
                        
                        html.Div( 
                            children=[
                            html.Div([
                            
                                dtt.DataTable( 
                                
                                id="my_datatable",
page_size= 9999 ,
    #   pagination_settings={'page_size': 9999999999},
                               sort_action="native",
                            
                                columns=[{ 'name': col, 'id': df_columns[idx] } for (idx, col) in enumerate(data_columns)],
                                #columns =[{'name': i, 'id': i} for i in ads.loc[:,['advertiser','text','page','fr']]],
                                #virtualization = True , 
                            
                                fixed_rows={'headers': True},
                               
                                style_table={'height':'500px',   },


                                 style_data_conditional=[
      					  {
           					 'if': {'row_index': 'odd'},
           					 'backgroundColor': 'rgb(248, 248, 248)'
       						 }
   								 ],
                                style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                 'fontWeight': 'bold',
                                 },
                                style_cell_conditional=[
                                                                                           
                                           

                                            {'if': {'column_id': 'text'},
                                             'width': '280px',
                                             'whiteSpace': 'normal',
                                                                                  'textAlign': 'center',

                                            },
                                              {'if': {'column_id': 'targets'},
                                             'width': '170px',
                                             'whiteSpace': 'normal',
                                             'textAlign': 'left'
                                            },
                                            {'if': {'column_id': 'title'},
                                             'width': '170px'
                                            },
                                             {'if': {'column_id': 'fr'},
                                             'width': '100px', 'textAlign': 'center',

                                            },
                                            {'if': {'column_id': 'page'},
                                              'width': '170px', 
                                              'wordBreak': 'break-all'
                                            },
                                            {'if': {'column_id': 'paid_for_by'},
                                              'width': '170px'
                                            }
                                    
                                          
                                          
                                     ],

                                style_cell= {
                                    #  'width':600,
                                     'textAlign': 'center',
                                    #  'display': 'auto',
                                    #  'flex-direction': 'column',
                                        'fontFamily': 'Open Sans',
                #'height': '60px',
               'padding': '10px 10px',
              'whiteSpace': 'normal',
                                                          
                                                            
                                 	  'font-size': '15px',
                                      },
                               
                              
                                ),
                            ]),
                            ],
                        ),
                    ],
                ),
               
                html.H4('Resources'),
                html.Div(
                     id= 'Resourc_section',  
                    children=[
                       html.Div(
                           id='data-ressource',
                           className='five columns',
                           children=[
                          html.B('These ads are extracted from  :'),
                          dcc.Markdown('''
                                    [The ProPublica dataset](https://www.propublica.org/datastore/dataset/political-advertisements-from-facebook)

                                    '''),
                        
                                   
                          html.B('Detailed measurement methodology and data analysis  :'),
                        dcc.Markdown('''
                                    [Understanding the Complexity of Detecting Political ads](http://lig-membres.imag.fr/gogao/papers/pol_ads_complexity_WWW2021.pdf)

                                    '''),
                         
                                      ], ),
                                   

                        html.Div(
                        id='def-ressource',
                                                   className='five columns',

                        children =
                        [html.B('Definitions of political ads :'),
                        dcc.Markdown('''
                                    1. [Facebook Definition for Political ads](https://www.facebook.com/business/help/167836590566506?id=288762101909005)
                                    2. [Google Definition for Political ads](https://support.google.com/adspolicy/answer/6014595?hl=en)
                                    3. [Twitter Definition for Political ads](https://business.twitter.com/en/help/ads-policies/ads-content-policies/political-content.html)
                                    4. [TikTok Definition for Political ads](https://ads.tiktok.com/help/article?aid=9550)
                                    '''),
                                    ],
                                    ),



                     ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output('count', 'children'),
[Input('my_datatable','data')],
)
def update_count(data):
    return f"{len(data)} "

@app.callback(
    Output('category_select', 'options'),
[Input('Label_select', 'value'),Input('Label_select', 'options')],
)
def update_output4(label_value,label_options):
    if len(label_value) == 0:
        addd4= ads[ads['label'].isin([x["value"] for x in label_options])]
    else:
        addd4= ads[ads['label'].isin(label_value)]
    return [{'label': i, 'value': i} for i in addd4['fin_ctg'].unique().tolist()]


@app.callback(
    Output('category_select', 'value'),
[Input('Label_select', 'value')],
)
def update_initialze_select(Label_select):
    return []



@app.callback(
    Output('advcategory_select', 'options'),
[Input('category_select', 'value'),Input('category_select', 'options')],
)
def update_output3(category_value,category_options):
    if len(category_value) == 0:
        addd= ads[ads['fin_ctg'].isin([x["value"] for x in category_options])]
    else:
        addd= ads[ads['fin_ctg'].isin(category_value)]
    return [{'label': i, 'value': i} for i in addd['categories_1'].unique().tolist()]

@app.callback(
    Output('advcategory_select', 'value'),
[Input('category_select', 'value')],
)
def update_output33(category_select):
      return []

@app.callback(
    Output('advertiser_select', 'options'),
[Input('advcategory_select', 'value'),Input('advcategory_select', 'options')],
)
def update_output1(advcategory_value,advcategory_options):
    if len(advcategory_value) == 0:
        addd= ads[ads['categories_1'].isin([x["value"] for x in advcategory_options])]
    else:
        addd= ads[ads['categories_1'].isin(advcategory_value)]
    return [{'label': i, 'value': i} for i in addd['title'].unique().tolist()]

@app.callback(
    Output('advertiser_select', 'value'),
[Input('advcategory_select', 'value')],
)
def update_output11(advcategory_select):
      return []

@app.callback(
    Output('paid_select', 'options'),
[Input('advertiser_select', 'value'),Input('advertiser_select', 'options')],
)
def update_output2(advertiser_value,advertiser_options):
    if len(advertiser_value) == 0:
        addd1= ads[ads['title'].isin([x["value"] for x in advertiser_options])]
    else:
         addd1= ads[ads['title'].isin(advertiser_value)]
    return [{'label': i, 'value': i} for i in sorted(addd1['sponsor'].unique().tolist())]
    

@app.callback(
    Output('paid_select', 'value'),
[Input('advertiser_select', 'value')]

)
def update_output22(advertiser_select):
    return []


   


@app.callback(
    Output('my_datatable','data'),
    [
        Input('advertiser_select','value'),
        Input('Label_select','value'),
        Input('category_select','value'),
        Input('paid_select','value'),
        Input('advcategory_select','value'),
        Input('labeled_by_advertiser_select','value'),



        



    ],
)
def update_output(advertiser_select, Label_select,category_select,paid_select,advcategory_select,labeled_by_advertiser_select):
   
    
    ad_mask = pd.DataFrame(data={"is_empty":[len(advertiser_select) == 0 for i in range(len(ads))]})
    Label_select_mask = pd.DataFrame(data={"is_empty":[len(Label_select) == 0 for i in range(len(ads))]})
    category_select_mask = pd.DataFrame(data={"is_empty":[len(category_select) == 0 for i in range(len(ads))]})
    paid_select_mask = pd.DataFrame(data={"is_empty":[len(paid_select) == 0 for i in range(len(ads))]})
    advcategory_select_mask = pd.DataFrame(data={"is_empty":[len(advcategory_select) == 0 for i in range(len(ads))]})
    labeled_by_advertiser_select_mask=pd.DataFrame(data={"is_empty":[len(labeled_by_advertiser_select) == 0 for i in range(len(ads))]})



    



    mask = (ad_mask["is_empty"] | ads['title'].isin(advertiser_select)) & (Label_select_mask["is_empty"] | ads['label'].isin(Label_select)) & (category_select_mask["is_empty"] | ads['fin_ctg'].isin(category_select)) & (paid_select_mask["is_empty"] | ads['sponsor'].isin(paid_select)) & (advcategory_select_mask["is_empty"] | ads['categories_1'].isin(advcategory_select)) & (labeled_by_advertiser_select_mask["is_empty"] | ads['paid_for_by'].isin(labeled_by_advertiser_select))
 
    add= ads[mask]
    return add.to_dict(orient="records")



    

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)

