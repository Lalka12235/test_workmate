import argparse
import sys
from collections import defaultdict

def read_csv_files(file_paths: list[str]):
    all_employees = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                
                if not lines:
                    continue
                
                headers = [h.strip() for h in lines[0].split(',')]
                
                for line in lines[1:]:
                    values = [v.strip() for v in line.split(',')]
                    if len(values) != len(headers):
                        continue
                    
                    employee = dict(zip(headers, values))
                    
                    # Нормализация названий полей
                    rate_fields = ['hourly_rate', 'rate', 'salary']
                    for field in rate_fields:
                        if field in employee:
                            employee['rate'] = float(employee[field])
                            break
                    
                    employee['hours_worked'] = float(employee.get('hours_worked', 0))
                    employee['payout'] = employee['hours_worked'] * employee['rate']
                    all_employees.append(employee)
                    
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден", file=sys.stderr)
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}", file=sys.stderr)
    
    return all_employees

def generate_payout_report(employees: list[dict]):
    departments = defaultdict(list)
    for emp in employees:
        departments[emp['department']].append(emp)

    dept_order = ['Design', 'HR', 'Marketing', 'Sales']
    sorted_departments = sorted(departments.keys(), key=lambda d: dept_order.index(d) if d in dept_order else d)

    total_hours_all = 0
    total_payout_all = 0

    for dept in sorted_departments:
        emp_list = sorted(departments[dept], key=lambda x: x['name'])

        print(f"{dept}")
        print("-" * len(dept))

        # Заголовки
        print(f"{'name':<22} {'hours':>5} {'rate':>5} {'payout':>8}")
        print(f"{'-'*22} {'-'*5} {'-'*5} {'-'*8}")

        dept_hours = 0
        dept_payout = 0

        for emp in emp_list:
            name = emp['name']
            hours = int(emp['hours_worked'])
            rate = int(emp['rate'])
            payout = emp['payout']

            dept_hours += hours
            dept_payout += payout

            print(f"{name:<22} {hours:>5} {rate:>5} ${payout:>7,.0f}")

        print(f"{'':<22} {dept_hours:>5}       ${dept_payout:>7,.0f}")
        print()

        total_hours_all += dept_hours
        total_payout_all += dept_payout

    print(f"{'':<22} {total_hours_all:>5}       ${total_payout_all:>7,.0f}")


def main():
    parser = argparse.ArgumentParser(description='Генерация отчетов о выплатах из CSV файлов')
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', required=True, help='Тип отчета (payout)')
    
    args = parser.parse_args()
    
    if args.report.lower() != 'payout':
        print("Ошибка: Поддерживается только отчет типа 'payout'", file=sys.stderr)
        sys.exit(1)
    
    employees_data = read_csv_files(args.files)
    report = generate_payout_report(employees_data)
    print(report)

if __name__ == '__main__':
    main()