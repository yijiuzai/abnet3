# ABnet3

Representation learning package using side information, system for subword modeling for [Zeroresource challenge](http://sapience.dec.ens.fr/bootphon/2017/index.html).

### Overview

<!-- **Sense of Place** is a feeling or perception held by people about a location: some characteristics of a place can
be perceived at first sight, such as wealth or safety. Lately, there has been recent interest in predicting these
human judgments with computer vision techniques [Ordonez and Berg 2014].

The **CNN architecture with the NetVLAD** layer from [Arandjelović et al. 2016] significantly outperforms
non-learnt image representations as well as off-the-shelf CNN descriptors, and improves over the state-of-the-
art on challenging image retrieval benchmarks. The goal of this project is to transfer the CNN representation
learnt for Visual Place Recognition to predict human judgments of safety and wealth of locations. -->

Build Representation for speech frames based on side information. Composed of different modules :

* `model.py`
* `loss.py`
* `sampler.py`
* `trainer.py`
* `embedder.py`
* `utils.py`
* `features.py`

### Installation of the package

To install the ABnet3 package, you can use Anaconda, and either create a conda environment:

    conda create --name abnet3 python=3.6 --file requirements.txt

or use a conda environment you already have with python 3 :

    conda install --file requirements.txt

requirement.txt do not install pytorch. You need to install this package using conda. For now, the latest compatible version is pytorch 0.2:
To install without gpu support
    conda install -c soumith pytorch=0.2

To install with GPU support (replace cuda75 with your version of cuda)
    conda install  pytorch=0.2 cuda75 -c pytorch


Once all the necessary packages are installed, simply launch:

    python setup.py build && python setup.py install

If you want to work on ABnet3 and develop your own modules, instead of:

    python setup.py install

you can launch:

    python setup.py develop

### Tensorboard vizualisation

The package will save train / dev loss during training. To vizualise them :

- Install tensorboard (`conda install tensorboard`)

- run `tensorboard --logdir path/to/logdir`.
The default logdir is `./run` in the current directory.

### Documentation

### Tests

The package comes with a unit-tests suit. To run it, first install *pytest* on your Python environment:

    pip install pytest
    pytest test
#### References

    .. [1] Thiolliere, R., Dunbar, E., Synnaeve, G., Versteegh, M., & Dupoux, E.
           *A hybrid dynamic time warping-deep neural network architecture for unsupervised acoustic modeling.*
           In Sixteenth Annual Conference of the International Speech Communication Association

    .. [2] Zeghidour, N., Synnaeve, G., Usunier, N. & Dupoux, E.
           *Joint Learning of Speaker and Phonetic Similarities with Siamese Networks.*
           In: INTERSPEECH-2016, (pp 1295-1299)



### Acknowledgments
A part of the code is inspired from the previous version in Theano of  [ABnet](https://github.com/bootphon/abnet2), and the [examples in Pytorch](https://github.com/pytorch/examples)
