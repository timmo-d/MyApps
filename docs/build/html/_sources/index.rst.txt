.. My Algo Trader documentation master file, created by
   sphinx-quickstart on Thu Jun  4 11:18:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to My Algo Trader's documentation!
==========================================
Introductory paragraph for app.

Overview on How to Run this API
*******************************
1. Either install a Python IDE or create a Python virtual environment to install the packages required
2. Install packages required
3. Install MySQL 8.x

Setup procedure
***************
1. Configure project environment (Either A. Install Pycharm OR B. Create a Virtual Environment)
    A. Install Pycharm (www.jetbrains.com/pycharm/download/)
    B. Create a Python Virtual Environment
        - Install virtualenv::

            sudo pip install virtualenv

        - Create virtialenv::

            virtualenv -p python3 <name of virtualenv>

        - Install requirements::

            pip install -r requirements.txt

Documentation for the Code
==========================
.. toctree::
   :maxdepth: 3
   :caption: Contents:

Run main
********
.. automodule:: src.app
   :members:

Data gathering and munging
**************************
.. automodule:: datamgt.src.control
   :members:

Downloading data
----------------
.. automodule:: datamgt.src.download
   :members: constructYFURL, download, add_column_in_csv, getPrices, getIndicies

Loading into database
---------------------
.. automodule:: datamgt.src.stage
   :members: stageSymbols, stageSymbolChanges, stagePrices, stageIndicies

Run ML models
*************
.. automodule:: analysis.src.testStrategy
   :members:

Construct feature functions
---------------------------
.. automodule:: analysis.src.featureFunctions
   :members: getCalFeatures, getHistory, getMomentum, getValue, getJump, getPrevWeeks, daysToWeeks, weektype

Construct features
------------------
.. automodule:: analysis.src.features
   :members: getTrainData, getFeatures, getReturn

Fetch data from database
------------------------
.. automodule:: analysis.src.fetchData
   :members: getRawData

Construct labels
----------------
.. automodule:: analysis.src.labelFunctions
   :members: labels3, labelId

Central import file
-------------------
.. automodule:: analysis.src.setup
   :members:

Test and Train
--------------
.. automodule:: analysis.src.testAndTrain
   :members: getPredictionsProb, getPredictions, backtestResults, getAssetReturns, getPredictionsNN

Test functions
--------------
.. automodule:: analysis.src.testFunctions
   :members:

Tune XGB parameters
-------------------
.. automodule:: analysis.src.TuningXGB
   :members: score



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
