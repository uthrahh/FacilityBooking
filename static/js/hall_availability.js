document.addEventListener(
    "DOMContentLoaded",
    function () {

        const hall =
            document.getElementById(
                "id_hall"
            );

        if (!hall)
            return;

        hall.addEventListener(
            "change",
            function () {

                fetch(
                    `/api/hall-availability/${this.value}/`
                )

                .then(
                    response => response.json()
                )

                .then(
                    data => {

                        console.log(
                            "Occupied Slots",
                            data
                        );

                    }
                );

            }
        );

    }
);