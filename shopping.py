import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).
    """
    evidence = []
    labels = []

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            # Convert data types and append to evidence
            evidence.append([
                int(row[0]),  # Administrative
                float(row[1]),  # Administrative_Duration
                int(row[2]),  # Informational
                float(row[3]),  # Informational_Duration
                int(row[4]),  # ProductRelated
                float(row[5]),  # ProductRelated_Duration
                float(row[6]),  # BounceRates
                float(row[7]),  # ExitRates
                float(row[8]),  # PageValues
                float(row[9]),  # SpecialDay
                month_to_int(row[10]),  # Month
                int(row[11]),  # OperatingSystems
                int(row[12]),  # Browser
                int(row[13]),  # Region
                int(row[14]),  # TrafficType
                1 if row[15] == "Returning_Visitor" else 0,  # VisitorType
                1 if row[16] == "TRUE" else 0  # Weekend
            ])

            # Append label
            labels.append(1 if row[17] == "TRUE" else 0)

    return evidence, labels


def month_to_int(month):
    """
    Convert month abbreviation to an integer index.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months.index(month)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).
    """
    true_positives = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 1)
    true_negatives = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 0)
    total_positives = sum(labels)
    total_negatives = len(labels) - total_positives

    sensitivity = true_positives / total_positives
    specificity = true_negatives / total_negatives

    return sensitivity, specificity


if __name__ == "__main__":
    main()
