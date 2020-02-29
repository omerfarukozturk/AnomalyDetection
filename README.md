# Anomaly Detection: Nelson Rules for Control Chart
## Python implementation

"Nelson rules are a method in process control of determining if some measured variable is out of control (unpredictable versus consistent). Rules, for detecting "out-of-control" or non-random conditions were first postulated by Walter A. Shewhart [1] in the 1920s. The Nelson rules were first published in the October 1984 issue of the Journal of Quality Technology in an article by Lloyd S Nelson.

The rules are applied to a control chart on which the magnitude of some variable is plotted against time. The rules are based on the mean value and the standard deviation of the samples."

https://en.wikipedia.org/wiki/Nelson_rules

The script (AnomalyDetection.py) checks anomaly in daily credit card expenditure dataset according to average weekly expenses. This script uses the first 52 weeks in the training (for calculating 𝑥̅ and 𝜎), so rest for testing.

Generates a table as csv file that is as follows:
The code fills the cells by 1, if there is an anomaly for the respected week and rule; otherwise, the value of the cell is 0.
