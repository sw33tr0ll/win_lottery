from requests_html import HTMLSession
import csv
from collections import Counter
import random

def fetch_and_save_powerball_data():
    csv_file = open('powerball_numbers.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['drawdate','ball1','ball2','ball3','ball4','ball5','powerball'])

    # From years 2020 to 2023
    for year in reversed(range(1999, 2025)):
        session = HTMLSession()
        r = session.get(f'https://www.powerball.net/archive/{year}')
        archive_boxes = r.html.find('.archive-box')

        for archive_box in archive_boxes:
            drawdate = archive_box.attrs['href'].split('/')[2]
            balls = [ball.text for ball in archive_box.find('.ball')]
            powerball = archive_box.find('.powerball', first=True).text
            
            csv_writer.writerow([drawdate, *balls, powerball])

    csv_file.close()

def load_data_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

def find_top_numbers(data, n=3):
    numbers = []
    for row in data:
        numbers.extend([int(row['ball1']), int(row['ball2']), int(row['ball3']), int(row['ball4']), int(row['ball5'])])
    
    number_counts = Counter(numbers)
    top_numbers = [num for num, count in number_counts.most_common(n)]
    return top_numbers

def generate_sequence(top_numbers):
    sequence = top_numbers[:]
    while len(sequence) < 5:
        num = random.randint(1, 69)
        if num not in sequence:
            sequence.append(num)
    sequence.sort()
    return tuple(sequence)

def generate_recommended_sequences(data, top_numbers, num_sequences=10):
    historical_sequences = set(tuple(sorted([int(row['ball1']), int(row['ball2']), int(row['ball3']), int(row['ball4']), int(row['ball5'])])) for row in data)
    
    recommended_sequences = set()
    while len(recommended_sequences) < num_sequences:
        sequence = generate_sequence(top_numbers)
        if sequence not in historical_sequences:
            recommended_sequences.add(sequence)
    
    return recommended_sequences

def main():
    # Fetch and save the data
    fetch_and_save_powerball_data()

    # Load the data
    data = load_data_from_csv('powerball_numbers.csv')
    print(data[:5])

    # Find the top 3 most picked numbers
    top_3_numbers = find_top_numbers(data)
    print("Top 3 Most Picked Numbers:", top_3_numbers)

    # Generate the recommended sequences
    recommended_sequences = generate_recommended_sequences(data, top_3_numbers)
    print("Top 10 Recommended Sequences:")
    for seq in recommended_sequences:
        print(seq)

if __name__ == "__main__":
    main()