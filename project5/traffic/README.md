# Experimental process 

From the exercise:
```
 You may wish to experiment with:

    different numbers of convolutional and pooling layers
    different numbers and sizes of filters for convolutional layers
    different pool sizes for pooling layers
    different numbers and sizes of hidden layers
    dropout
``` 

<br/>

### First iteration of the model
```
model = tf.keras.models.Sequential([

    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH,  IMG_HEIGHT, 3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),

    # Add an output layer with output units for all categories
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
```
Taken from the lecture source code, and slightly adapted to suit the exercise, as a starting point. 
Accuracy for training after ten epochs was around 0.80-0.88, with a loss of about 0.35 - 0.60 over several runs.
Whereas, for testing the accuracy was around 0.95 with a loss of 0.16-0.20.

<br/>

### Second iteration of the model
Changing numbers and sizes of filters for convolutional layers.
```
...
# Convolutional layer. Learn 32 filters using a 3x3 kernel
tf.keras.layers.Conv2D(
    64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
),
...
```
Changing the number of filters to 64, resulted in an accuracy of around 0.80-0.88 and a loss of 0.30-0.56 for training after ten epochs for several runs. For testing of the model an accuracy of around 0.97-0.98 with a loss of 0.08-0.15 was seen.
When increasing the size of the filter from (3, 3) to (5, 5) a minimal increase in accuracy and minimal decrease in loss were seen for both training and testing the model (increase of 0.05-0.1 in accuracy and decrease of around 0.1 in loss). However, the time to complete each epoch increased slightly from approximately 15-20s to 25-40s when training the model.  Whereas when the number of filters was set to 128 with a filter size of (3, 3) similar accuracy and loss was achieved compared to the filter sizes 32 and 64, however the time to achieve this was noticeably longer (> 40s with around 70ms/step). As for setting the the number of filters to 128 with a filter size to (5, 5), the time to complete the individual epochs was similar compared to a filter size of (3, 3) with similar accuracy and loss as well.
In conclusion further iterations will be continued with the number of filters set to 64 and a filter size of (3, 3), as only minimal improvements were seen in accuracy and loss with other settings while time to finish epochs during training increased noticeably.

<br/>

### Third iteration of the model
Different numbers of convolutional and pooling layers.
```
# Convolutional layer. Learn 64 filters using a 3x3 kernel
tf.keras.layers.Conv2D(
    64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
),

# Max-pooling layer, using 2x2 pool size
tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

# Convolutional layer. Learn 64 filters using a 3x3 kernel
tf.keras.layers.Conv2D(
    64, (3, 3), activation="relu"
),

# Max-pooling layer, using 2x2 pool size
tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
```
First another convolutional layer was added with the number of filters set to 64 with a filter of (3, 3). Time to complete epochs barely increased while accuracy increased and loss decreased compared to the model without an added convolutional layer. Interestingly, adding another Max-pooling layer resulted in similar accuracy and loss with an decreased time to complete the epochs during training. Thus, resulting in a faster model around 14s and 27ms/step compared to 20s and 35ms/step). Hence continuing to the fourth iteration with adding an additional convolutional and max-pooling layer.

<br/>

### Fourth iteration of the model
different pool sizes for pooling layers
```
# Max-pooling layer, using 2x2 pool size
tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
```
Increasing the pool sizes for the pooling layers from (2, 2) to (3, 3) had no noticeable effect on training time. However it resulted in slightly lower accuracy and higher loss during the validation of the model. Thus, sticking to the pooling size of (2, 2) for the remainder of the iterations seemed more reasonable.


<br/>

### Fifth iteration of the model
Different numbers and sizes of hidden layers and dropout.
```
# Add a hidden layer with dropout
tf.keras.layers.Dense(512, activation="relu"),
tf.keras.layers.Dropout(0.5),
```
Removing the dropout completely resulted in a loss close to 0, which is unwelcome as it means that the model is probably overfitted. Hence keeping in the 0.5 dropout in the model. Furthermore, inceasing the size of the hidden layer from 128 to 256 yielded no noticeable differences. Nevertheless increasing it to 512 resulted in a higher accuracy, close to 0.99 over serveral runs, without adding much time to finish epochs during training. Therefore a size of 512 seemed reasonable to include in the final iteration of the model. 