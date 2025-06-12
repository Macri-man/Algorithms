import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.utils import to_categorical
from scipy import signal

# Parameters
timesteps = 20
num_classes = 3

# Generate signals
x = np.linspace(0, 100, 1000)
sine = np.sin(x)
square = signal.square(x)
sawtooth = signal.sawtooth(x)

# Combine waveforms and labels
waves = [sine, square, sawtooth]
wave_names = ['Sine', 'Square', 'Sawtooth']
X = []
Y = []

# Create labeled training sequences
for label, wave in enumerate(waves):
    for i in range(len(wave) - timesteps):
        X.append(wave[i:i+timesteps])
        Y.append(label)

X = np.array(X)
Y = np.array(Y)
X = X.reshape((X.shape[0], timesteps, 1))
Y_cat = to_categorical(Y, num_classes)

# --- Visualization: Raw Waveform Sequences ---
plt.figure(figsize=(12, 4))
colors = ['blue', 'green', 'red']
for class_id in range(3):
    plt.subplot(1, 3, class_id + 1)
    # Plot 5 random sequences from each class
    idxs = np.where(Y == class_id)[0][:5]
    for idx in idxs:
        plt.plot(X[idx].squeeze(), color=colors[class_id], alpha=0.6)
    plt.title(f"{wave_names[class_id]} samples")
    plt.ylim(-1.5, 1.5)
    plt.grid(True)
plt.suptitle("Raw Waveform Input Sequences (Before Training)")
plt.tight_layout()
plt.show()

# --- Model definition ---
inputs = Input(shape=(timesteps, 1))
lstm_out = LSTM(50)(inputs)
outputs = Dense(num_classes, activation='softmax')(lstm_out)
model = Model(inputs, outputs)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, Y_cat, epochs=10, batch_size=32)

# Intermediate model to extract LSTM output features
intermediate_model = Model(inputs=model.input, outputs=model.get_layer(index=1).output)
lstm_outputs = intermediate_model.predict(X)  # Shape: (samples, 50)

# --- Visualization: t-SNE after training ---
tsne = TSNE(n_components=2, random_state=42)
reduced = tsne.fit_transform(lstm_outputs)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=Y, cmap='tab10', s=8)
plt.title("t-SNE of LSTM Outputs After Training (Waveform Classification)")
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.colorbar(label="Class (0=Sine, 1=Square, 2=Sawtooth)")
plt.grid(True)
plt.show()
