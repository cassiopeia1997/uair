'''
preparation of data
'''
from sklearn import datasets  
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
import matplotlib.pyplot as plt
from pybrain.utilities import percentError
from pybrain.structure import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer

iris_ds = datasets.load_iris()
X, y = iris_ds.data, iris_ds.target
label = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
#print X
#print y

# 4 input attributes, 1 output with 3 class labels
ds = ClassificationDataSet(4, 1, nb_classes=3, class_labels=label)  
for i in range(len(y)): 
    ds.appendLinked(X[i], y[i])
ds.calculateStatistics()

# split training, testing, validation data set (proportion 4:1)
tstdata_temp, trndata_temp = ds.splitWithProportion(0.25)  
tstdata = ClassificationDataSet(4, 1, nb_classes=3, class_labels=label)
for n in range(0, tstdata_temp.getLength()):
    tstdata.appendLinked( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )
#print tstdata
trndata = ClassificationDataSet(4, 1, nb_classes=3, class_labels=label)
for n in range(0, trndata_temp.getLength()):
    trndata.appendLinked( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

# one hot encoding
trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()


# 4 input nodes, 3 output node each represent one class
# here we set 5 hidden layer nodes.
# SoftmaxLayer(0/1) for multi-label output activation function
n_h = 5
net = buildNetwork(4, n_h, 3, outclass = SoftmaxLayer)  
# standard(incremental) BP algorithm: 
for i in range(200):
	trainer = BackpropTrainer(net, trndata)
	tstresult = percentError( trainer.testOnClassData(), tstdata['target'] )
	print("epoch: %4d" % (i+1), " test error: %5.2f%%" % tstresult)
trainer.trainEpochs(1)
# accumulative BP algorithm: 
'''
trainer = BackpropTrainer(net, trndata, batchlearning=True)
err_train, err_valid = trainer.trainUntilConvergence(maxEpochs=200)
'''
#test of model
for ipr,target in tstdata:
	#print target
	result=net.activate(ipr)
	#print result
	#print result.max()
# convergence curve 
#classificationPerformance(net, tstdata)
#plt.plot(err_train,'b',err_valid,'r')
#plt.show()

# model testing

tstresult = percentError( trainer.testOnClassData(), tstdata['target'] )
print("epoch: %4d" % trainer.totalepochs, " test error: %5.2f%%" % tstresult)   