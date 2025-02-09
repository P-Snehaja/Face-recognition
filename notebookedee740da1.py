{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.12","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"none","dataSources":[{"sourceId":1351797,"sourceType":"datasetVersion","datasetId":786787},{"sourceId":6246646,"sourceType":"datasetVersion","datasetId":3589407}],"dockerImageVersionId":30527,"isInternetEnabled":false,"language":"python","sourceType":"script","isGpuEnabled":false}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:16:21.622497Z\",\"iopub.execute_input\":\"2023-08-04T14:16:21.622878Z\",\"iopub.status.idle\":\"2023-08-04T14:16:33.774223Z\",\"shell.execute_reply.started\":\"2023-08-04T14:16:21.622847Z\",\"shell.execute_reply\":\"2023-08-04T14:16:33.773049Z\"}}\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sn\nimport skimage.io\nimport keras.backend as K\nimport tensorflow as tf\nfrom tensorflow.keras.preprocessing.image import ImageDataGenerator\nfrom tensorflow.keras.preprocessing.image import load_img\nfrom tensorflow.keras.utils import load_img\nfrom tensorflow.keras.applications import ResNet50\nfrom tensorflow.keras.layers import Dense, Flatten, Dropout,BatchNormalization ,Activation\nfrom tensorflow.keras.models import Model, Sequential\nfrom keras.applications.nasnet import NASNetLarge\nfrom tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping\nfrom tensorflow.keras.optimizers import Adam\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:16:33.775882Z\",\"iopub.execute_input\":\"2023-08-04T14:16:33.776631Z\",\"iopub.status.idle\":\"2023-08-04T14:16:33.783595Z\",\"shell.execute_reply.started\":\"2023-08-04T14:16:33.776601Z\",\"shell.execute_reply\":\"2023-08-04T14:16:33.782472Z\"}}\ntrain_datagen = ImageDataGenerator(rescale = 1./255,\n                                   validation_split = 0.2,\n                                  \n        rotation_range=5,\n        width_shift_range=0.2,\n        height_shift_range=0.2,\n        shear_range=0.2,\n        #zoom_range=0.2,\n        horizontal_flip=True,\n        vertical_flip=True,\n        fill_mode='nearest')\n\nvalid_datagen = ImageDataGenerator(rescale = 1./255,\n                                  validation_split = 0.2)\n\ntest_datagen  = ImageDataGenerator(rescale = 1./255\n                                  )\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:16:33.785231Z\",\"iopub.execute_input\":\"2023-08-04T14:16:33.785685Z\",\"iopub.status.idle\":\"2023-08-04T14:17:01.181484Z\",\"shell.execute_reply.started\":\"2023-08-04T14:16:33.785639Z\",\"shell.execute_reply\":\"2023-08-04T14:17:01.180668Z\"}}\ntrain_dataset  = train_datagen.flow_from_directory(directory = '../input/fer2013/train',\n                                                   target_size = (48,48),\n                                                   class_mode = 'categorical',\n                                                   subset = 'training',\n                                                   batch_size = 64)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:01.183163Z\",\"iopub.execute_input\":\"2023-08-04T14:17:01.184063Z\",\"iopub.status.idle\":\"2023-08-04T14:17:07.423778Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:01.184031Z\",\"shell.execute_reply\":\"2023-08-04T14:17:07.422473Z\"}}\nvalid_dataset = valid_datagen.flow_from_directory(directory = '../input/fer2013/train',\n                                                  target_size = (48,48),\n                                                  class_mode = 'categorical',\n                                                  subset = 'validation',\n                                                  batch_size = 64)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:07.425026Z\",\"iopub.execute_input\":\"2023-08-04T14:17:07.425352Z\",\"iopub.status.idle\":\"2023-08-04T14:17:14.902602Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:07.425321Z\",\"shell.execute_reply\":\"2023-08-04T14:17:14.901785Z\"}}\ntest_dataset = test_datagen.flow_from_directory(directory = '../input/fer2013/test',\n                                                  target_size = (48,48),\n                                                  class_mode = 'categorical',\n                                                  batch_size = 64)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:14.903580Z\",\"iopub.execute_input\":\"2023-08-04T14:17:14.904818Z\",\"iopub.status.idle\":\"2023-08-04T14:17:15.140657Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:14.904768Z\",\"shell.execute_reply\":\"2023-08-04T14:17:15.138861Z\"}}\nfrom tensorflow.keras.preprocessing import image\nimg = image.load_img(\"/kaggle/input/fer2013/test/happy/PrivateTest_10077120.jpg\",target_size=(48,48))\nimg = np.array(img)\nplt.imshow(img)\nprint(img.shape)\n\nimg = np.expand_dims(img, axis=0)\nfrom keras.models import load_model\nprint(img.shape)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:15.142776Z\",\"iopub.execute_input\":\"2023-08-04T14:17:15.143257Z\",\"iopub.status.idle\":\"2023-08-04T14:17:16.796180Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:15.143223Z\",\"shell.execute_reply\":\"2023-08-04T14:17:16.794697Z\"}}\nimport tensorflow as tf\nfrom tensorflow.keras.applications import ResNet50\n\nbase_model = ResNet50(input_shape=(48, 48, 3), include_top=False, weights=None)\n\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:16.797448Z\",\"iopub.execute_input\":\"2023-08-04T14:17:16.797796Z\",\"iopub.status.idle\":\"2023-08-04T14:17:16.807790Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:16.797766Z\",\"shell.execute_reply\":\"2023-08-04T14:17:16.806883Z\"}}\nfor layer in base_model.layers[:-4]:\n    layer.trainable=False\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:16.811590Z\",\"iopub.execute_input\":\"2023-08-04T14:17:16.811898Z\",\"iopub.status.idle\":\"2023-08-04T14:17:17.406327Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:16.811873Z\",\"shell.execute_reply\":\"2023-08-04T14:17:17.405266Z\"}}\nmodel=Sequential()\n\nmodel.add(base_model)\nmodel.add(Dropout(0.5))\nmodel.add(Flatten())\nmodel.add(BatchNormalization())\nmodel.add(Dense(32,kernel_initializer='he_uniform'))\nmodel.add(BatchNormalization())\nmodel.add(Activation('relu'))\nmodel.add(Dropout(0.5))\nmodel.add(Dense(32,kernel_initializer='he_uniform'))\nmodel.add(BatchNormalization())\nmodel.add(Activation('relu'))\nmodel.add(Dropout(0.5))\nmodel.add(Dense(32,kernel_initializer='he_uniform'))\nmodel.add(BatchNormalization())\nmodel.add(Activation('relu'))\nmodel.add(Dense(7,activation='softmax'))\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:17.409980Z\",\"iopub.execute_input\":\"2023-08-04T14:17:17.410443Z\",\"iopub.status.idle\":\"2023-08-04T14:17:17.475668Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:17.410415Z\",\"shell.execute_reply\":\"2023-08-04T14:17:17.474407Z\"}}\nmodel.summary()\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:17.476952Z\",\"iopub.execute_input\":\"2023-08-04T14:17:17.477344Z\",\"iopub.status.idle\":\"2023-08-04T14:17:17.826138Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:17.477316Z\",\"shell.execute_reply\":\"2023-08-04T14:17:17.825013Z\"}}\nfrom tensorflow.keras.utils import plot_model\nfrom IPython.display import Image\nplot_model(model, to_file='convnet.png', show_shapes=True,show_layer_names=True)\nImage(filename='convnet.png') \n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:17.827359Z\",\"iopub.execute_input\":\"2023-08-04T14:17:17.827720Z\",\"iopub.status.idle\":\"2023-08-04T14:17:17.835645Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:17.827684Z\",\"shell.execute_reply\":\"2023-08-04T14:17:17.834719Z\"}}\ndef f1_score(y_true, y_pred): #taken from old keras source code\n    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))\n    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))\n    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))\n    precision = true_positives / (predicted_positives + K.epsilon())\n    recall = true_positives / (possible_positives + K.epsilon())\n    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())\n    return f1_val\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:17.837313Z\",\"iopub.execute_input\":\"2023-08-04T14:17:17.837755Z\",\"iopub.status.idle\":\"2023-08-04T14:17:17.877701Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:17.837722Z\",\"shell.execute_reply\":\"2023-08-04T14:17:17.876705Z\"}}\nMETRICS = [\n      tf.keras.metrics.BinaryAccuracy(name='accuracy'),\n      tf.keras.metrics.Precision(name='precision'),\n      tf.keras.metrics.Recall(name='recall'),  \n      tf.keras.metrics.AUC(name='auc'),\n        f1_score,\n]\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:17.879101Z\",\"iopub.execute_input\":\"2023-08-04T14:17:17.879449Z\",\"iopub.status.idle\":\"2023-08-04T14:17:17.886454Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:17.879418Z\",\"shell.execute_reply\":\"2023-08-04T14:17:17.884793Z\"}}\nlrd = ReduceLROnPlateau(monitor = 'val_loss',patience = 20,verbose = 1,factor = 0.50, min_lr = 1e-10)\n\nmcp = ModelCheckpoint('model.h5')\n\nes = EarlyStopping(verbose=1, patience=20)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:17.888861Z\",\"iopub.execute_input\":\"2023-08-04T14:17:17.889269Z\",\"iopub.status.idle\":\"2023-08-04T14:17:17.918009Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:17.889237Z\",\"shell.execute_reply\":\"2023-08-04T14:17:17.916677Z\"}}\nmodel.compile(optimizer='Adam', loss='categorical_crossentropy',metrics=METRICS)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:17:17.919530Z\",\"iopub.execute_input\":\"2023-08-04T14:17:17.919838Z\",\"iopub.status.idle\":\"2023-08-04T14:44:56.594349Z\",\"shell.execute_reply.started\":\"2023-08-04T14:17:17.919814Z\",\"shell.execute_reply\":\"2023-08-04T14:44:56.592583Z\"}}\nhistory=model.fit(train_dataset,validation_data=valid_dataset,epochs = 10,verbose = 1,callbacks=[lrd,mcp,es])\n\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:44:56.596820Z\",\"iopub.execute_input\":\"2023-08-04T14:44:56.597245Z\",\"iopub.status.idle\":\"2023-08-04T14:44:57.530735Z\",\"shell.execute_reply.started\":\"2023-08-04T14:44:56.597210Z\",\"shell.execute_reply\":\"2023-08-04T14:44:57.529198Z\"}}\ndef Train_Val_Plot(acc,val_acc,loss,val_loss,auc,val_auc,precision,val_precision,f1,val_f1):\n    \n    fig, (ax1, ax2,ax3,ax4,ax5) = plt.subplots(1,5, figsize= (20,5))\n    fig.suptitle(\" MODEL'S METRICS VISUALIZATION \")\n\n    ax1.plot(range(1, len(acc) + 1), acc)\n    ax1.plot(range(1, len(val_acc) + 1), val_acc)\n    ax1.set_title('History of Accuracy')\n    ax1.set_xlabel('Epochs')\n    ax1.set_ylabel('Accuracy')\n    ax1.legend(['training', 'validation'])\n\n\n    ax2.plot(range(1, len(loss) + 1), loss)\n    ax2.plot(range(1, len(val_loss) + 1), val_loss)\n    ax2.set_title('History of Loss')\n    ax2.set_xlabel('Epochs')\n    ax2.set_ylabel('Loss')\n    ax2.legend(['training', 'validation'])\n    \n    ax3.plot(range(1, len(auc) + 1), auc)\n    ax3.plot(range(1, len(val_auc) + 1), val_auc)\n    ax3.set_title('History of AUC')\n    ax3.set_xlabel('Epochs')\n    ax3.set_ylabel('AUC')\n    ax3.legend(['training', 'validation'])\n    \n    ax4.plot(range(1, len(precision) + 1), precision)\n    ax4.plot(range(1, len(val_precision) + 1), val_precision)\n    ax4.set_title('History of Precision')\n    ax4.set_xlabel('Epochs')\n    ax4.set_ylabel('Precision')\n    ax4.legend(['training', 'validation'])\n    \n    ax5.plot(range(1, len(f1) + 1), f1)\n    ax5.plot(range(1, len(val_f1) + 1), val_f1)\n    ax5.set_title('History of F1-score')\n    ax5.set_xlabel('Epochs')\n    ax5.set_ylabel('F1 score')\n    ax5.legend(['training', 'validation'])\n\n\n    plt.show()\n    \n\nTrain_Val_Plot(history.history['accuracy'],history.history['val_accuracy'],\n               history.history['loss'],history.history['val_loss'],\n               history.history['auc'],history.history['val_auc'],\n               history.history['precision'],history.history['val_precision'],\n               history.history['f1_score'],history.history['val_f1_score']\n              )\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:44:57.540150Z\",\"iopub.execute_input\":\"2023-08-04T14:44:57.540445Z\",\"iopub.status.idle\":\"2023-08-04T14:44:57.558909Z\",\"shell.execute_reply.started\":\"2023-08-04T14:44:57.540418Z\",\"shell.execute_reply\":\"2023-08-04T14:44:57.557477Z\"}}\nhistory.history['accuracy']\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2023-08-04T14:44:57.561175Z\",\"iopub.execute_input\":\"2023-08-04T14:44:57.561585Z\",\"iopub.status.idle\":\"2023-08-04T14:45:02.292254Z\",\"shell.execute_reply.started\":\"2023-08-04T14:44:57.561546Z\",\"shell.execute_reply\":\"2023-08-04T14:45:02.291179Z\"}}\nfrom tensorflow.keras.preprocessing import image\nimport numpy as np\n\n# Load the image\nimg = image.load_img(\"/kaggle/input/fer2013/test/happy/PrivateTest_10077120.jpg\", target_size=(48, 48))\n\n# Convert the image to an array and preprocess it\nimg_array = image.img_to_array(img)\nimg_array = img_array / 255.0  # Normalize pixel values to [0, 1]\nimg_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension\n\nimport tensorflow as tf\n\ndef f1_score(y_true, y_pred):\n    y_true = tf.cast(y_true, tf.float32)\n    y_pred = tf.round(tf.clip_by_value(y_pred, 0, 1))\n    tp = tf.reduce_sum(y_true * y_pred)\n    fp = tf.reduce_sum(y_pred) - tp\n    fn = tf.reduce_sum(y_true) - tp\n    precision = tp / (tp + fp + tf.keras.backend.epsilon())\n    recall = tp / (tp + fn + tf.keras.backend.epsilon())\n    f1 = 2 * precision * recall / (precision + recall + tf.keras.backend.epsilon())\n    return f1\n\n\n# Load the model\nfrom keras.models import load_model\n\nmodel_path = '/kaggle/input/modelh5/model.h5'\nmodel = load_model(model_path, custom_objects={'f1_score': f1_score})\n\n\n# Make predictions\npredictions = model.predict(img_array)\nmax_index = np.argmax(predictions[0])\nemotion_detection = ('angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise')\nemotion_prediction = emotion_detection[max_index]\nprint(\"Predicted emotion:\", emotion_prediction)\n","metadata":{"_uuid":"cd0e04ae-c214-4573-ad5d-f3a830c0cd87","_cell_guid":"ff5fa70a-f505-4464-ad7e-8dcf008f26fb","trusted":true,"collapsed":false,"jupyter":{"outputs_hidden":false}},"outputs":[],"execution_count":null}]}