#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# ## Paso 1: Cargar los datos.
# Levantamos los datos de los pacientes

# In[ ]:


# Read data from file

import numpy as np
import pandas as pd

file_name = './datos_de_pacientes_5000.csv'
data = pd.read_csv(file_name, index_col=0)


# In[ ]:


print(data)


# ## Paso 2: Preprocesar los datos.
# 
# Separamos los datos de entrada de las etiquetas
# 
# Separamos conjuntos de training, validación y testing según sea necesario

# In[ ]:


# Date preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Scaling numerical variables
scaler = MinMaxScaler()

# Separate the data from the target labels
X = data.drop(['riesgo_cardiaco'], axis=1)
y = np.array(data['riesgo_cardiaco'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# For training set
scaled_X_train = scaler.fit_transform(X_train)
scaled_X_train = pd.DataFrame(scaled_X_train, columns=X_train.columns)

# For testing set
scaled_X_test = scaler.fit_transform(X_test)
scaled_X_test = pd.DataFrame(scaled_X_test, columns=X_test.columns)


# In[ ]:


print(scaled_X_train)


# ##Paso 3: Armo la red

# In[ ]:


# Build the Neural Network
import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Create the model
model = Sequential()

# 6 INPUT (colesterol, presión, glucosa, edad, sobrepeso, tabaquismo)
model.add(Dense(50, input_shape=(6,), activation='relu', kernel_initializer='uniform'))
model.add(Dense(25, activation='relu', kernel_initializer='random_normal'))
model.add(Dense(35, activation='relu', kernel_initializer='random_normal'))
model.add(Dense(1, activation='sigmoid')) # Sigmoid activation in the output layer

# Compile
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01))
model.summary()


# ##Paso 4: Entreno la red neuronal

# In[ ]:


# Training
model.fit(X_train, y_train, verbose=2, batch_size = 10000, epochs=50)


# ##Paso 5: Evaluo la red

# In[ ]:


# Evaluate
result = model.evaluate(X_test, y_test)
print(result)

