function loadHallAvailability() {

    const hall = document.getElementById("id_hall").value;
    const date = document.getElementById("id_booking_date").value;

    if (!hall || !date) {

        return;

    }

    fetch(`/api/hall-availability/${hall}/?date=${date}`)

        .then(response => response.json())

        .then(data => {

            renderHallAvailability(data);

        });

}

function renderHallAvailability(bookings) {

    const container = document.getElementById(
        "availability"
    );

    if (!container) {

        return;

    }

    if (bookings.length === 0) {

        container.className =
            "alert alert-success";

        container.innerHTML =
        `
        <strong>

            Hall Available

        </strong>

        <br>

        No approved bookings found.

        `;

        return;

    }

    let html =

    `
    <strong>

        Occupied Slots

    </strong>

    <table class="table table-sm table-bordered mt-2">

        <thead>

            <tr>

                <th>

                    Startup

                </th>

                <th>

                    Time

                </th>

            </tr>

        </thead>

        <tbody>
    `;

    bookings.forEach(function(slot){

        html +=

        `
        <tr>

            <td>

                ${slot.startup}

            </td>

            <td>

                ${slot.from}

                -

                ${slot.to}

            </td>

        </tr>
        `;

    });

    html +=

    `
        </tbody>

    </table>
    `;

    container.className =
        "alert alert-warning";

    container.innerHTML =
        html;

}

function slotAvailable(from,to,bookings){

    let start =
        parseInt(
            from.replace(":","")
        );

    let end =
        parseInt(
            to.replace(":","")
        );

    for(let booking of bookings){

        let bookedStart =
            parseInt(
                booking.from.replace(":","")
            );

        let bookedEnd =
            parseInt(
                booking.to.replace(":","")
            );

        if(

            start < bookedEnd &&

            end > bookedStart

        ){

            return false;

        }

    }

    return true;

}

function validateHallBooking(){

    const hall =
        document.getElementById(
            "id_hall"
        ).value;

    const date =
        document.getElementById(
            "id_booking_date"
        ).value;

    const from =
        document.getElementById(
            "id_from_time"
        ).value;

    const to =
        document.getElementById(
            "id_to_time"
        ).value;

    if(

        !hall ||

        !date ||

        !from ||

        !to

    ){

        return;

    }

    fetch(`/api/hall-availability/${hall}/?date=${date}`)

        .then(response=>response.json())

        .then(bookings=>{

            if(

                !slotAvailable(

                    from,

                    to,

                    bookings

                )

            ){

                alert(

                    "Selected hall is already booked during this time."

                );

                document.getElementById(
                    "id_from_time"
                ).value="";

                document.getElementById(
                    "id_to_time"
                ).value="";

            }

        });

}

document.addEventListener(

    "DOMContentLoaded",

    function(){

        const hall =
            document.getElementById(
                "id_hall"
            );

        const date =
            document.getElementById(
                "id_booking_date"
            );

        const from =
            document.getElementById(
                "id_from_time"
            );

        const to =
            document.getElementById(
                "id_to_time"
            );

        if(hall){

            hall.addEventListener(

                "change",

                loadHallAvailability

            );

        }

        if(date){

            date.addEventListener(

                "change",

                loadHallAvailability

            );

        }

        if(from){

            from.addEventListener(

                "change",

                validateHallBooking

            );

        }

        if(to){

            to.addEventListener(

                "change",

                validateHallBooking

            );

        }

    }

);