let equipmentData = [];

function loadEquipment() {

    const lab = document.getElementById("id_lab").value;
    const date = document.getElementById("id_booking_date").value;

    if (!lab || !date) {
        return;
    }

    fetch(`/api/equipment/${lab}/?date=${date}`)

        .then(response => response.json())

        .then(data => {

            equipmentData = data;

            renderAvailability(data);

            document.getElementById(
                "equipment-rows"
            ).innerHTML = "";

            addEquipmentRow();

        });

}

function renderAvailability(data) {

    const container = document.getElementById(
        "equipment-container"
    );

    container.innerHTML = "";

    if (data.length === 0) {

        container.innerHTML =
            `<div class="alert alert-warning">
                No Equipment Found
            </div>`;

        return;

    }

    data.forEach(eq => {

        let occupied = "";

        if (eq.occupied.length === 0) {

            occupied =
                `<li class="text-success">
                    Fully Available
                </li>`;

        }

        else {

            eq.occupied.forEach(slot => {

                occupied +=
                    `<li class="text-danger">
                        ${slot.from} - ${slot.to}
                    </li>`;

            });

        }

        container.innerHTML +=

        `
        <div class="card mb-3 border-primary">

            <div class="card-body">

                <div class="d-flex justify-content-between">

                    <div>

                        <h5>

                            ${eq.name}

                        </h5>

                        <small>

                            ₹${eq.rate}/hour

                        </small>

                    </div>

                </div>

                <hr>

                <strong>

                    Occupied Slots

                </strong>

                <ul>

                    ${occupied}

                </ul>

            </div>

        </div>
        `;

    });

}

function addEquipmentRow() {

    const container = document.getElementById(
        "equipment-rows"
    );

    const row = document.createElement("div");

    row.className =
        "card p-3 mb-3 equipment-row";

    row.innerHTML =

    `
    <div class="row align-items-end">

        <div class="col-md-5">

            <label>

                Equipment

            </label>

            <select
                class="form-select equipment-select"
                name="equipment"
            >

                <option value="">

                    Select Equipment

                </option>

                ${
                    equipmentData.map(eq =>

                    `
                    <option value="${eq.id}">

                        ${eq.name}

                    </option>
                    `

                    ).join("")
                }

            </select>

        </div>

        <div class="col-md-2">

            <label>

                From

            </label>

            <input
                type="time"
                class="form-control from-time"
                name="from_time"
            >

        </div>

        <div class="col-md-2">

            <label>

                To

            </label>

            <input
                type="time"
                class="form-control to-time"
                name="to_time"
            >

        </div>

        <div class="col-md-2">

            <button
                type="button"
                class="btn btn-danger w-100 remove-btn"
            >

                Remove

            </button>

        </div>

    </div>
    `;

    container.appendChild(row);

    copyFirstTime(row);

    row.querySelector(".remove-btn")
        .onclick = function () {

            row.remove();

            calculateFee();

        };

    row.querySelector(".equipment-select")
        .addEventListener(
            "change",
            validateRow
        );

    row.querySelector(".from-time")
        .addEventListener(
            "change",
            validateRow
        );

    row.querySelector(".to-time")
        .addEventListener(
            "change",
            validateRow
        );

}

function copyFirstTime(newRow) {

    const rows = document.querySelectorAll(
        ".equipment-row"
    );

    if (rows.length < 2)
        return;

    newRow.querySelector(".from-time").value =
        rows[0].querySelector(".from-time").value;

    newRow.querySelector(".to-time").value =
        rows[0].querySelector(".to-time").value;

}

function validateRow(event) {

    const row = event.target.closest(
        ".equipment-row"
    );

    const equipmentId =
        row.querySelector(".equipment-select").value;

    const from =
        row.querySelector(".from-time").value;

    const to =
        row.querySelector(".to-time").value;

    if (!equipmentId || !from || !to) {

        calculateFee();

        return;

    }

    const equipment =
        equipmentData.find(
            e => String(e.id) === equipmentId
        );

    if (!equipment) {

        return;

    }

    if (isOverlapping(
        from,
        to,
        equipment.occupied
    )) {

        alert(
            "Selected slot is already occupied."
        );

        row.querySelector(".from-time").value = "";

        row.querySelector(".to-time").value = "";

        return;

    }

    calculateFee();

}

function calculateFee() {

    let total = 0;

    document.querySelectorAll(
        ".equipment-row"
    ).forEach(row => {

        const equipmentId =
            row.querySelector(".equipment-select").value;

        const from =
            row.querySelector(".from-time").value;

        const to =
            row.querySelector(".to-time").value;

        if (!equipmentId || !from || !to)
            return;

        const equipment =
            equipmentData.find(
                e => String(e.id) === equipmentId
            );

        if (!equipment)
            return;

        const start =
            new Date("1970-01-01T" + from);

        const end =
            new Date("1970-01-01T" + to);

        const hours =
            (end - start) / 3600000;

        total +=
            hours * parseFloat(equipment.rate);

    });

    document.getElementById(
        "fee-display"
    ).innerHTML = total.toFixed(2);

}

function isOverlapping(from, to, occupied) {

    const start =
        from.replace(":", "");

    const end =
        to.replace(":", "");

    for (const slot of occupied) {

        const slotStart =
            slot.from.replace(":", "");

        const slotEnd =
            slot.to.replace(":", "");

        if (
            start < slotEnd &&
            end > slotStart
        ) {

            return true;

        }

    }

    return false;

}

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const lab =
            document.getElementById("id_lab");

        const date =
            document.getElementById("id_booking_date");

        if (lab)
            lab.addEventListener(
                "change",
                loadEquipment
            );

        if (date)
            date.addEventListener(
                "change",
                loadEquipment
            );

    }
);