# coding: UTF-8

import string
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

#读入并展示数据
f = open('./poems_clean.txt', 'r', encoding='utf-8')
poems = []
for line in f.readlines():
    title, athour, poem = line.split('::')
    poem = poem.replace(' ', '')
    poem = poem.replace('，', '')
    poem = poem.replace('。', '')
    poem = poem.replace('\n', '')
    poems.append(list(poem))
print (poems[0])
print('\n')
'''
['凄', '凄', '恻', '恻', '又', '微', '嚬', '欲', '话', '羇', '愁', '忆', '故', '人', '薄', '酒', '旋', '醒', '寒', 
'彻', '夜', '好', '花', '虚', '谢', '雨', '藏', '春', '萍', '蓬', '已', '恨', '为', '逋', '客', '江', '岭', '那', 
'知', '见', '侍', '臣', '未', '必', '交', '情', '系', '贫', '富', '柴', '门', '自', '古', '少', '车', '尘']
'''


#从字符到正整数的映射：Tokenizer编码，最终的文本数据包含3846个不同的汉字,由于技术原因，再加一个1
tokenizer = Tokenizer()
tokenizer.fit_on_texts(poems)
poems_digit = tokenizer.texts_to_sequences(poems)
vocab_size = len(tokenizer.word_index) + 1
print (vocab_size)
'''
3847
'''


#处理数据的“长短不一”：补零操作
print ('原始诗歌')
print(poems[20])
print(poems_digit[20])
print('\n')

poems_digit = pad_sequences(poems_digit, maxlen=70, padding='post')
print('编码+补全后的结果')
print(poems_digit[20])
'''
原始诗歌
['鬓', '惹', '新', '霜', '耳', '旧', '聋', '眼', '昏', '腰', '曲', '四', '肢', '风', '交', '亲', 
'若', '要', '知', '形', '候', '岚', '嶂', '烟', '中', '折', '臂', '翁']
[439, 1370, 67, 202, 948, 137, 2594, 279, 467, 842, 317, 323, 2102, 6, 507, 406, 254, 691, 26, 1044, 1116, 1710, 1188, 99, 17, 557, 1611, 714]


编码+补全后的结果
[ 439 1370   67  202  948  137 2594  279  467  842  317  323 2102    6
  507  406  254  691   26 1044 1116 1710 1188   99   17  557 1611  714
    0    0    0    0    0    0    0    0    0    0    0    0    0    0
    0    0    0    0    0    0    0    0    0    0    0    0    0    0
    0    0    0    0    0    0    0    0    0    0    0    0    0    0]
'''


#提取因变量和自变量：把poems_digit矩阵拆分为X和Y，
X = poems_digit[:,  :-1]
Y = poems_digit[:, 1: ]

print (poems_digit.shape)
print (X.shape)
print (Y.shape)

'''
(2550, 70)
(2550, 69)
(2550, 69)
'''
print ('X示例', '\t', 'Y示例')
for i in range(10):
    print (X[0][i], '\t', Y[0][i])
print ('...', '\t', '...')
'''
X示例      Y示例
480      480
480      1931
1931     1931
1931     298
298      206
206      2582
2582     114
114      892
892      2091
2091     95
...      ...
'''


#将因变量Y变成one-hot向量的形式。
from keras.utils import to_categorical
Y = to_categorical(Y, num_classes=vocab_size)
print (Y.shape)
'''
(2550, 69, 3847)
'''


#LSTM模型的构建
from keras.layers import Input, LSTM, Dense, Embedding, Activation, BatchNormalization
from keras import Model

hidden_size1 = 128
hidden_size2 = 64

inp = Input(shape=(69,))

x = Embedding(vocab_size, hidden_size1, input_length=69, mask_zero=True)(inp)
x = LSTM(hidden_size2, return_sequences=True)(x)

x = Dense(vocab_size)(x)
pred = Activation('softmax')(x)

model = Model(inp, pred)
model.summary()
'''
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         (None, 69)                0         
_________________________________________________________________
embedding_1 (Embedding)      (None, 69, 128)           492416    
_________________________________________________________________
lstm_1 (LSTM)                (None, 69, 64)            49408     
_________________________________________________________________
dense_1 (Dense)              (None, 69, 3847)          250055    
_________________________________________________________________
activation_1 (Activation)    (None, 69, 3847)          0         
=================================================================
Total params: 791,879
Trainable params: 791,879
Non-trainable params: 0
_________________________________________________________________
'''


#LSTM模型编译与拟合
from keras.optimizers import Adam

model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.01), metrics=['accuracy'])
# model.fit(X, Y, epochs=10, batch_size=16, validation_split=0.2)
'''
Epoch 1/10 2040/2040 [==============================] - 66s 33ms/step - loss: 7.0967 - acc: 0.0235 - val_loss: 7.0020 - val_acc: 0.0291
Epoch 2/10 2040/2040 [==============================] - 99s 49ms/step - loss: 6.8796 - acc: 0.0263 - val_loss: 6.8978 - val_acc: 0.0317
Epoch 3/10 2040/2040 [==============================] - 76s 37ms/step - loss: 6.6745 - acc: 0.0363 - val_loss: 6.7848 - val_acc: 0.0439
Epoch 4/10 2040/2040 [==============================] - 63s 31ms/step - loss: 6.4093 - acc: 0.0538 - val_loss: 6.7339 - val_acc: 0.0540
......
Epoch 10/10 2040/2040 [==============================] - 69s 34ms/step - loss: 5.1414 - acc: 0.1266 - val_loss: 7.0999 - val_acc: 0.0643
'''

#模型预测
sample_text = ['床','前','明']
print (sample_text)
sample_text = tokenizer.texts_to_sequences(sample_text)
print (sample_text)
sample_text = pad_sequences(sample_text, maxlen=69, padding='post')
word_prob = model.predict(sample_text)[0,2]
print (word_prob)
tmp=tokenizer.word_index
dic_new = dict([val, key] for key, val in tmp.items())
print('tmp',dic_new)
print (dic_new[word_prob.argmax()+1], word_prob.max())
'''
['床', '前', '明']
[[540], [80], [52]]
[3.4639926e-03 1.1927439e-02 5.2260247e-04 ... 5.0051693e-08 4.7071349e-08
 5.2237368e-08]
 tmp {1: '不', 2: '人', 3: '山',... , 3845: '埼', 3846: '脾'}
有 0.04201949
'''


#LSTM模型做藏头诗
poem_incomplete = '山****清****最****佳****'
poem_index = []
poem_text = ''
for i in range(len(poem_incomplete)):
    current_wrod = poem_incomplete[i]
    if current_wrod != '*':
        index = tokenizer.word_index[current_wrod]
    else:
        x = np.expand_dims(poem_index, axis=0)
        x = pad_sequences(x, maxlen=69, padding='post')
        y = model.predict(x)[0, i]
        y[0] = 0 #去掉停止词
        index = y.argmax()
        current_wrod = dic_new[index]

    poem_index.append(index)
    poem_text = poem_text + current_wrod

poem_text = poem_text[0:]
print (poem_text[0:5])
print (poem_text[5:10])
print (poem_text[10:15])
print (poem_text[15:20])
'''
山中有客心
清净色满城
水上云山中
秀色入云中
'''