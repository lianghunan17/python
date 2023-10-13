# python
python
import csv
import os
import string

def split_csv_by_range(input_file_path, output_dir, primary_column, backup_column, char_range):
    encoding = 'cp932'
    file_handlers = {}
    writers = {}
    row_counts = {}

    with open(input_file_path, mode='r', encoding=encoding) as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            first_char = get_first_character(row, primary_column, backup_column)
            matched = False
            for r in char_range:
                if r == '文字と数字以外':
                    continue
                if '-' in r:
                    start_char, end_char = r.split('-')
                    if start_char <= first_char <= end_char:
                        matched = True
                elif first_char == r:
                    matched = True
                
                if matched:
                    if r not in file_handlers:
                        output_file_path = os.path.join(output_dir, f'{r}.csv')
                        file_handlers[r] = open(output_file_path, mode='w', encoding='cp932', newline='')
                        writers[r] = csv.DictWriter(file_handlers[r], fieldnames=reader.fieldnames)
                        writers[r].writeheader()
                        row_counts[r] = 0
                    writers[r].writerow(row)
                    row_counts[r] += 1
                    break
            
            if not matched:
                r = '文字と数字以外'
                if r not in file_handlers:
                    output_file_path = os.path.join(output_dir, f'{r}.csv')
                    file_handlers[r] = open(output_file_path, mode='w', encoding='cp932', newline='')
                    writers[r] = csv.DictWriter(file_handlers[r], fieldnames=reader.fieldnames)
                    writers[r].writeheader()
                    row_counts[r] = 0
                writers[r].writerow(row)
                row_counts[r] += 1

        for _, handler in file_handlers.items():
            handler.close()

    summary_file_path = os.path.join(output_dir, "分割のファイル数情報.csv")
    with open(summary_file_path, 'w', encoding='cp932', newline='') as summary_file:
        writer = csv.DictWriter(summary_file, fieldnames=['ファイル名', '数'])
        writer.writeheader()
        for r in row_counts.keys():
            writer.writerow({'ファイル名': f'{r}.csv', '数': row_counts[r]})

def get_first_character(row, primary_column, backup_column):
    primary_val = row[primary_column]
    if primary_val:
        return primary_val[0].upper()
    backup_val = row[backup_column]
    if backup_val:
        return backup_val[0].upper()
    return primary_val[0].upper() if primary_val else ""

input_file_path = 'C:\\Users\\ryo.kohnan\\Desktop\\梁\\SQL\\データ\\export_case_test_20230522.csv'
output_dir = 'C:\\Users\\ryo.kohnan\\Desktop\\梁\\SQL\\データ'
primary_column = 'CONTACTEMAIL'
backup_column = 'SUPPLIEDEMAIL'
char_range = ['A', 'B'] + list(string.ascii_uppercase[2:]) + ['0-9', '文字と数字以外']

split_csv_by_range(input_file_path, output_dir, primary_column, backup_column, char_range)


CSVフェイルを仕分けする。
![image](https://github.com/lianghunan17/python/assets/50505315/88b8be5d-9ec2-4ccd-8bdf-c08e3247ce70)
