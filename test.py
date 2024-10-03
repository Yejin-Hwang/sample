#!/usr/bin/env python
# coding: utf-8

# In[20]:


from datascience import *
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt


# # Join

# In[2]:


drink = Table(['Drink','Cafe','Price']).with_rows([['Milk Tea', 'Ahsa', 4],
                                                   ['Espresso', 'Starbucks', 6],
                                                   ['Latte', 'Starbucks', 7],
                                                   ['Espresso', 'Star', 6]])


# In[3]:


drink


# In[4]:


discounts = Table().with_columns("% off",make_array(5,25,10),
                                "location",make_array('Starbucks','Ahsa','Star'))
discounts


# In[5]:


drink_wdis=drink.join("Cafe",discounts,"location")
drink_wdis


# In[6]:


def disprice(p,off):
    return p*(1-off/100)

drink_wdis.apply(disprice,'Price','% off')


# In[7]:


drink_wdis.with_column("price_after_discount",drink_wdis.apply(disprice,'Price','% off'))


# # Bike sharing demo

# In[23]:


trip = Table.read_table('trip.csv')
trip.num_rows


# In[24]:


trip.show(4)


# In[25]:


trip.hist('Duration')


# In[26]:


trip.sort('Duration',descending=True).show(3)


# In[27]:


(250/60)


# In[28]:


trip_bhd=trip.where('Duration',are.below(1800))


# In[29]:


trip_bhd.hist('Duration')


# # Check Start and End Stations

# In[30]:


trip_bhd.show(3)


# # Which station do people rent most bikes?

# In[33]:


start = trip_bhd.group('Start Station')


# In[34]:


start.show(3)


# In[35]:


top5pop =start.sort('count',descending=True).column('Start Station')[0:5]


# In[36]:


top5pop


# In[37]:


stations = Table.read_table('station.csv').drop(4,6)
stations.show(3)


# In[20]:


stations_map=stations.select('lat','long','name')
Marker.map_table(stations_map)


# In[41]:


stations_sf=stations.where('landmark','San Francisco')


# In[42]:


stations_sf_map=stations_sf.select('lat','long','name')
Marker.map_table(stations_sf_map)


# In[43]:


start.sort('count',descending=True).show(3)


# In[45]:


stations_sf_map.show(3)


# In[55]:


top_5_station=start.sort('count',descending=True).take(np.arange(5))


# In[56]:


top_5_station=top_5_station.join('Start Station',stations_sf_map,'name')
top_5_station


# In[53]:


top_5_station_map=top_5_station.select('lat','long','Start Station')
Marker.map_table(top_5_station_map)


# In[57]:


top_5_station_map


# # Make a circle map

# In[58]:


top_5_station


# In[66]:


top_5_station_circle=(
top_5_station.with_columns('colors','blue','areas',top_5_station.column('count')/10)
)
top_5_station_circle


# In[68]:


top_5_station_circle=top_5_station_circle.select('lat','long','Start Station','colors','areas')


# In[64]:


top_5_station_circle.relabel('Start Station')


# In[69]:


Circle.map_table(top_5_station_circle)


# # Comparison

# In[70]:


3>2


# In[72]:


type(3>2)


# In[73]:


3=3


# In[74]:


3==3.0


# In[75]:


3!=10


# In[76]:


x = 15
y=3


# In[77]:


x>15


# In[78]:


x>y


# In[80]:


-10<x-y<3


# In[79]:


(x-y)>-10 and (x-y)<3


# In[81]:


pets = make_array('cat','cat','cat','cat','cat','dog','dog','dog','dog')


# In[82]:


pets == 'dog'


# In[83]:


sum(pets == 'dog')


# In[84]:


np.count_nonzero(pets == 'dog')


# In[85]:


x = np.arange(20,60)


# In[86]:


sum(x > 35)


# In[87]:


survey = Table.read_table('welcome_survey_sp22.csv')


# In[88]:


survey.show(2)


# In[92]:


r = survey.row(1)
r


# In[93]:


r.item(1)


# In[94]:


r.item('Extroversion')


# In[96]:


survey.select(1,2,3)


# In[98]:


np.average(survey.select(1,2,3).row(1))


# In[100]:


survey.select(1,2,3).apply(sum)


# In[102]:


survey.select(1,2,3).with_column('Total',survey.select(1,2,3).apply(sum))


# # Control

# In[103]:



x=20


# In[105]:


if x>18:
    print('You can leagally vote.')


# In[106]:


def check_age(x):
    if x>18:
        print('You can leagally vote.')
    if x>21:
        print('You can leagally drink.')


# In[107]:


check_age(x=20)


# In[108]:


check_age(x=25)


# In[109]:


def check_age(x):
    if x>18:
        print('You can leagally vote.')
    elif x>21:
        print('You can leagally drink.')
    else:
        print('You can leagally drink milk.')


# In[110]:


check_age(15)


# In[111]:


check_age(19)


# In[112]:


check_age(25)


# In[113]:


trip.show(3)


# # Create a new column show one-way trip or round trip.

# In[114]:


def trip_check(start,end):
    if start == end:
        return 'Round Trip'
    else:
        return 'One-way'


# In[117]:


trip.row(0).item('Start Station')
trip.row(0).item('End Station')


# In[118]:


trip_check(start=trip.row(0).item('Start Station'),end=trip.row(0).item('End Station'))


# In[121]:


trip.apply(trip_check,'Start Station','End Station')


# In[123]:


trip_v1=trip.with_column('Trip Kind', trip.apply(trip_check,'Start Station','End Station'))


# In[125]:


trip_v1.where('Trip Kind','Round Trip')


# # Random selection
# 
# ## Let's play a game:
# 
# Roll a die, if my number is bigger, you pay me \$1
# 
# if my number is smaller, I pay you \$1
# 
# if numbers are same, nothing happens
# 
# Need to find a way to simulate this game

# In[25]:


def one_round(my_roll,your_roll):
    if my_roll > your_roll:
        return 1
    elif my_roll < your_roll:
        return -1
    elif my_roll == your_roll:
        return 0


# In[29]:


one_round(my_roll=1,your_roll=6)


# In[30]:


one_round(my_roll=6,your_roll=3)


# In[8]:


np.random.choice(np.arange(6)+1,10)


# In[32]:


def simulate_one_roll():
    my_roll = np.random.choice(np.arange(6)+1,1)
    your_roll = np.random.choice(np.arange(6)+1,1)
    return one_round(my_roll,your_roll)


# In[37]:


simulate_one_roll()


# # Appending Arrays

# In[16]:


first = make_array(1)
second = make_array(-1)


# In[19]:


np.append(first,second)


# # For statment

# In[23]:


print('I love my', 'cat')
print('I love my', 'dog')
print('I love my', 'kitty')


# In[24]:


for i in make_array('cat','dog','kitty'):
    print('I love my ', i)


# # toss die game con.

# In[38]:


game_results = make_array()

for i in np.arange(1000):
    one_result = simulate_one_roll()
    game_results = np.append(game_results,one_result)


# In[43]:


Table().with_column('sim_results',game_results).hist('sim_results')


# # Toss a coin 100 times

# In[45]:


coin = make_array('Head','Tail')
coin


# In[50]:


np.random.choice(coin,1)


# # How many head we can get if we toss a coin 100 times?

# In[57]:


outcome = make_array()
for i in np.arange(100):
    outcome = np.append(outcome,np.random.choice(coin,1))


# In[58]:


sum(outcome == 'Head')


# # A,K,Q, draw two card randomly
# # Sample Space = \{ {A,K}, {A,Q}, {K,Q},{K,A},{Q,K},{Q,A}\}
# 
# $$
# P(\{Q,K\})=\frac{1}{6}
# $$

# In[59]:


box = make_array('A','K','Q')


# In[68]:


np.random.choice(box,2,replace=False)[0]+np.random.choice(box,2,replace=False)[1]


# In[77]:


outcome = make_array()
for i in np.arange(10000):
    onetry = np.random.choice(box,2,replace=False)
    outcome = np.append(outcome,onetry[0]+onetry[1])


# In[78]:


sum(outcome=='QK')/len(outcome)


# In[79]:


1/6


# # 
# In general,
# $$
# P(A \cap B) \not= P(A)\times P(B)
# $$
# 
# $$
# P(A \cap B) = P(A)\times P(B|A)
# $$

# $$
# P(\{K\})=\frac{1}{3} \qquad P(\{Q\})=\frac{1}{3}
# $$
# 
# $$
# P(\{KQ\})=P(\{K\})\times P(\{Q|K\})\\
# =\frac{1}{3}\frac{1}{2}=\frac{1}{6}\\
# $$

# # Example: Roll a die two times, what is the probability to get at least one 6?
# 
# P('at least one 6') = P('first die is 6 and second is not')+P('first die is not 6 and second is 6')+
# P('first die is 6 and second is 6')=

# In[80]:


(1/6)*(5/6)+(1/6)*(5/6)+(1/6)*(1/6)


# In[82]:


dice=np.arange(1,7)
dice


# In[88]:


outcome = make_array()
outcome = np.append(outcome,np.random.choice(dice,2,replace=True))
outcome


# In[92]:


Table(['first','second']).with_row(np.random.choice(dice,2,replace=True))


# In[89]:


Table(['first','second'])
outcome = np.append(outcome,np.random.choice(dice,2,replace=True))
outcome


# In[108]:


outcome = Table(['first','second'])
for i in np.arange(1000):
    onetry = np.random.choice(dice,2,replace=True)
    outcome = outcome.with_row(onetry)


# In[109]:


sum(outcome['first']==6)+sum(outcome['second']==6)-outcome.where('first',6).where('second',6).num_rows


# In[110]:


296/1000


# In[ ]:




