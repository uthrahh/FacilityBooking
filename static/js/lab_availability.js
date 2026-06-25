document.addEventListener(
    "DOMContentLoaded",
    function () {

        const lab =
            document.getElementById(
                "id_lab"
            );

        if (!lab)
            return;

        lab.addEventListener(
            "change",
            function () {

                fetch(
                    `/api/lab-availability/${this.value}/`
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