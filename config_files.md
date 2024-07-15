### Model configuration documentation

The model configuration is a `.json` file that's parsed by the IOT-ensemble-trainer to determine the base models used in bagging and stacking ensemble methods. Essentially it's a list of models where each model has the following properties:
- `type: str` - the base model type (must match the scikit learn naming convention, case-sensitive).
- `params: dict` - the parameters and their respective values (parameter names must match the scikit learn naming convention).

Example of a model configuration:

```
[
    {
        "type": "LogisticRegression",
        "params": {
            "tol": 0.0001,
            "C": 1.0,
            "max_iter": 50,
        },
    },
    {
        "type": "RandomForestClassifier",
        "params": {
            "criterion": "gini"
        }
    },
    {
        "type": "SVC",
            "params": {
                "tol": 0.0001,
                "C": 1.5,
                "max_iter": 100
            }
    }
]
```

This configuration will use Logistic Regression, Random Forest Classifier and a Support Vector Classifier as its base model.

- LogisticRegression
- SVC
- RandomForestClassifier
- DecisionTreeClassifier
- KNeighborsClassifier
- GaussianNB
- GaussianProcessClassifier
- Keras Sequential (see Using MLPs as base model)

### Using MLPs as base model
In order to use a keras trained MLP as a base model, you will need to use `"MLP"` as the type. The IOT-trainer will add an initial Dense layer deduced from the input data to assist the user with the model architecture, however, beyond that first layer it is up to the user to write appropriate configuration files that match the dataset uploaded by the user.

The parameters for the MLP consist of the key being the layer the user wishes to add to the model architecture, and the value being a list containing the number of neurons and an activation function. The user can also specify a pure activation layer by setting the key to `"activation"` and then specifying the type of activation function. Currently, only Dense layers and all the activation functions are supported. 

<i>As the data intended for the IOT-Ensemble-Trainer is a 1D array there adding support for a CNN layer would be redundant as a CNN layer on a 1D array would be the same as a linear dense layer. Furthermore, as the data has no order/time relevance, adding a LSTM or RNN layer would be incorrect and train on non-existent logic/relations between rows in the dataset.</i>

Example of an MLP base model consisting of a dense linear layer with 8 neurons and a softmax activation layer.

```
[
    {
        "type": "LogisticRegression",
        "params": {
            "tol": 0.0001,
            "C": 1.0,
            "max_iter": 50
        }
    },
    {
        "type": "LogisticRegression",
        "params": {
            "tol": 0.0001,
            "C": 5.0,
            "max_iter": 50
        }
    },
    {
        "type": "MLP",
        "params": {
            "dense": [8, "linear"],
            "activation": "softmax"
        }
    }
]
```
### Bounds/Verification 
The Bounds/Verification file is a `.csv` file of 2 rows, the top row defines the variable used by the Z3 solver to validate the Neural Network and the bottom row defines the values for each variable. The following columns are required in the Bounds/Verification file:

- `greater_than: float` - number that the feature value has to be greater than.
- `feature: str` - string matching the feature name.
- `less_than: float` - number that the feature value has to be less than.
- `truth_category: str` - the category expected as classification output for all inputs within these bounds (less than and greater than for the feature given).
- `false_category_1/2/3: str` - 3 separate fields, each specifying a category expected to **not** be predicated over the truth category.

Example of a bounds file:
```
"greater_than","feature","less_than","truth_category","false_category_1","false_category_2","false_category_3"
"2.1","Header_Length","90.1","DoS-SYN_Flood","DDoS-PSHACK_Flood","BenignTraffic","MITM-ArpSpoofing"
```