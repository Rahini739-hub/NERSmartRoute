from flask import Flask, render_template, request, jsonify
from risk_model import predict_risk

app = Flask(__name__)


# ---------------------------------------
# ROUTE DATA
# ---------------------------------------

ROUTES = {
    ("guwahati", "aizawl"): {
        "route": "Guwahati -> Silchar -> Aizawl",
        "alternative": "Guwahati -> Shillong -> Aizawl",
        "distance": 520,
        "time": 18.5,
        "cost_per_kg": 85,
        "accessibility": 82
    },

    ("guwahati", "shillong"): {
        "route": "Guwahati -> Nongpoh -> Shillong",
        "alternative": "Guwahati -> Byrnihat -> Shillong",
        "distance": 100,
        "time": 3.5,
        "cost_per_kg": 35,
        "accessibility": 91
    },

    ("guwahati", "imphal"): {
        "route": "Guwahati -> Nagaon -> Dimapur -> Imphal",
        "alternative": "Guwahati -> Shillong -> Imphal",
        "distance": 470,
        "time": 15.0,
        "cost_per_kg": 78,
        "accessibility": 76
    },

    ("guwahati", "agartala"): {
        "route": "Guwahati -> Shillong -> Silchar -> Agartala",
        "alternative": "Guwahati -> Hojai -> Silchar -> Agartala",
        "distance": 550,
        "time": 17.0,
        "cost_per_kg": 72,
        "accessibility": 80
    }
}


# ---------------------------------------
# ACCESSIBILITY
# ---------------------------------------

def calculate_accessibility(route):

    road = route["accessibility"]
    terrain = max(50, road - 8)
    connectivity = min(98, road + 5)
    disruption = max(40, road - 12)

    overall = round(
        (road + terrain + connectivity + disruption) / 4
    )

    return {
        "road": road,
        "terrain": terrain,
        "connectivity": connectivity,
        "disruption": disruption,
        "overall": overall
    }


# ---------------------------------------
# HOME
# ---------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------
# ANALYZE
# ---------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request data"
        }), 400

    source = data.get("source", "").strip()
    destination = data.get("destination", "").strip()
    cargo = data.get("cargo", "").strip()
    priority = data.get("priority", "Normal").strip()

    try:
        weight = float(data.get("weight", 0))
    except (TypeError, ValueError):
        weight = 0


    # ---------------------------------------
    # FIND ROUTE
    # ---------------------------------------

    key = (
        source.lower(),
        destination.lower()
    )

    route = ROUTES.get(key)


    # ---------------------------------------
    # UNKNOWN ROUTE
    # ---------------------------------------

    if route is None:

        accessibility = 70

        if priority.lower() == "emergency":
            accessibility = 76

        estimated_cost = weight * 75

        if priority.lower() == "emergency":
            estimated_cost *= 1.10

        elif priority.lower() == "high":
            estimated_cost *= 1.05

        return jsonify({

            "source": source,
            "destination": destination,
            "cargo": cargo,
            "weight": weight,
            "priority": priority,

            "route":
                source + " -> " + destination,

            "alternative":
                "Alternative route requires further analysis",

            "distance": "Estimated",
            "time": "Estimated",

            "cost":
                round(estimated_cost, 2),

            "accessibility":
                accessibility,

            "accessibility_details": {
                "road": accessibility,
                "terrain": max(50, accessibility - 8),
                "connectivity": min(98, accessibility + 5),
                "disruption": max(40, accessibility - 12),
                "overall": accessibility
            },

            "risk": "Medium",

            "risk_score": 60,

            "message":
                "Route analyzed using prototype intelligence."
        })


    # ---------------------------------------
    # ACCESSIBILITY
    # ---------------------------------------

    accessibility_data = calculate_accessibility(route)


    # ---------------------------------------
    # COST
    # ---------------------------------------

    estimated_cost = (
        weight * route["cost_per_kg"]
    )

    if priority.lower() == "emergency":
        estimated_cost *= 1.10

    elif priority.lower() == "high":
        estimated_cost *= 1.05


    # ---------------------------------------
    # ML INPUT
    # ---------------------------------------

    terrain = max(
        50,
        route["accessibility"] - 8
    )


    # ---------------------------------------
    # ML PREDICTION
    # ---------------------------------------

    ml_risk, risk_score = predict_risk(
        route["distance"],
        weight,
        route["accessibility"],
        terrain
    )


    # ---------------------------------------
    # FORCE NORMAL PYTHON TYPES
    # ---------------------------------------

    risk_score = int(risk_score)


    # ---------------------------------------
    # DEBUG
    # ---------------------------------------

    print("ML RISK:", ml_risk)
    print("ML CONFIDENCE:", risk_score)


    # ---------------------------------------
    # RESPONSE
    # ---------------------------------------

    return jsonify({

        "source": source,

        "destination": destination,

        "cargo": cargo,

        "weight": weight,

        "priority": priority,

        "route":
            route["route"],

        "alternative":
            route["alternative"],

        "distance":
            route["distance"],

        "time":
            route["time"],

        "cost":
            round(estimated_cost, 2),

        "accessibility":
            accessibility_data["overall"],

        "accessibility_details":
            accessibility_data,

        "risk":
            ml_risk,

        "risk_score":
            risk_score,

        "message":
            "AI route intelligence analysis completed."
    })


# ---------------------------------------
# START SERVER
# ---------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )