
document.addEventListener("DOMContentLoaded", function () {
    var addPopup = document.getElementById("add-popup");
    var popupOverlay = document.querySelector(".popup-overlay");
    var popupBox = document.querySelector(".popup-box");
    var cancelpopup = document.getElementById("cancel-popup");

    var container = document.querySelector(".container");
    var note = document.getElementById("add-note");
    var noteTitle = document.getElementById("note-title-input");
    var shortDescription = document.getElementById("note-description-input");
    var change = document.getElementById("change");

    addPopup.addEventListener("click", function () {
        popupOverlay.style.display = "block";
        popupBox.style.display = "block";
    });

    cancelpopup.addEventListener("click", function () {
        popupOverlay.style.display = "none";
        popupBox.style.display = "none";
    });

    // note.addEventListener("click", function (event) {
    //     event.preventDefault();
    //     if (noteTitle.value !== "") {
    //         // var div = document.createElement("div");
    //         // div.setAttribute("class", "note-container");
    //         // div.innerHTML = `<h2>{{data.title}}</h2>
    //         //                  <p>{{data.note}}</p>
    //         //                  <button type="button" class="delete" onclick="deleteitem(event)">Delete</button>`;
    //         // container.append(div);

    //         // Reset input values
    //        title

        //     popupOverlay.style.display = "none";
        //     popupBox.style.display = "none";
        //  }
        // })


});

function add(event){
    
    popupOverlay.style.display = "none";
    popupBox.style.display = "none";
    
}

function deleteitem(event){
    event.target.parentElement.remove()
}