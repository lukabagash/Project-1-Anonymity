import pandas as pd

class Anonymization:

    def __init__(self, data_path):
        self.data = self.load_data(data_path)
        self.anonymized_data = None
        self.utility_value = 1

    def load_data(self, data_path):
        """
        Load the dataset from the given path.
        """
        return pd.read_csv(data_path, encoding="ISO-8859-1")



    def suppress_attributes(self, columns_to_suppress):
        """
        Suppress the specified columns from the dataset.
        """
        self.anonymized_data = self.data.drop(columns=columns_to_suppress, errors='ignore')

        utility_loss = len(columns_to_suppress) * 0.01
        self.utility_value -= utility_loss

    def generalize_date_level_1(self):
        """
        Level 1 Generalization: Remove the day from the Departure Date.
        """

        self.anonymized_data['Departure Date'] = pd.to_datetime(self.data['Departure Date']).dt.to_period('M')

        self.utility_value -= 0.05
    
    def generalize_date_level_2(self, k):
        """
        Level 2 Generalization: Adjust the Departure Date based on k-anonymity requirements.
        """
        # Group by the QIDs and count the number of records in each group.
        groups = self.anonymized_data.groupby(['Gender', 'Airport Continent', 'Departure Date']).size().reset_index(name='count')

        # Extract the month and year from the 'Departure Date' column.
        groups['Year'] = groups['Departure Date'].dt.year
        groups['Month'] = groups['Departure Date'].dt.month

        # Sort the groups by Gender, Airport Continent, Month, and Year.
        groups = groups.sort_values(['Gender', 'Airport Continent', 'Year', 'Month'])

        i = 0
        new_dates = []
        utility_loss = 0

        while i < len(groups):
            # If the current group size is less than k, we need to generalize the date further.
            if groups.iloc[i]['count'] < k:
                start_year = groups.iloc[i]['Year']
                start_month = groups.iloc[i]['Month']
                end_year = start_year
                end_month = start_month
                count = groups.iloc[i]['count']

                # Keep adding records from the next groups until we have at least k records.
                while count < k and i < len(groups) - 1:
                    i += 1
                    count += groups.iloc[i]['count']
                    end_year = groups.iloc[i]['Year']
                    end_month = groups.iloc[i]['Month']

                # Set the new date range for the combined group.
                new_dates.extend([f"{start_month}/{start_year}-{end_month}/{end_year}"] * count)
                utility_loss += abs(end_month-start_month) * 0.001
            else:
                # If the group size is already at least k, keep the month and year as it is.
                new_dates.extend([f"{groups.iloc[i]['Month']}/{groups.iloc[i]['Year']}"] * groups.iloc[i]['count'])
            i += 1

        # Sort the self.anonymized_data DataFrame in the same order as the groups DataFrame.
        self.anonymized_data = self.anonymized_data.sort_values(['Gender', 'Airport Continent', 'Departure Date'])

        # Directly assign the new_dates list to the 'Departure Date' column.
        self.anonymized_data['Departure Date'] = new_dates

        self.utility_value -= utility_loss


    def anonymize(self, k):
        """
        Anonymize the data for a given k value.
        This is a placeholder and needs the actual anonymization logic.
        """
        # TODO: Implement the actual anonymization logic here
        # Suppress the specified columns
        columns_to_suppress = ["Passenger ID", "First Name", "Last Name", "Nationality", "Pilot Name"]

        if columns_to_suppress:
            self.suppress_attributes(columns_to_suppress)

        # Level 1 Generalization
        self.generalize_date_level_1()

        # Check k-anonymity after Level 1
        grouped = self.anonymized_data.groupby(['Gender', 'Airport Continent', 'Departure Date'])
        insufficient_groups = grouped.filter(lambda x: len(x) < k)
        
        # If there are groups that don't meet the k-anonymity requirement, apply Level 2 Generalization
        if not insufficient_groups.empty:
            self.generalize_date_level_2(k)


    def save_to_csv(self, filename):
        """
        Save the anonymized data to a CSV file.
        """
        if self.anonymized_data is not None:
            self.anonymized_data.to_csv(filename, index=False)
        else:
            print("Data has not been anonymized yet.")


    def measure_utility(self):
        """
        Return the utility of the anonymized data.
        """
        return round(self.utility_value, 2)
