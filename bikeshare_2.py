import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = input('Welcome! , Choose the city (chicago, new york city, washington) that you would like to see its data ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Please choose valid city (chicago, new york city, washington) ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Nice choice :), Enter the month that you want to filter on or choose (all) ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april','may', 'june']:
        month = input('Please choose valid month(s) type: all, january, february, march, april, may, june ').lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Nice, now choose the day of the week or all that you want to filter on ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wedensday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Please choose valid day(s) type: all, monday, tuesday, wedensday, thursday, friday, saturday, sunday ').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv('{}.csv'.format(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april','may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print('The most common month: {}'.format(common_month))

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    print('The most common day: {}'.format(common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common hour: ' + str(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startST = df['Start Station'].value_counts().idxmax()
    print('The most common start station used: {}'.format(common_startST))

    # display most commonly used end station
    common_endST = df['End Station'].value_counts().idxmax()
    print('The most common end station used: {}'.format(common_endST))

    # display most frequent combination of start station and end station trip
    frequent_StartEnd_ST = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent combination of start station and end station trip:\n {}'.format(frequent_StartEnd_ST))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600.0
    print('The total travel time: {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600.0
    print('The mean travel time: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The number of user types: {}'.format(user_types))

    # Display counts of gender
    if 'Gender' not in df.columns:
        print('The city\'s data dont have gender :(')
    else:
        user_gender = df['Gender'].value_counts()
        print('The number of gender: {}'.format(user_gender))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('The city\'s data dont have birth year :(')
    else:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].value_counts().idxmax())

        print('The earliest year of birth: {}'.format(earliest))
        print('The most recent year of birth: {}'.format(most_recent))
        print('The common year of birth: {}'.format(common_year))

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
