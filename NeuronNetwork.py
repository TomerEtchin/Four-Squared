import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# Load the Q-table data
with open('Board-QTable.json', 'r') as f:
    data = json.load(f)




X_list = []
y_list = []
char_to_int = {'X': -1, '0': 0, '1' : 1, '2' : 2 }

for key, value in data.items():
    X_list.append([char_to_int[char] for char in key])
    y_list.append(value[0])

X = np.array(X_list)
y = np.array(y_list)






print("Dataset size:", X.shape, "features,", y.shape, "labels")

# Split into training and test sets (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("Train/test split:", X_train.shape, X_test.shape)

# === Build the Keras model ===
model = Sequential([
    Dense(64, activation='relu', input_shape=(34,)),  # 34 inputs
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')  # Output score between 0 and 1
])

# Compile the model
model.compile(optimizer=Adam(),
              loss='mean_squared_error',
              metrics=['mae'])

# Train the model
history = model.fit(X_train, y_train,
                    validation_split=0.2,
                    epochs=20,
                    batch_size=32,
                    verbose=1)

# Evaluate the model
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss:.4f}, Test MAE: {test_mae:.4f}")

# Predict on new data
predictions = model.predict(X_test[:5])
print("Predictions for the first 5 rows:", predictions)

# Save the model for later use in ANNAgent
model.save("ann_model.keras")

plt.figure(figsize=(15, 6))

# Loss plot
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# MAE plot
plt.subplot(1, 2, 2)
plt.plot(history.history['mae'], label='Training MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('Training and Validation MAE')
plt.xlabel('Epochs')
plt.ylabel('Mean Absolute Error')
plt.legend()

plt.tight_layout()
plt.show()
