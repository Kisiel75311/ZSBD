import os
import re
import pandas as pd


class ResultParser:
    def __init__(self, directory_path, performance_file_path):
        self.directory_path = directory_path
        self.performance_file_path = performance_file_path

    def calculate_total_cost(self, file_path):
        with open(file_path, 'r') as file:
            sql_content = file.read()
            for line in sql_content.split('\n'):
                if '|   0 |' in line:
                    parts = line.split('|')
                    # Adjust the index as necessary to target the correct column
                    cost_part = parts[7].strip()  # Cost is assumed to be in the 8th column

                    # Check if cost_part is in 'K' format (e.g., '117K')
                    if cost_part.endswith('K'):
                        # Remove 'K' and convert to integer, then multiply by 1000
                        cost_value = cost_part[:-1]
                        try:
                            return int(float(cost_value) * 1000)
                        except ValueError:
                            # Log the error or handle it as needed
                            print(f"Invalid cost value (K format): {cost_part} in file {file_path}")
                            return None
                    else:
                        # Handle regular numeric values
                        try:
                            return int(cost_part.split()[0])
                        except ValueError:
                            # Log the error or handle it as needed
                            print(f"Non-numeric cost value found: {cost_part} in file {file_path}")
                            return None
            return None

    def calculate_total_cost_for_all_files(self):
        results = []
        for file_name in os.listdir(self.directory_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(self.directory_path, file_name)
                total_cost = self.calculate_total_cost(file_path)
                script_name = '_'.join(file_name.split('_')[1:]).rsplit('.', 1)[0]
                results.append({'Nazwa Skryptu': script_name, 'Koszt': total_cost})

        # Tworzenie DataFrame
        df = pd.DataFrame(results)
        # Obliczenie średniego kosztu dla każdego skryptu
        avg_costs = df.groupby('Nazwa Skryptu')['Koszt'].mean().reset_index()
        avg_costs.rename(columns={'Koszt': 'Średni Koszt'}, inplace=True)

        # Formatowanie kolumny 'Średni Koszt' aby wyświetlała liczby zamiast notacji naukowej
        avg_costs['Średni Koszt'] = avg_costs['Średni Koszt'].apply(lambda x: f'{x:.0f}')

        # Zapisanie do pliku Markdown
        markdown_table = avg_costs.to_markdown(index=False)
        with open('wyniki.md', 'w') as file:
            file.write(markdown_table)
        return avg_costs

    def generate_performance_table(self):
        # Wczytywanie danych
        data = pd.read_csv(self.performance_file_path, header=None, names=['Iteracja', 'Nazwa Skryptu', 'Czas'],
                           sep=', ')

        # Konwersja czasu do wartości liczbowych (w milisekundach)
        data['Czas'] = data['Czas'].str.replace('ms', '').astype(float)

        # Agregacja danych
        aggregated_data = data.groupby('Nazwa Skryptu')['Czas'].agg(['mean', 'min', 'max']).reset_index()
        aggregated_data.columns = ['Nazwa Skryptu', 'Średni Czas [ms]', 'Min. Czas [ms]', 'Max. Czas [ms]']

        # Zapisanie do pliku Markdown i zwrócenie wyniku
        markdown_table = aggregated_data.to_markdown(index=False)
        with open('tabela_wynikow.md', 'w') as file:
            file.write(markdown_table)

        return aggregated_data

    def merge_tables_and_save(self, cost_table, time_table, output_directory):
        # Merge tables
        merged_df = cost_table.merge(time_table, on='Nazwa Skryptu', how='outer')
        merged_df.rename(columns={'Koszt': 'Średni Koszt', 'mean': 'Średni Czas [ms]', 'min': 'Min. Czas [ms]',
                                  'max': 'Max. Czas [ms]'}, inplace=True)

        # Save the merged table to the specified output path
        output_path = os.path.join(output_directory, 'final_table.md')
        markdown_table = merged_df.to_markdown(index=False)
        with open(output_path, 'w') as file:
            file.write(markdown_table)


# Użycie klasy
directory_path = 'explain_plans'  # Ścieżka do katalogu z planami
performance_file_path = 'results/results_with_cache_clear.txt'  # Ścieżka do pliku z wynikami wydajności
output_path = 'results/tables'  # Ścieżka do zapisania tabeli wynikowej

parser = ResultParser(directory_path, performance_file_path)
cost_table = parser.calculate_total_cost_for_all_files()
print(cost_table)
# exit()
time_table = parser.generate_performance_table()

# Merge tables and save the result to the specified output path
parser.merge_tables_and_save(cost_table, time_table, output_path)
