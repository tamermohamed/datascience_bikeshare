import time
from matplotlib.pyplot import get
import pandas as pd
import numpy as np
from sqlalchemy import true
from time import strptime
import sys
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def display_raw_data(df):

    """ Display row data for the user 5 rows each time"""
    
    print("To show raw data 5 rows each time, enter yes to display row data,enter no to continue")

    index = 0

    while True:

        view_data = input()

        if view_data.lower() == 'yes':

            raw_data = df[index:index +5]
            index += 5
            
            print(raw_data)

            if raw_data.empty:
                print('-'*5 + 'No More Data To Show' + '-'*5)
                break
            else:
                print('-'*5 + 'enter yes to show next 5 rows or no to cancel' + '-'*5)
        
        elif view_data.lower() == 'no':
            break
        else:
            print('Wrong Input')

    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    print('Select The City : 1 For chicago, 2 For new york city and 3 For washington, Or -1 To Exit the Analysis')

    while True:

        city = input()
        if city == '-1':
            sys.exit()
        elif  city == '1' :
            city = 'chicago'
        elif city == '2':
            city = 'new york city'
        elif city == '3':
            city = 'washington'
        else:
            print('You Have Wrong Selction Please Select City Again')

        
        if  CITY_DATA.get(city) != None:
            break
        

    # get user input for month (all, january, february, ... , june)

    print('Select The Month : all, january, february, ... , june OR -1 To Exit')

    while True:
        
        input_month = input()

        if input_month == '-1' or input_month.lower() == 'all':
            month = -1
            break
        
        try :

            month = int(strptime(input_month,'%B').tm_mon)
            break
        except:
            print('You input Wrong Month')
       
    # get user input for day of week (all, monday, tuesday, ... sunday)

    print('Select The day of the week : all, monday, tuesday, ... sunday OR -1 To Exit and use all as Default Value')

    while True:
        
        input_day = input()

        if input_day == '-1' or input_day.lower() == 'all':
            day = -1
            break
        
        try :

            day = strptime(input_day,'%A').tm_mday - 1
            break
        except:
            print('You input Wrong Day')

    print('-'*40)
    
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - index of the month to filter by, or -1 to apply no month filter
        (int) day - index of the day of week to filter by, or -1 to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day'] = df['Start Time'].dt.dayofweek

    df['hour'] = df['Start Time'].dt.hour

    if month != -1 :

        df = df[df['month'] == month]

    if day != -1:
        df = df[df['day'] == day]

    display_raw_data(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    most_common_month = df['month'].mode()[0]
    
    print(f'Most Common Month : {str(calendar.month_name[most_common_month])} \n')
    # display the most common day of week

    most_common_day = df['day'].mode()[0]
    
    print(f'Most Common Day : {str(calendar.day_name[most_common_day] )} \n')
    # display the most common start hour

    most_common_hour = df['hour'].mode()[0]
    
    print(f'Most Common Hour : {str(most_common_hour)} \n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"Most commonly used start station : {common_start_station}")
    # display most commonly used end station
    
    common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station : {common_end_station}")

    # display most frequent combination of start station and end station trip

    df['start_end'] = df['Start Station'] +' >> '+ df['End Station']

    common_start_end_station = df['start_end'].mode()[0]
    print(f"Most frequent combination of start station and end station trip : {common_start_end_station }")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    
    print(f'Total Trip Time : {str(total_time)} in seconds \n')

    # display mean travel time

    avg_time = df['Trip Duration'].mean()
    print(f'Average Trip Time : {str(avg_time)} in seconds \n'  )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(f"User Types Count :\n{user_types} \n")

    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(f"User Genders Count : \n{user_gender} \n")

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        print(f"Earliest Birth Year : {int(df['Birth Year'].min())} \n")
        print(f"Most Recent Birth Year : {int(df['Birth Year'].max())} \n")
        print(f"Most Common Birth Year : {int(df['Birth Year'].mode()[0])} \n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
