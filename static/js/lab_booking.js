document.addEventListener(
    "DOMContentLoaded",
    function () {

        const labSelect =
            document.getElementById(
                "id_lab"
            );

        const equipmentSelect =
            document.getElementById(
                "id_equipments"
            );

        labSelect.addEventListener(
            "change",
            function () {

                fetch(
                    `/equipment/${this.value}/`
                )

                .then(
                    response => response.json()
                )

                .then(
                    data => {

                        equipmentSelect.innerHTML = "";

                        data.forEach(
                            equipment => {

                                let option =
                                    document.createElement(
                                        "option"
                                    );

                                option.value =
                                    equipment.id;

                                option.textContent =
                                    equipment.name;

                                equipmentSelect.appendChild(
                                    option
                                );

                            }
                        );

                    }
                );

            }
        );

    }
);