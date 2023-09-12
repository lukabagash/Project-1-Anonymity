import pandas as pd

class Anonymization:

    def __init__(self, data_path):
        self.data = self.load_data(data_path)
        self.anonymized_data = None

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

    def generalize_date(self):
        """
        Generalize the Departure Date by removing the day.
        """
        self.anonymized_data['Departure Date'] = pd.to_datetime(self.data['Departure Date']).dt.to_period('M')

    def anonymize(self, k):
        """
        Anonymize the data for a given k value.
        This is a placeholder and needs the actual anonymization logic.
        """
        # TODO: Implement the actual anonymization logic here
        columns_to_suppress = ["Passenger ID", "First Name", "Last Name", "Nationality", "Airport Name", "Airport Country Code", "Country Name", "Continents", "Pilot Name"]
        # Suppress the specified columns

        if columns_to_suppress:
            self.suppress_attributes(columns_to_suppress)
        
        self.generalize_date()
        grouped = self.anonymized_data.groupby(['Gender', 'Airport Continent', 'Departure Date'])
        print(grouped.filter(lambda x: len(x) >= k))


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
        Measure the utility of the anonymized data.
        This is a placeholder and needs the actual utility measurement logic.
        """
        # TODO: Implement the actual utility measurement logic here
        utility_value = 0  # Placeholder
        return utility_value
