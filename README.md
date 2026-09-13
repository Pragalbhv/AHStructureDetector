# Alkali Halide Structure Detector
**Author:** Hayden O. Scheiber

`AHStructureDetector` is a python library that gives straightforward access to the 2022 binary salt structure classifiers intended for use in analyzing phases in molecular dynamics trajectories of alkali halide salt systems. The structure classifiers are constructed from feedforward convolutional neural networks, where 1D convolution is performed in time to filter out short-lived structural fluctuations. This increases accuracy in the face of thermal noise, allowing the classifiers to perform well even at high temperatures. The details of the alkali halide structure detector are fully described in [J. Chem. Phys. **157**, 204108 (2022)](https://aip.scitation.org/doi/10.1063/5.0122274). The two functions available in this library were used to generate the main analyses in that project. Note that the trained neural networks used for classification are available [within a subdirectory of this repository](./AHStructureDetector/ML_Models), saved in TensorFlow `SavedModel` format. These can be directly imported into your local installation of Tensorflow 2.

## Installation

Dependencies:
 - [tensorflow](https://www.tensorflow.org/) (2.4 or later)
 - [MDAnalysis](https://www.mdanalysis.org/)
 - [freud](https://freud.readthedocs.io/)
 - [numpy](https://numpy.org/)
 - [seaborn](https://seaborn.pydata.org/)
 - [matplotlib](https://matplotlib.org/)
 - [scipy](https://scipy.org/)

To install, I suggest first setting up a virtual environment with **python 3.8**. 
Download the repository and install dependencies, then from within the repository use `pip install ./dist/AHStructureDetector-1.0.0-py3-none-any.whl`

## Using the `AHStructureDetector` Library
This library contains two functions: `AHStructureDetector.Check_Structures` and `AHStructureDetector.Calculate_Liquid_Fraction`. Both work very similarly and neither have required inputs, but many optional inputs. `Check_Structures` is the main analysis tool while `Calculate_Liquid_Fraction` is intended for use when a global solid/liquid order parameter is required.

`AHStructureDetector` supports [GROMACS](https://www.gromacs.org/) trajectories and extended XYZ (`*.extxyz`) trajectories. GROMACS analysis requires both a trajectory file (`*.trr`) and geometry input file (`*.gro` or `*.g96`) in `WorkDir`, named identically (`SystemName`) besides the extension. For extxyz, the single `SystemName.extxyz` file contains the trajectory and cell information; use `FileType='extxyz'`. Frame `Time` or `time` metadata is interpreted in ps, and otherwise frames are spaced by 1 ps.

The simplest way to use a function is to is to move to the directory containing your GROMACS trajectory file and  geometry. Then in python  use
```python
import AHStructureDetector as ahsd
ahsd.Check_Structures(WorkDir='/path/to/working/directory')
```
The default behaviour is to find the `*.trr` file in the `WorkDir` (by default, the current directory) and apply the `0-0a` structure classifier to the trajectory in `1 ps` time steps (as dictated by the `TimePerFrame` input). By default, two new files will be produced: an classification overview plot (toggle on/off with `SavePredictionsImage`) and a classified trajectory output in `*.xyz` format (toggle on/off with `SaveTrajectory`). Other neural network structure classifiers can be accessed by modifying the following four options: `ML_TimeLength`, `ML_TimeStep`,  `Voronoi`,  and `Qlm_Average`. The following combinations are available:

| `ML_TimeLength` (ps) | `ML_TimeStep` (ps) | `Voronoi` | `Qlm_Average` | Classifier Name | Accuracy (%) |
|--|--|--|--|--|--|
|0|0|False|False|0-0|91.61|
|2|1|False|False|2-1|98.37|
|4|1|False|False|4-1|99.41|
|10|1|False|False|10-1|99.90|
|10|5|False|False|10-5|98.35|
|20|5|False|False|20-5|99.33|
|50|5|False|False|50-5|99.90|
|0|0|False|**True**|0-0a|99.58|
|2|1|False|**True**|2-1a|99.94|
|4|1|False|**True**|4-1a|99.97|
|10|1|False|**True**|10-1a|99.99|
|10|5|False|**True**|10-5a|98.95|
|20|5|False|**True**|20-5a|99.97|
|50|5|False|**True**|50-5a|99.99|
|0|0|**True**|False|0-0v|92.50|
|2|1|**True**|False|2-1v|98.49|
|4|1|**True**|False|4-1v|99.23|
|10|1|**True**|False|10-1v|99.74|
|10|5|**True**|False|10-5v|98.42|
|20|5|**True**|False|20-5v|99.25|
|50|5|**True**|False|50-5v|99.82|

The accuracy column refers to average accuracy when each classifier was tested on 9 million data points from a set of bulk systems of known structure that were not used in the training process. In general, I suggest using the default `Qlm_Average=True` unless you have a good reason not to. These classifiers have significantly higher accuracy with little additional computational cost. The main trade-off in using `Qlm_Average=True` is that very small structures may be missed due to spatial averaging. Modifying `ML_TimeLength` and `ML_TimeStep` from the default (`0` and `0`) turns on *time convolution* which increases accuracy by averaging out instantaneous thermal fluctuations. Use of this feature requires that trajectory time steps are saved in `ML_TimeStep` increments and the trajectory for analysis must be at least `ML_TimeLength` ps in length.

See the documentation available with each individual function for more details.

## Unit Tests
Included in this package are unit tests for each classifier to ensure the package is working properly.
Tests can be performed with `pytest` from the main `AHStructureDetector` directory using

    python -m pytest

Questions? Feel free to contact the author: scheiber@chem.ubc.ca
