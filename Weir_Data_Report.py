import pandas as pd
import seaborn as sns
from matplotlib import pyplot as pyplot

df = pd.read_csv('./extensive_data.csv')

active_statuses = ['Active', 'In Progress', 'On Hold', 'Pending']
pending_statuses = ['On Hold', 'Pending']
resolved_statuses = ['Completed', 'Resolved', 'Closed', 'Submitted']
service_desk_team = ['Leigh Browning', ' Xyrus Roxas', 'Elliott Beeten', 'Daniel Bowen', 'Marc Falzon']

# datetime_columns =['CreatedOn', 'LastModified', 'ResolvedOn', 'SLOTarget']
# for each in datetime_columns:
#     df[each] = pd.to_datetime(df[each])

for col in df.columns:
    if df[col].dtype == 'object':
        try:
            df[col] = pd.to_datetime(df[col])
        except ValueError:
            pass

df = df.assign(CreatedOn_year=df.CreatedOn.dt.year,
 CreatedOn_month=df.CreatedOn.dt.month,
  CreatedOn_day=df.CreatedOn.dt.day,
  ResolvedOn_year=df.ResolvedOn.dt.year,
 ResolvedOn_month=df.ResolvedOn.dt.month,
  ResolvedOn_day=df.ResolvedOn.dt.day,
  TicketDuration=(df['ResolvedOn'] - df['CreatedOn']).dt.days,
  Created_month_name = df.CreatedOn.dt.month_name(),
  Resolved_month_name = df.ResolvedOn.dt.month_name(),
  Created_period = df.CreatedOn.dt.to_period('M'),
  Resolved_period = df.ResolvedOn.dt.to_period('M'),
  )


# organse seperate df for monthly rundown
ser_createdon = df.RequestId.groupby(df.Created_period).count()
ser_resolvedon = df.RequestId.groupby(df.Resolved_period).count()
ser_mean_dur = df.TicketDuration.groupby(df.Created_period).mean()
ser_max_dur = df.TicketDuration.groupby(df.Created_period).max()
ser_onboard = df.RequestId[df.Title.str.contains('Onboarding actions')].groupby(df.Created_period).count()
ser_offboard = df.RequestId[df.Title.str.contains('Offboarding actions')].groupby(df.Created_period).count()

# Combine seperate dataframes into Monthly rundown
# df_combined = pd.merge(df_createdon, df_resolvedon, right_index=True, left_index=True)
df_combined = pd.DataFrame(
    {'Created': ser_createdon,
    'Resolved': ser_resolvedon,
    'Mean Dur':ser_mean_dur,
    'Max Dur': ser_max_dur,
    'Onboarding': ser_onboard,
    'Offboarding': ser_offboard,

    }
)

print(df_combined)

# print each column as a seperate plot
df_combined.plot(subplots=True)

#Plot and Save Aged Tickets to File    
sns.boxplot(y='AssignedToUser', x='AgeInDays', data=df[df['Status'].isin(active_statuses)&(df.AssignedToUserCompany=='Minerals Australia')]).get_figure().savefig("Aged_Ticket_Report.png", bbox_inches='tight', dpi=200)

# Plot Resolution by Duration
sns.boxplot(y='AssignedToUser', x='AgeInDays', data=df[df['Status'].isin(resolved_statuses)&(df.AssignedToUserCompany=='Minerals Australia')]).get_figure().savefig("Aged_Ticket_Report.png", bbox_inches='tight', dpi=200)

# Plot Tickets Created by month - split IR/SR

"""

General Filter:
    edf[(edf['ResolvedOn'].dt.month == 8)&(edf['AssignedToUserCompany']=='Minerals Australia')&
    (edf['ResolvedOn'].dt.year==2019)]
    sns.boxplot(y='AssignedToUser', x='Ticket_Duration', data=generic_filter)

Filter Field with expressions:
    df[df.CreatedOn_year==2019].CreatedOn.dt.month

Defined Columns with filter:
    df[['CreatedOn','AffectedUser']][df['CreatedOn_month']==8]

Data set Sorting:
    data=dataset.sort_values(by='AssignedToUser')

Tickets by multiple conditions: 
    edf[edf['Status'].isin(active_statuses)]

Ticks by Single condition:
    edf[edf['Status']=='Active']

Strip datetime to date only:
    edf['Ticket_Duration'] = edf['Ticket_Duration'].dt.days

Filtered Date for query:
    closed_tickets_df[((closed_tickets_df['CreatedOn'].dt.month == 6) &
     (closed_tickets_df['AssignedToUserCompany']=='Minerals Australia'))]
    active_tickets_df = edf[edf['Status'].isin(active_statuses)]

    closed_tickets_df[(closed_tickets_df['ResolvedOn'].dt.month == 8)&
    (closed_tickets_df['AssignedToUserCompany']=='Minerals Australia')&
    (closed_tickets_df['ResolvedOn'].dt.year==2019)]

Onboarding requests
    df.Title[df.Title.str.contains('Onboarding actions') & (df.CreatedOn.dt.month==8)].count()

Offboarding requests
    df.Title[df.Title.str.contains('Offboarding actions') & (df.CreatedOn.dt.month==8)&(df.CreatedOn_year==2019)].count()

Specific Plots:
*****
put plt.figure(figsize=(width, height)) before plots to change size
*****

Active Tickets by AssignedToUser (Box)
    sns.boxplot(y='AssignedToUser', x='AgeInDays', data=edf[edf['Status'].isin(active_statuses)&
    (edf.AssignedToUserCompany=='Minerals Australia')])

Active Tickets By AssignedToUser (spots)
    sns.stripplot(y='AssignedToUser', x='AgeInDays',
     data=edf[(edf['Status'].isin(active_statuses))&
     (edf['AssignedToUserCompany']=='Minerals Australia')], hue='Status', jitter=True)

Duration by Resolved Month:
    plt.figure(figsize=(5,7))
    sns.boxplot(x='ResolvedOn_month',
    y='TicketDuration',
    data=df[(df.ResolvedOn_month>2)&
    (df.ResolvedOn_month<9)&
    (df.CreatedOn_year==2019)])

Created Ticket Count:
    sns.countplot(x='Created_month_name',
      data=df[(df.CreatedOn_year==2019)&
      (df.AssignedToUserCompany=='Minerals Australia')
      ].sort_values('CreatedOn_month'))
    plt.xticks(rotation=30)

    sns.violinplot(x='CreatedOn_month',
     y='TicketDuration',
     hue='Ticket_Type',
     data=df[(df.CreatedOn_month>2)&
    (df.CreatedOn_month<9)&
    (df.CreatedOn_year==2019)], split=True)

     sns.boxplot(x='ResolvedOn_month',
      y='TicketDuration',
      data=df[(df.ResolvedOn_month>2)&
      (df.ResolvedOn_month<9)&
      (df.ResolvedOn_year==2019)])

Twin Line Plot - Created and Resolved
    fig, ax = plt.subplots()
    sns.lineplot(x=df.CreatedOn.dt.month.value_counts().index, y=df.CreatedOn.dt.month.value_counts(), data=df[(df.CreatedOn.dt.year==2019)&(df.CreatedOn.dt.month==8)], ax=ax, color='b', label='Created')
    sns.lineplot(x=df.ResolvedOn.dt.month.value_counts().index, y=df.ResolvedOn.dt.month.value_counts(), data=df[(df.ResolvedOn.dt.year==2019)&(df.ResolvedOn.dt.month==8)], ax=ax, color='r', label='Resolved')
    labels = ax.get_xticklabels()
    ax.set_xticklabels(labels, rotation=-30)
    plt.legend()
    plt.xlabel('Months')
    plt.ylabel('Count')
    plt.show()

Save Plot to File:
    aged_plot = aged_graph.get_figure()
    aged_plot.savefig("aged_plot.png", dpi=200, bbox_inches='tight')

    .get_figure().savefig("Aged_Ticket_Report.png", bbox_inches='tight', dpi=200)

Save plot to file - single line:
    sns.boxplot(y='AssignedToUser', x='AgeInDays', data=edf[edf['Status'].isin(active_statuses)&
    (edf.AssignedToUserCompany=='Minerals Australia')]).get_figure().
    savefig("test_plot_2.png", bbox_inches='tight', dpi=200)

INFORMATIVE ONLY

    df['birthdate'].groupby(df.birthdate.dt.to_period("M")).agg('count')
    pd.to_datetime(testdate['CreatedOn']).dt.year.value_counts()
"""

