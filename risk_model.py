import pandas as pd
from sklearn.ensemble import RandomForestClassifier


# ---------------------------------------
# SAMPLE LOGISTICS TRAINING DATA
# ---------------------------------------

data = {

    "distance": [
        100, 150, 200, 300, 400,
        450, 500, 550, 600, 250,
        350, 480, 520, 180, 420
    ],

    "weight": [
        100, 300, 500, 800, 1000,
        1200, 1500, 2000, 2500, 600,
        900, 750, 200, 150, 1100
    ],

    "accessibility": [
        92, 88, 85, 72, 68,
        65, 60, 58, 55, 80,
        70, 69, 82, 94, 66
    ],

    "terrain": [
        90, 85, 82, 70, 65,
        60, 55, 50, 48, 78,
        68, 67, 80, 92, 62
    ],

    "risk": [
        "Low", "Low", "Medium", "Medium", "High",
        "High", "High", "High", "High", "Medium",
        "High", "Medium", "Low", "Low", "High"
    ]
}


# ---------------------------------------
# CREATE DATAFRAME
# ---------------------------------------

df = pd.DataFrame(data)


# ---------------------------------------
# FEATURES
# ---------------------------------------

X = df[
    [
        "distance",
        "weight",
        "accessibility",
        "terrain"
    ]
]


# ---------------------------------------
# TARGET
# ---------------------------------------

y = df["risk"]


# ---------------------------------------
# TRAIN RANDOM FOREST MODEL
# ---------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# ---------------------------------------
# PREDICT RISK
# ---------------------------------------

def predict_risk(
    distance,
    weight,
    accessibility,
    terrain
):

    input_data = [[
        distance,
        weight,
        accessibility,
        terrain
    ]]


    # Prediction
    prediction = model.predict(input_data)

    risk = prediction[0]


    # Probability
    probabilities = model.predict_proba(
        input_data
    )[0]


    # Model classes
    classes = model.classes_


    # Match class with probability
    probability_map = dict(
        zip(classes, probabilities)
    )


    # Confidence of predicted class
    confidence = probability_map.get(
        risk,
        0
    )


    # Convert to normal Python integer
    risk_score = int(
        round(float(confidence) * 100)
    )


    return risk, risk_score


# ---------------------------------------
# TEST MODEL
# ---------------------------------------

if __name__ == "__main__":

    risk, score = predict_risk(
        520,
        200,
        82,
        74
    )

    print("Predicted Risk:", risk)

    print(
        "ML Prediction Confidence:",
        score,
        "/100"
    )