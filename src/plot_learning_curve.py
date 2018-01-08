"""
Plot learning curve for trained caffe model
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt

CWD = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
MODEL_DIR = os.path.join(CWD, 'model')


train_log = pd.read_csv(os.path.join(MODEL_DIR, "train_model.log.train"), delimiter=',')
print(train_log)
test_log = pd.read_csv(os.path.join(MODEL_DIR, "train_model.log.test"), delimiter=',')
print(test_log)

'''
Making learning curve
'''
fig, ax1 = plt.subplots(figsize=(10.5, 6))

#Plotting training and test losses
train_loss, = ax1.plot(train_log['NumIters'], train_log['loss'], color='red',  alpha=.5)
test_loss, = ax1.plot(test_log['NumIters'], test_log['loss'], linewidth=2, color='green')
ax1.set_ylim(ymin=0, ymax=1)
ax1.set_xlabel('Iterations', fontsize=15)
ax1.set_ylabel('Loss', fontsize=15)
ax1.tick_params(labelsize=15)
#Plotting test accuracy
ax2 = ax1.twinx()
test_accuracy, = ax2.plot(test_log['NumIters'], test_log['accuracy'], linewidth=2, color='blue')
ax2.set_ylim(ymin=0, ymax=1)
ax2.set_ylabel('Accuracy', fontsize=15)
ax2.tick_params(labelsize=15)
#Adding legend
plt.legend([train_loss, test_loss, test_accuracy], ['Training Loss', 'Test Loss', 'Test Accuracy'],  bbox_to_anchor=(1, 0.8))
plt.title('Training Curve', fontsize=18)
#Saving learning curve
# plt.show()
plt.savefig(os.path.join(MODEL_DIR, 'learning_curve.png'))