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
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter the city (chicago, new york city or washington): ")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
          break
        else:
            print("Invalid input. Please enter a valid input.")
    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input("Do you want to choose particular month? If yes, enter month name from first six months, else type 'all': ")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Invalid input. Please enter a valid input.")
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Do you want to choose particular day? If yes, enter day name, else type 'all': ")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid input. Please enter a valid input")
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        df = df[df['month'] == month]
    
    if day != 'all':
        
        df = df[df['day_of_week'] == day.title()]
   
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    mcm = df['month'].mode()[0]
    print("The most common month is: ", mcm)

    # Display the most common day of week
    mcdow = df['day_of_week'].mode()[0]
    print("The most common day of week is: ", mcdow)
    
    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    mcsh = df['hour'].mode()[0]
    print("The most common start hour is: ", mcsh)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    mcuss = df['Start Station'].mode()[0]
    print("The most commonly used start station is ", mcuss)

    # Display most commonly used end station
    mcues = df['End Station'].mode()[0]
    print("The most commonly used end station is ", mcues)

    # Display most frequent combination of start station and end station trip
    df['mfcossaest'] = df['Start Station'] + " " + df['End Station']
    print("The most common route combination is ", df['mfcossaest'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()
    total_travel_hours = total_travel / 3600
    print("The total travel time is (in hours):", round(total_travel_hours))

    # Display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("The total mean travel time is (in hours):", round(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    if city != 'washington':
        # Display counts of gender
        gen = df.groupby(['Gender'])['Gender'].count()
        print(gen)
        # Display earliest, most recent, and most common year of birth
        mryob = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        eyob = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        mcyob = df['Birth Year'].mode()[0]
        print("The earliest year of birth is ", eyob, "\n")
        print("The most recent year of birth is ", mryob, "\n")
        print("The most common year of birth is ", mcyob, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    x = 1
    while True:
        raw_data = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        if raw_data.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
