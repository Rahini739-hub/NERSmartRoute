async function analyzeRoute() {

    const source = document.getElementById("source").value.trim();
    const destination = document.getElementById("destination").value.trim();
    const cargo = document.getElementById("cargo").value.trim();
    const weight = document.getElementById("weight").value;
    const priority = document.getElementById("priority").value;

    const result = document.getElementById("result");

    // INPUT VALIDATION
    if (!source || !destination || !cargo || !weight) {

        result.innerHTML = `
            <div class="empty-result">

                <h3>Please fill all details</h3>

                <p>
                    Enter source, destination, cargo and weight.
                </p>

            </div>
        `;

        return;
    }


    // LOADING
    result.innerHTML = `
        <div class="empty-result">

            <div class="radar">

                <div class="radar-ring ring1"></div>

                <div class="radar-ring ring2"></div>

                <div class="radar-dot"></div>

            </div>

            <h3>
                Analyzing Route...
            </h3>

            <p>
                Processing route accessibility,
                risk and logistics data.
            </p>

        </div>
    `;


    try {

        // SEND DATA TO FLASK
        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                source: source,

                destination: destination,

                cargo: cargo,

                weight: weight,

                priority: priority

            })

        });


        // SERVER RESPONSE
        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Route analysis failed"
            );

        }


        // ACCESSIBILITY DETAILS
        const details =
            data.accessibility_details || {

                road: data.accessibility,

                terrain:
                    Math.max(
                        50,
                        data.accessibility - 8
                    ),

                connectivity:
                    Math.min(
                        98,
                        data.accessibility + 5
                    ),

                disruption:
                    Math.max(
                        40,
                        data.accessibility - 12
                    ),

                overall:
                    data.accessibility

            };


        // ML CONFIDENCE
        const riskScore =
            data.risk_score !== undefined
                ? data.risk_score
                : 0;


        // EMERGENCY MODE
        const emergencyMode =
            data.priority &&
            data.priority.toLowerCase() === "emergency";


        // RESULT
        result.innerHTML = `

            <div class="analysis-result">


                <!-- RECOMMENDED ROUTE -->

                <div class="result-main">

                    <h3>
                        Recommended Route
                    </h3>

                    <p class="route-name">
                        ${data.route}
                    </p>

                </div>


                <!-- EMERGENCY MODE -->

                ${emergencyMode ? `

                    <div class="emergency-box">

                        <strong>
                            EMERGENCY PRIORITY ACTIVE
                        </strong>

                        <p>
                            Route optimized for urgent
                            shipment delivery.
                        </p>

                    </div>

                ` : ""}


                <!-- MAIN METRICS -->

                <div class="metrics">


                    <div class="metric">

                        <span>
                            ACCESSIBILITY
                        </span>

                        <strong>
                            ${data.accessibility}/100
                        </strong>

                    </div>


                    <div class="metric">

                        <span>
                            TRAVEL TIME
                        </span>

                        <strong>
                            ${data.time} hrs
                        </strong>

                    </div>


                    <div class="metric">

                        <span>
                            DISTANCE
                        </span>

                        <strong>
                            ${data.distance} km
                        </strong>

                    </div>


                    <div class="metric">

                        <span>
                            ESTIMATED COST
                        </span>

                        <strong>
                            Rs ${data.cost}
                        </strong>

                    </div>


                </div>


                <!-- ACCESSIBILITY INTELLIGENCE -->

                <div class="accessibility-panel">


                    <div class="accessibility-title">

                        <div>

                            <h3>
                                Accessibility Intelligence
                            </h3>

                            <p>
                                Route accessibility analysis
                            </p>

                        </div>


                        <div class="overall-score">

                            ${details.overall}

                            <span>
                                /100
                            </span>

                        </div>

                    </div>


                    <!-- ROAD -->

                    <div class="access-item">

                        <div class="access-header">

                            <span>
                                Road Accessibility
                            </span>

                            <strong>
                                ${details.road}%
                            </strong>

                        </div>


                        <div class="progress">

                            <div
                                class="progress-fill"
                                style="width:${details.road}%">
                            </div>

                        </div>

                    </div>


                    <!-- TERRAIN -->

                    <div class="access-item">

                        <div class="access-header">

                            <span>
                                Terrain Condition
                            </span>

                            <strong>
                                ${details.terrain}%
                            </strong>

                        </div>


                        <div class="progress">

                            <div
                                class="progress-fill"
                                style="width:${details.terrain}%">
                            </div>

                        </div>

                    </div>


                    <!-- CONNECTIVITY -->

                    <div class="access-item">

                        <div class="access-header">

                            <span>
                                Connectivity
                            </span>

                            <strong>
                                ${details.connectivity}%
                            </strong>

                        </div>


                        <div class="progress">

                            <div
                                class="progress-fill"
                                style="width:${details.connectivity}%">
                            </div>

                        </div>

                    </div>


                    <!-- DISRUPTION -->

                    <div class="access-item">

                        <div class="access-header">

                            <span>
                                Disruption Factor
                            </span>

                            <strong>
                                ${details.disruption}%
                            </strong>

                        </div>


                        <div class="progress">

                            <div
                                class="progress-fill"
                                style="width:${details.disruption}%">
                            </div>

                        </div>

                    </div>


                </div>


                <!-- RISK -->

                <div class="risk-box">


                    <div>

                        <span>
                            RISK LEVEL
                        </span>

                        <strong>
                            ${data.risk}
                        </strong>

                    </div>


                    <div class="risk-confidence">

                        <span>
                            ML PREDICTION CONFIDENCE
                        </span>

                        <strong>
                            ${riskScore}/100
                        </strong>

                    </div>


                </div>


                <!-- ALTERNATIVE ROUTE -->

                <div class="alternative">

                    <span>
                        ALTERNATIVE ROUTE
                    </span>

                    <p>
                        ${data.alternative}
                    </p>

                </div>


                <!-- SHIPMENT INFORMATION -->

                <div class="shipment-info">


                    <p>

                        <strong>
                            Cargo:
                        </strong>

                        ${data.cargo}

                    </p>


                    <p>

                        <strong>
                            Priority:
                        </strong>

                        ${data.priority}

                    </p>


                    <p>

                        <strong>
                            Weight:
                        </strong>

                        ${data.weight} kg

                    </p>


                </div>


            </div>

        `;

    }


    // ERROR
    catch (error) {

        console.error(error);

        result.innerHTML = `

            <div class="empty-result">

                <h3>
                    Server Error
                </h3>

                <p>
                    Unable to analyze the route.
                </p>

            </div>

        `;

    }

}