import pandas as pd
from pathlib import Path


class TestResultsController:
    def __init__(self, folder_path='results'):
        self.folder_path = Path(folder_path)
        pd.options.display.float_format = "{:.2f}".format

    def _parse_result_file(self, file_path):
        df = pd.read_csv(file_path, names=['Transaction', 'Duration'],
                         converters={'Duration': lambda x: float(x.replace('ms', ''))},
                         skipinitialspace=True)

        stats = df.groupby('Transaction').Duration.agg(['count', 'min', 'max', 'mean']).reset_index()
        stats.columns = ['Transaction', 'Count', 'Min Duration (ms)', 'Max Duration (ms)', 'Mean Duration (ms)']
        total_duration = df['Duration'].sum()

        # Add total row
        total_row = pd.Series(['Total', stats['Count'].sum(), '-', '-', total_duration],
                              index=stats.columns)
        stats = stats.append(total_row, ignore_index=True)

        return {'table_name': file_path.stem, 'stats': stats, 'total_duration': total_duration}

    def _parse_all_results(self):
        return [self._parse_result_file(file_path) for file_path in self.folder_path.glob('*.txt')]

    def _print_parsed_results(self, parsed_results):
        for result in parsed_results:
            print(f"Table: {result['table_name']}")
            print(result['stats'])
            print("\n")

    def _save_table_as_txt(self, result, output_dir):
        with open(output_dir / f"{result['table_name']}_table.txt", 'w') as f:
            f.write(result['stats'].to_string(index=False))

    def summarize_performance_tests(self):
        parsed_results = self._parse_all_results()
        self._print_parsed_results(parsed_results)

        output_dir = self.folder_path / 'tables'
        output_dir.mkdir(exist_ok=True)

        for result in parsed_results:
            self._save_table_as_txt(result, output_dir)


if __name__ == '__main__':
    controller = TestResultsController()
    controller.summarize_performance_tests()
