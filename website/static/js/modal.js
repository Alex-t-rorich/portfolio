// Modal pop up, add modal paramaters in the top 
window.addEventListener('load', function () {


    // Singular Modal Map -- Add new Singular** Modal calls here
    var singleMap = new Map([
        [document.getElementById("profileAddBtn"), document.getElementById("profileAddModal")],
        [document.getElementById("navigationAddBtn"), document.getElementById("navigationAddModal")],
        [document.getElementById("educationAddBtn"), document.getElementById("educationAddModal")] 
    ]);


    // Navigation Edit Modal Map -- Copy and replace for Dynamic** Modals
    var navLoopCount = document.getElementById("navigation_count").value
    var navEditArray = []

    for (let i = 1; i <= navLoopCount; i++) {
        navEditArray.push({ key: document.getElementById("navigationEditBtn" + [i]), value: document.getElementById("navigationEditModal" + [i]) })
    };

    var navEditMap = new Map(
        navEditArray.map(object => {
            return [object.key, object.value];
        }),
    );


    // Education Edit Modal Map -- Copy and replace for Dynamic** Modals
    var educationLoopCount = document.getElementById("education_count").value
    var educationEditArray = []

    for (let i = 1; i <= educationLoopCount; i++) {
        educationEditArray.push({ key: document.getElementById("educationEditBtn" + [i]), value: document.getElementById("educationEditModal" + [i]) })
    };

    var educationEditMap = new Map(
        educationEditArray.map(object => {
            return [object.key, object.value];
        }),
    );


    // Joined Map -- Add new Maps here
    var modalMap = new Map([...singleMap, ...navEditMap, ...educationEditMap]); 

    modalMap.forEach((value, key) => {
        doModal(key, value);
    });


    // Function to show/hide Modal
    function doModal(anchor, popupbox) {

        var span = popupbox.getElementsByClassName("close")[0];

        anchor.addEventListener("click", function (event) {
            popupbox.style.display = "block";
        });

        span.addEventListener("click", function (event) {
            popupbox.style.display = "none";
        });

        window.addEventListener("click", function (event) {
            if (event.target == popupbox) {
                popupbox.style.display = "none";
            }
        });
    }
});

