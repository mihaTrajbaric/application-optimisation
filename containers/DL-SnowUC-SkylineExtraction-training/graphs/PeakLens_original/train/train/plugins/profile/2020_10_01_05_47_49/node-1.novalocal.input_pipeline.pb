	�i����w@�i����w@!�i����w@	�~D���?�~D���?!�~D���?"e
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails$�i����w@�{b�*_�?A!����w@YH�`�ڥ?*	B`��"�@2Y
"Iterator::Model::Prefetch::BatchV2
��ϛJ�?!�?A��X@)������?1\f�rVPW@:Preprocessing2c
+Iterator::Model::Prefetch::BatchV2::Shuffle��o��?!v�t�E@)�o��?1v�t�E@:Preprocessing2F
Iterator::Model?s֧��?!R{����?)��k��?1֏砉��?:Preprocessing2P
Iterator::Model::PrefetchH�Sȕzv?!�<���?)H�Sȕzv?1�<���?:Preprocessing:�
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
�Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
�Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
�Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
�Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)�
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis�
device�Your program is NOT input-bound because only 0.0% of the total step time sampled is waiting for input. Therefore, you should focus on reducing other time.no*no#You may skip the rest of this page.B�
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown�
	�{b�*_�?�{b�*_�?!�{b�*_�?      ��!       "      ��!       *      ��!       2	!����w@!����w@!!����w@:      ��!       B      ��!       J	H�`�ڥ?H�`�ڥ?!H�`�ڥ?R      ��!       Z	H�`�ڥ?H�`�ڥ?!H�`�ڥ?JCPU_ONLY