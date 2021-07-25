import os
import datetime
# from google.colab import drive
# drive.mount('/content/drive')

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import h5py

# CONSTANTS

OUT_STEPS = 19
MAX_EPOCHS = 50

# GLOBAL VARIABLES

multi_val_performance = {}
multi_performance = {}
train_df = None
val_df = None
test_df = None
num_features = []
column_indices = []
crop_type = []
caruid = []
history = []

def data_manipulation(csv_file):
  global multi_val_performance, multi_performance, train_df, val_df, test_df
  global num_features, column_indices, crop_type, caruid, history

  csv_path = r"C:/Users/Gramm/Downloads/{0}.csv".format(csv_file)
  split_path = csv_path.split("/")
  csv_split = split_path[-1].split("_")
  crop_type, caruid = csv_split[0], csv_split[1].split(".")[0]

  df = pd.read_csv(csv_path)
  date_time = df.pop('Year')

  # print(df)

  plot_cols = ['Yield']
  plot_features = df[plot_cols]
  plot_features.index = date_time
  _ = plot_features.plot(subplots=True)

  # print(plot_features)

  # print(df.describe().transpose())

  column_indices = {name: i for i, name in enumerate(df.columns)}

  n = len(df)
  train_df = df[0:int(n*0.7)]
  val_df = df[int(n*0.7):int(n*0.9)]
  test_df = df[int(n*0.9):]

  num_features = df.shape[1]

  train_mean = train_df.mean()
  train_std = train_df.std()

  train_df = (train_df - train_mean) / train_std
  val_df = (val_df - train_mean) / train_std
  test_df = (test_df - train_mean) / train_std

  # print(train_df)

  df_std = (df - train_mean) / train_std
  df_std = df_std.melt(var_name='Column', value_name='Normalized')
  plt.figure(figsize=(12, 6))
  ax = sns.violinplot(x='Column', y='Normalized', data=df_std)
  _ = ax.set_xticklabels(df.keys(), rotation=90)

class WindowGenerator():
  def __init__(self, input_width, label_width, shift,
               train_df, val_df, test_df,
               label_columns=None):
    # Store the raw data.
    self.train_df = train_df
    self.val_df = val_df
    self.test_df = test_df

    # Work out the label column indices.
    self.label_columns = label_columns
    if label_columns is not None:
      self.label_columns_indices = {name: i for i, name in
                                    enumerate(label_columns)}
    self.column_indices = {name: i for i, name in
                           enumerate(train_df.columns)}

    # Work out the window parameters.
    self.input_width = input_width
    self.label_width = label_width
    self.shift = shift

    self.total_window_size = input_width + shift

    self.input_slice = slice(0, input_width)
    self.input_indices = np.arange(self.total_window_size)[self.input_slice]

    self.label_start = self.total_window_size - self.label_width
    self.labels_slice = slice(self.label_start, None)
    self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

  def __repr__(self):
    return '\n'.join([
        f'Total window size: {self.total_window_size}',
        f'Input indices: {self.input_indices}',
        f'Label indices: {self.label_indices}',
        f'Label column name(s): {self.label_columns}'])

def split_window(self, features):
  inputs = features[:, self.input_slice, :]
  labels = features[:, self.labels_slice, :]
  if self.label_columns is not None:
      labels = tf.stack(
          [labels[:, :, self.column_indices[name]] for name in self.label_columns],
          axis=-1)

  # Slicing doesn't preserve static shape information, so set the shapes
  # manually. This way the `tf.data.Datasets` are easier to inspect.
  inputs.set_shape([None, self.input_width, None])
  labels.set_shape([None, self.label_width, None])

  return inputs, labels

def plot(self, model=None, plot_col='Yield', max_subplots=3):
  inputs, labels = self.example
  plt.figure(figsize=(12, 8))
  plot_col_index = self.column_indices[plot_col]
  max_n = min(max_subplots, len(inputs))
  for n in range(max_n):
    plt.subplot(max_n, 1, n+1)
    plt.ylabel(f'{plot_col} [normed]')
    plt.plot(self.input_indices, inputs[n, :, plot_col_index],
             label='Inputs', marker='.', zorder=-10)
    if self.label_columns:
      label_col_index = self.label_columns_indices.get(plot_col, None)
    else:
      label_col_index = plot_col_index

    if label_col_index is None:
      continue

    plt.scatter(self.label_indices, labels[n, :, label_col_index],
                edgecolors='k', label='Labels', c='#2ca02c', s=64)
    if model is not None:
      predictions = model(inputs)
      plt.scatter(self.label_indices, predictions[n, :, label_col_index],
                  marker='X', edgecolors='k', label='Predictions',
                  c='#ff7f0e', s=64)

    if n == 0:
      plt.legend()

  plt.xlabel('Time [3-Week Average]')

def make_dataset(self, data):
    data = np.array(data, dtype=np.float32)
    ds = tf.keras.preprocessing.timeseries_dataset_from_array(
        data=data,
        targets=None,
        sequence_length=self.total_window_size,
        sequence_stride=1,
        shuffle=True,
        batch_size=32,)

    ds = ds.map(self.split_window)

    return ds

@property
def train(self):
  return self.make_dataset(self.train_df)

@property
def val(self):
  return self.make_dataset(self.val_df)

@property
def test(self):
  return self.make_dataset(self.test_df)

@property
def example(self):
  """Get and cache an example batch of `inputs, labels` for plotting."""
  result = getattr(self, '_example', None)
  if result is None:
    # No example batch was found, so get one from the `.train` dataset
    result = next(iter(self.train))
    # And cache it for next time
    self._example = result
  return result

WindowGenerator.train = train
WindowGenerator.val = val
WindowGenerator.test = test
WindowGenerator.example = example
WindowGenerator.plot = plot
WindowGenerator.split_window = split_window
WindowGenerator.make_dataset = make_dataset

# !mkdir -p saved_model
# When training, change Barley_1100 to specific crop

def compile_and_fit(model, window, patience=5):
  # Checkpoint callback usage
  checkpoint_path = 'C:/Users/Gramm/Desktop/School/spring2021/GEOG481/Training/{0}/Checkpoints/{1}/cp.ckpt'.format(crop_type, caruid)
  # checkpoint_path = 'saved_model/Barley_1100/training_1/cp.ckpt'
  
  # Create a callback that saves the model's weights
  cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                  save_weights_only=True,
                                                  monitor='val_accuracy',
                                                  verbose=1)
  
  # Changed from meansquarederror() to SparseCategoricalCrossentropy()
  # optimizer changed from tf.optimizer.Adam() to 'adam'
  model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer='adam',
                metrics=[tf.metrics.MeanSquaredError()])

  history = model.fit(window.train, epochs=MAX_EPOCHS,
                      validation_data=window.val,
                      callbacks=[cp_callback])
  return history

def model_creation(): 
  multi_window = WindowGenerator(input_width=19,
                                label_width=OUT_STEPS,
                                shift=OUT_STEPS,
                                train_df=train_df,
                                val_df = val_df,
                                test_df = test_df)
  print(multi_window)

  CONV_WIDTH = 3
  multi_conv_model = tf.keras.Sequential([
      # Shape [batch, time, features] => [batch, CONV_WIDTH, features]
      tf.keras.layers.Lambda(lambda x: x[:, -CONV_WIDTH:, :]),
      # Shape => [batch, 1, conv_units]
      tf.keras.layers.Conv1D(256, activation='relu', kernel_size=(CONV_WIDTH)),
      # Shape => [batch, 1, out_steps*features]
      tf.keras.layers.Dense(OUT_STEPS*num_features,
                            kernel_initializer=tf.initializers.zeros()),
      # Shape => [batch, out_steps, features]
      tf.keras.layers.Reshape([OUT_STEPS, num_features])
  ])

  history = compile_and_fit(multi_conv_model, multi_window)

  IPython.display.clear_output()

  multi_val_performance['Conv'] = multi_conv_model.evaluate(multi_window.val, steps=1, verbose=1)
  multi_performance['Conv'] = multi_conv_model.evaluate(multi_window.test, steps=1, batch_size=32, verbose=1)
  print(multi_val_performance['Conv'])
  print(multi_performance['Conv'])
  # multi_window.plot(multi_conv_model)


  multi_conv_model.save('C:/Users/Gramm/Desktop/School/spring2021/GEOG481/Training/{0}/Models/{1}/model'.format(crop_type, caruid))

  print("Model Created")

def model_training():
  for i in range(20):
    multi_window = WindowGenerator(input_width=19,
                                  label_width=OUT_STEPS,
                                  shift=OUT_STEPS,
                                  train_df = train_df,
                                  val_df = val_df,
                                  test_df = test_df)

    new_model = tf.keras.models.load_model('C:/Users/Gramm/Desktop/School/spring2021/GEOG481/Training/{0}/Models/{1}/model'.format(crop_type, caruid))
    history = compile_and_fit(new_model, multi_window)

    new_model.save('C:/Users/Gramm/Desktop/School/spring2021/GEOG481/Training/{0}/Models/{1}/model'.format(crop_type, caruid))

  print(multi_window.test_df)
  multi_window.plot(new_model)
  print(multi_performance['Conv'])

barley_caruids = ["BARLEY_2401"]
canola_caruids = ["CANOLA_1300"]

for file in barley_caruids:
  data_manipulation(file)
  model_creation()