import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load digits dataset
digits = load_digits()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(digits.data)

# Train-test split with image indices
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
    X_scaled, digits.target, np.arange(len(digits.images)),
    test_size=0.3, random_state=42
)

# Define models
models = {
    "Logistic Regression": LogisticRegression(max_iter=10000, C=50.0, solver='lbfgs'),
    "SVM (RBF Kernel)": SVC(kernel='rbf', C=10, gamma=0.001),
    "KNN (k=3)": KNeighborsClassifier(n_neighbors=3)
}

results = {}

# Train and evaluate each model
for name, model in models.items():
    start_time = time.time()
    model.fit(X_train, y_train)
    duration = time.time() - start_time
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    
    results[name] = {
        "model": model,
        "accuracy": acc,
        "duration": duration,
        "report": report,
        "y_pred": y_pred,
        "confusion_matrix": cm
    }
    
    print(f"--- {name} ---")
    print(f"Training Time: {duration:.4f} seconds")
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

# Plot confusion matrices
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, (name, res) in zip(axes, results.items()):
    sns.heatmap(res["confusion_matrix"], annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title(f"{name}\nAccuracy: {res['accuracy']:.4f}\nTrain Time: {res['duration']:.2f}s")
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
plt.tight_layout()
plt.suptitle("Confusion Matrices for Models", fontsize=16, y=1.05)
plt.show()

# Sample prediction visualizer
def show_predictions(images, true_labels, pred_labels, title, n=8):
    plt.figure(figsize=(10, 4))
    for i in range(n):
        plt.subplot(2, 4, i + 1)
        plt.imshow(images[i], cmap='gray')
        plt.title(f'T:{true_labels[i]}\nP:{pred_labels[i]}')
        plt.axis('off')
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

# Show predictions from each model
test_images = digits.images[idx_test]
for name in models:
    print(f"\nSample predictions for {name}")
    show_predictions(
        test_images[:8],
        y_test[:8],
        results[name]["y_pred"][:8],
        title=f"{name} Predictions"
    )

# Function to plot classification report (bar chart)
def plot_classification_report_bars(report_dict, model_name):
    classes = list(map(str, range(10)))
    metrics = ['precision', 'recall', 'f1-score']
    
    # Collecting per-class metrics
    class_metrics = {metric: [report_dict[digit][metric] for digit in classes] for metric in metrics}
    
    # Append macro and weighted avg
    class_metrics['precision'].extend([
        report_dict['macro avg']['precision'],
        report_dict['weighted avg']['precision']
    ])
    class_metrics['recall'].extend([
        report_dict['macro avg']['recall'],
        report_dict['weighted avg']['recall']
    ])
    class_metrics['f1-score'].extend([
        report_dict['macro avg']['f1-score'],
        report_dict['weighted avg']['f1-score']
    ])
    class_labels = classes + ['macro avg', 'weighted avg']

    # X positions for the bars
    x = np.arange(len(class_labels))
    width = 0.25

    # Create a figure for the bar chart
    plt.figure(figsize=(14, 6))

    for i, metric in enumerate(metrics):
        plt.bar(x + i*width, class_metrics[metric], width=width, label=metric.capitalize())

    plt.xticks(x + width, class_labels, rotation=45)
    plt.ylim(0.0, 1.1)
    plt.ylabel("Score")
    plt.title(f"Classification Metrics per Class: {model_name}")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Function to plot classification report (table)
def plot_classification_report_table(report_dict, model_name):
    classes = list(map(str, range(10)))
    class_labels = classes + ['macro avg', 'weighted avg']
    
    # Collecting metrics for table
    table_data = np.array([
        [report_dict[digit]['precision'] for digit in classes] + [report_dict['macro avg']['precision'], report_dict['weighted avg']['precision']],
        [report_dict[digit]['recall'] for digit in classes] + [report_dict['macro avg']['recall'], report_dict['weighted avg']['recall']],
        [report_dict[digit]['f1-score'] for digit in classes] + [report_dict['macro avg']['f1-score'], report_dict['weighted avg']['f1-score']]
    ]).T  # Transpose to match row/column format

    # Create a figure for the table
    fig, ax = plt.subplots(figsize=(14, 6))  # Create a new figure for the table

    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=table_data,
                     colLabels=['Precision', 'Recall', 'F1-Score'],
                     rowLabels=class_labels,
                     loc='center',
                     cellLoc='center', colColours=["lightgray"] * 3)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.title(f"Classification Report Table: {model_name}")
    plt.show()

# Load digits dataset
digits = load_digits()

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    digits.data, digits.target, test_size=0.3, random_state=42)

# Models and training
models = {
    'Logistic Regression': LogisticRegression(max_iter=10000),
    'SVM': SVC(),
    'KNN': KNeighborsClassifier()
}

results = {}

# Train each model and generate reports
for name, model in models.items():
    start_time = time.time() 
    model.fit(X_train, y_train)
    training_time = time.time() - start_time

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    results[name] = {
        'report': report,
        'training_time': training_time
    }

# Plot classification reports (bar charts) and tables separately for each model
for name, res in results.items():
    plot_classification_report_bars(res["report"], name)  # Plot bar chart
    plot_classification_report_table(res["report"], name)  # Plot table

# Print training times
for name, res in results.items():
    print(f"{name} Training Time: {res['training_time']:.4f} seconds")