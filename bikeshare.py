import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_input(prompt):
    return input(prompt).strip().lower()


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
    city_prompt = 'Would you like to see data for Chicago, New York, or Washington?'
    city = get_input(city_prompt)
    while city != 'chicago' and city != 'new york' and city != 'washington':
        print('Please enter a valid city name.')
        city = get_input(city_prompt)
    print('Looks like you want to hear about {}! If this is not true, restart the program now!'.format(
        city.title().capitalize()))

    filter_time_prompt = 'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.'
    filter_time = get_input(filter_time_prompt)
    while filter_time != 'month' and filter_time != 'day' and filter_time != 'all' and filter_time != 'none':
        print('Please enter a valid filter.')
        filter_time = get_input(filter_time_prompt)
    month, day = '', ''

    # get user input for month (all, january, february, ... , june)
    if filter_time == 'month':
        print('We will make sure to filter by month!')
        month_prompt = 'Which month? January, February, March, April, May, or June? Please type out the full month name.'
        month = get_input(month_prompt)
        while month not in months:
            print('Please enter a valid month.')
            month = get_input(month_prompt)
        print('Just one moment... loading the data')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_time == 'day':
        print('We will make sure to filter by day!')
        day_prompt = 'Which day? Please type a day Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.'
        day = get_input(day_prompt)
        while day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday':
            print('Please enter a valid day.')
            day = get_input(day_prompt)
        print('Just one moment... loading the data')

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month == 'all' or month in months:
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day == 'all' or day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday' or day == 'Saturday' or day == 'Sunday':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df.dropna(axis=0)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # display the most common month
        popular_month = df['month'].mode()[0]
        print('Most Popular Month: ', popular_month)

        # display the most common day of week
        popular_day_of_week = df['day_of_week'].mode()[0]
        print('Most Popular Day: ', popular_day_of_week)

        # display the most common start hour
        # extract hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print('Most Popular Hour: ', popular_hour)
    except Exception as exception:
        print(exception)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # display most commonly used start station
        popular_start_station = df['Start Station'].mode()[0]
        print('Most Popular Start Station: ', popular_start_station)
    except Exception as exception:
        print(exception)

    try:
        # display most commonly used end station
        popular_end_station = df['End Station'].mode()[0]
        print('Most Popular End Station: ', popular_end_station)
    except Exception as exception:
        print(exception)

    try:
        # display most frequent combination of start station and end station trip
        popular_start_end_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
        print('Most Popular Start and End Station: ', popular_start_end_station)
    except Exception as exception:
        print(exception)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    trip_duration = df['Trip Duration']

    # display total travel time
    print('Total Travel Time: ', trip_duration.sum())

    # display mean travel time

    # Average travel time
    avg_travel_time = np.mean(trip_duration, axis=0)

    # Standard Deviation of travel time
    std_travel_time = np.std(trip_duration, axis=0)

    # Mean normalized travel time
    mean_norm_travel_time = np.mean((trip_duration - avg_travel_time) / std_travel_time, axis=0)
    print('Mean Travel Time: ', mean_norm_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('User Types: ', user_types)
    except KeyError as key_error:
        print(key_error)

    try:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        print('Genders: ', genders)
    except KeyError as key_error:
        print(key_error)

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest Birth Year: ', earliest_birth_year)
        latest_birth_year = df['Birth Year'].max()
        print('Latest Birth Year: ', latest_birth_year)
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most Common Birth Year: ', most_common_birth_year)
    except KeyError as key_error:
        print(key_error)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display 5 rows of raw data at a time
        raw_data_prompt = 'Would you like to see 5 rows of raw data? Enter yes or no.'
        raw_data = get_input(raw_data_prompt)

        while raw_data != 'yes' and raw_data != 'no':
            print('Please enter a valid response.')
            raw_data = get_input(raw_data_prompt)

        if raw_data == 'yes':
            print(df.head())
            limit = 5
            while len(df) > limit and not df.empty:
                raw_data_prompt = 'Would you like to see 5 more rows of raw data? Enter yes or no.'
                raw_data = get_input(raw_data_prompt)
                while raw_data != 'yes' and raw_data != 'no':
                    print('Please enter a valid response.')
                    raw_data = get_input(raw_data_prompt)
                if raw_data == 'yes':
                    print(df[limit:limit + 5])
                    limit += 5
                else:
                    break

        restart = get_input('\nWould you like to restart? Enter yes to restart.\n')
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
