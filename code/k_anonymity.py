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
        main_groups = self.anonymized_data.groupby(['Gender', 'Airport Continent'])

        new_dates = []
        utility_loss = 0

        for _, group in main_groups:
            # Sort the group by 'Departure Date'
            group = group.sort_values('Departure Date')

            # Create a subset group based on 'Departure Date' and count the records
            subset_groups = group.groupby('Departure Date').size().reset_index(name='count')

            i = 0
            last_generalized_start_date = None
            prev_count = None
            while i < len(subset_groups):
                if subset_groups.iloc[i]['count'] < k:
                    start_date = subset_groups.iloc[i]['Departure Date']
                    end_date = start_date
                    count = subset_groups.iloc[i]['count']

                    # Keep adding records from the next groups until we have at least k records.
                    while count < k and i < len(subset_groups) - 1:
                        i += 1
                        count += subset_groups.iloc[i]['count']
                        end_date = subset_groups.iloc[i]['Departure Date']

                    # If we're at the last subset group and it's less than k, merge with the previous group
                    if i == len(subset_groups) - 1 and count < k:
                        # Remove the date range of the previous group from new_dates
                        if prev_count:
                            new_dates = new_dates[:-prev_count]
                            count += prev_count  # Total count of both groups
                        if last_generalized_start_date:
                            start_date = last_generalized_start_date
                        end_date = subset_groups.iloc[i]['Departure Date']  # End date of the last group
                    # Set the new date range for the combined group.
                    new_dates.extend([f"{start_date}--{end_date}"] * count)
                    last_generalized_start_date = start_date
                    prev_count = count

                    utility_loss += count * 0.0001
                else:
                    new_dates.extend([subset_groups.iloc[i]['Departure Date']] * subset_groups.iloc[i]['count'])
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
        
        g = self.anonymized_data.groupby(['Gender', 'Airport Continent', 'Departure Date'])
        print(g.filter(lambda x: len(x) < k))


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
