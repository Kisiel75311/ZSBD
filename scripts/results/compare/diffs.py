import difflib
import os

# Define directories
dirs = {
    "none": "./none/",
    "index": "./index/",
    "bitmapindex": "./bitmapindex/"
}

# Function to compare files and write HTML diff results
def compare_files(file1, file2, result_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    # Generate the diff in HTML format with ignoring whitespace
    diff_generator = difflib.HtmlDiff()
    diff_html = diff_generator.make_file(file1_lines, file2_lines, file1, file2, context=True, numlines=0)

    # Write the HTML diff to the result file
    with open(result_file, 'w') as f_out:
        f_out.write(diff_html)

# Iterate over all SQL files in the directories
for filename in os.listdir(dirs["none"]):
    none_file = os.path.join(dirs["none"], filename)

    # Compare none with index
    index_file = os.path.join(dirs["index"], "normal_" + filename.split("_")[1])
    if os.path.exists(index_file):
        result_filename = f"./results/diff_none_index_{filename.split('_')[1]}.html"
        compare_files(none_file, index_file, result_filename)

    # Compare none with bitmapindex
    bitmapindex_file = os.path.join(dirs["bitmapindex"], "bitmap_" + filename.split("_")[1])
    if os.path.exists(bitmapindex_file):
        result_filename = f"./results/diff_none_bitmapindex_{filename.split('_')[1]}.html"
        compare_files(none_file, bitmapindex_file, result_filename)

    # Compare index with bitmapindex
    if os.path.exists(index_file) and os.path.exists(bitmapindex_file):
        result_filename = f"./results/diff_index_bitmapindex_{filename.split('_')[1]}.html"
        compare_files(index_file, bitmapindex_file, result_filename)
