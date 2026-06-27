function loadAvailability() {

    const lab = document.getElementById("id_lab").value;
    const date = document.getElementById("id_booking_date").value;

    if (!lab || !date) {
        return;
    }

    fetch(`/api/lab-availability/${lab}/?date=${date}`)

        .then(response => response.json())

        .then(data => {

            renderAvailabilityCalendar(data);

        });

}

function renderAvailabilityCalendar(bookings) {

    const container = document.getElementById(
        "availability-calendar"
    );

    if (!container) {
        return;
    }

    if (bookings.length === 0) {

        container.innerHTML =

        `
        <div class="alert alert-success">

            Entire Lab Available

        </div>
        `;

        return;

    }

    let html =

    `
    <div class="card border-warning mb-3">

        <div class="card-header bg-warning">

            Occupied Time Slots

        </div>

        <div class="card-body">

            <table class="table table-bordered table-sm">

                <thead>

                    <tr>

                        <th>Startup</th>

                        <th>Time</th>

                        <th>Status</th>

                    </tr>

                </thead>

                <tbody>
    `;

    bookings.forEach(function (booking) {

        html +=

        `
        <tr>

            <td>

                ${booking.startup}

            </td>

            <td>

                ${booking.from}

                -

                ${booking.to}

            </td>

            <td>

                <span class="badge bg-danger">

                    Occupied

                </span>

            </td>

        </tr>
        `;

    });

    html +=

    `
                </tbody>

            </table>

        </div>

    </div>
    `;

    container.innerHTML = html;

}

function slotAvailable(from, to, bookings) {

    const start = parseInt(
        from.replace(":", "")
    );

    const end = parseInt(
        to.replace(":", "")
    );

    for (const booking of bookings) {

        const bookedStart = parseInt(
            booking.from.replace(":", "")
        );

        const bookedEnd = parseInt(
            booking.to.replace(":", "")
        );

        if (

            start < bookedEnd &&

            end > bookedStart

        ) {

            return false;

        }

    }

    return true;

}

function validateLabSlot() {

    const lab = document.getElementById(
        "id_lab"
    ).value;

    const date = document.getElementById(
        "id_booking_date"
    ).value;

    const from = document.getElementById(
        "id_from_time"
    ).value;

    const to = document.getElementById(
        "id_to_time"
    ).value;

    if (

        !lab ||

        !date ||

        !from ||

        !to

    ) {

        return;

    }

    fetch(`/api/lab-availability/${lab}/?date=${date}`)

        .then(response => response.json())

        .then(bookings => {

            if (

                !slotAvailable(

                    from,

                    to,

                    bookings

                )

            ) {

                alert(

                    "Selected time slot is already booked."

                );

                document.getElementById(
                    "id_from_time"
                ).value = "";

                document.getElementById(
                    "id_to_time"
                ).value = "";

            }

        });

}

document.addEventListener(

    "DOMContentLoaded",

    function () {

        const lab = document.getElementById(
            "id_lab"
        );

        const date = document.getElementById(
            "id_booking_date"
        );

        const from = document.getElementById(
            "id_from_time"
        );

        const to = document.getElementById(
            "id_to_time"
        );

        if (lab) {

            lab.addEventListener(
                "change",
                loadAvailability
            );

        }

        if (date) {

            date.addEventListener(
                "change",
                loadAvailability
            );

        }

        if (from) {

            from.addEventListener(
                "change",
                validateLabSlot
            );

        }

        if (to) {

            to.addEventListener(
                "change",
                validateLabSlot
            );

        }

    }

);