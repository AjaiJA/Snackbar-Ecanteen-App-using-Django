let isNavVisible=false
let maxNav=()=>{
    let sideNavBar=document.querySelector(".sidebar-nav-main")
    sideNavBar.classList.toggle('active-nav')
    if(isNavVisible) {
        document.querySelector('.sidebar-nav-main ul li input').style.display="none"
        isNavVisible=false
    }
    else {
        document.querySelector('.sidebar-nav-main ul li input').style.display="block"
        isNavVisible=true
    }
}

let updateFoodItem=(event)=>{
    var foodId=event.target.querySelector('.Food_id').value;
    var foodName=event.target.querySelector('.food-name-field').value;
    var foodRatePerQuantity=event.target.querySelector('.food-rate-per-quantity').value;
    var foodAvailableTotalQuantity=event.target.querySelector('.food-available-total-quantity ').value;
    fetch("/admin/update-food/", {
        body: JSON.stringify({ 
            foodId : foodId,
            foodName : foodName,
            foodRatePerQuantity : foodRatePerQuantity,
            foodAvailableTotalQuantity : foodAvailableTotalQuantity,
        }),
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        }
    })
    .then((res) => res.json())
    .then((data) => {
        if(data.status_code==200) {
            // setTimeout(()=>location.reload(),5000)
            document.querySelector('.food-updated-status-para').innerHTML="Food Item Updated Successfully"
        }
        setTimeout(()=>document.querySelector('.food-updated-status-para').innerHTML="",5000)
    })
    event.preventDefault ? event.preventDefault() : (event.returnValue=false)
}

console.log(document.querySelectorAll('.user-name-column'))
let idToUsername=document.querySelectorAll('.user-name-column')
if(idToUsername.length>0) {
    for(let i=0; i<idToUsername.length; i++) {
        fetch("/admin/find-user/", {
            body: JSON.stringify({ 
                userId:idToUsername[i].innerHTML
            }),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            }
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.status_code==200) {
                // setTimeout(()=>location.reload(),5000)
                idToUsername[i].innerHTML=data.username
                console.log(data.username)
            }
        })
    }
}

function resetForm() { 
    
}

const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button")
let input = document.querySelector(".image-data-input")
let dynamicDiv=document.querySelector('.file-dynamic-section')
let file

button.onclick = ()=>{
    console.log("d")
    input.click()
}

input.addEventListener("change", function(){
    file = this.files[0]
    let file1=input.value
    dropArea.classList.add("active")
    showFile()
})

dropArea.addEventListener("dragover", (event)=>{
    event.preventDefault()
    dropArea.classList.add("active")
    dragText.textContent = "Release to Upload File"
})

dropArea.addEventListener("dragleave", ()=>{
    dropArea.classList.remove("active")
    dragText.textContent = "Drag & Drop to Upload File"
})

dropArea.addEventListener("drop", (event)=>{
    event.preventDefault()
    file = event.dataTransfer.files[0]
    showFile()
})

function showFile() {
    let fileType = file.type;
    let validExtensions = ["image/jpeg", "image/jpg", "image/png"]
    if(validExtensions.includes(fileType)) {
        let fileReader = new FileReader()
        fileReader.onload = ()=> {
            let fileURL = fileReader.result
            let imgTag = `<img src="${fileURL}" alt="image"/>`
            dropArea.innerHTML = imgTag
        }
        fileReader.readAsDataURL(file)
        dynamicDiv.innerHTML="Click here to Change the image"
        dynamicDiv.onclick = ()=>{
            input.click()
        }
        dynamicDiv.style.cursor="pointer"
        dynamicDiv.style.color="blue"
    }
    else {
        alert("This is not an Image File!")
        dropArea.classList.remove("active")
        dragText.textContent = "Drag & Drop to Upload File"
        dynamicDiv.innerHTML="Upload your Food Image Here!"
         dynamicDiv.style.cursor="default"
        dynamicDiv.style.color="#999"
        dynamicDiv.onclick =null
    }
}

(function ($) {
    'use strict';
    try {
        var file_input_container = $('.js-input-file');
        if (file_input_container[0]) {
            file_input_container.each(function () {
                var that = $(this);
                var fileInput = that.find(".input-file");
                var info = that.find(".input-file__info");
                fileInput.on("change", function () {
                    var fileName;
                    fileName = $(this).val();
                    if (fileName.substring(3,11) == 'fakepath') {
                        fileName = fileName.substring(12);
                    }
                    if(fileName == "") {
                        info.text("No file chosen");
                    } else {
                        info.text(fileName);
                    }
                })
            });
        }
    }
    catch (e) {
        console.log(e);
    }
})(jQuery);
