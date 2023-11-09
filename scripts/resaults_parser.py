import pandas as pd
from pathlib import Path


class TestResultsController:
    """
    This class is used to parse and display the performance testing results.
    """
    __slots__ = ['folder_path']

    def __init__(self, folder_path='results'):
        """
        Initializes a new instance of the TestResultsController
        """
        self.folder_path = Path(folder_path)

    def _parse_result_file(self, file_path):
        """
        Parses the given file and calculates some statistics.
        """
        # Derive the table name from the file name
        table_name = file_path.stem

        # Load the data into dataframe & remove 'ms' from 'Duration' field
        df = pd.read_csv(file_path, names=['Transaction', 'Duration'],
                         converters={'Duration': lambda x: float(x.replace('ms', ''))},
                         skipinitialspace=True)

        # Calculate basic statistical metrics
        stats = df.groupby('Transaction').Duration.agg(['count', 'min', 'max', 'mean']).reset_index()
        stats.columns = ['Transaction', 'Count', 'Min Duration (ms)', 'Max Duration (ms)', 'Mean Duration (ms)']

        # Calculate the total duration
        total_duration = df['Duration'].sum()

        # Append the calculated data into the parsed results list
        return {'table_name': table_name, 'stats': stats, 'total_duration': total_duration}

    def _parse_all_results(self):
        """
        Parses all the result files located in the result folder
        """
        return [self._parse_result_file(file_path) for file_path in self.folder_path.glob('*.txt')]

    def _print_parsed_results(self, parsed_results):
        """
        Prints the parsed results
        """
        for result in parsed_results:
            print(f"Table: {result['table_name']}")
            print(result['stats'])
            print(f"Total Duration (ms): {result['total_duration']}\n")

    def summarize_performance_tests(self):
        """
        Parses all the results and then prints them
        """
        parsed_results = self._parse_all_results()
        self._print_parsed_results(parsed_results)


if __name__ == '__main__':
    controller = TestResultsController()
    controller.summarize_performance_tests()
