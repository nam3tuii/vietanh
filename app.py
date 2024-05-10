import warnings #thư viện để tắt các thông báo không cần thiết.
warnings.filterwarnings('ignore')
from tensorflow import keras
from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
IMAGE_SIZE=[224, 224] #kích thước ảnh đầu vào cho mô hình
train_path='Datasets/train'#đường dẫn đến thư mục chứa dữ liệu huấn luyện
valid_path='Datasets/test' #đường dẫn đến thư mục chứa dữ liệu kiểm tra
vgg=VGG16(input_shape=IMAGE_SIZE+[3],weights='imagenet',include_top=False)
for layer in vgg.layers:#Đóng băng các layer trong mô hình VGG16 để không được huấn luyện lại.
    layer.trainable=False
folders=glob('Datasets/train/*')#Tìm kiếm các thư mục con trong thư mục huấn luyện.
x=Flatten()(vgg.output)
prediction=Dense(len(folders),activation='softmax')(x)
model =Model(inputs=vgg.input,outputs=prediction)#Tạo mô hình từ đầu vào của VGG16 và đầu ra của lớp Dense.
model.summary()#Hiển thị thông tin của mô hình
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])#thiết lập thông số huấn luyện
from keras.src.legacy.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale = 1./255,shear_range = 0.2,zoom_range = 0.2,horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)
training_set = train_datagen.flow_from_directory('Datasets/train',target_size =(224, 224),batch_size = 10,class_mode = 'categorical')
test_set = test_datagen.flow_from_directory('Datasets/test',target_size = (224, 224),batch_size = 10,class_mode = 'categorical')
model.fit(training_set,validation_data=test_set,epochs=1,steps_per_epoch=len(training_set),validation_steps=len(test_set)
)
import tensorflow as tf
from keras.models import load_model
model.save('xray.h5')#Lưu mô hình đã huấn luyện vào một tệp tin có tên là 'xray.h5'. 
#Mô hình có thể được sử dụng sau này để dự đoán bệnh viêm phổi từ ảnh X-quang mới.
