// import {loginForm} from './html.js';

window.onload = () => {
    // document.querySelector('.login-form-app-attached').innerHTML=loginForm
    let currentUrl=window.location.href
    let navBarSection = document.querySelectorAll('.navbar-section a')
    if(currentUrl.includes("dishes")) 
        navBarSection[2].classList.add('active')
    else if(currentUrl.includes("order")) 
        navBarSection[3].classList.add('active')
    else if(currentUrl.includes("menu")) 
        navBarSection[1].classList.add('active')
    else if(currentUrl.includes("review")) 
        navBarSection[4].classList.add('active')
    else if(currentUrl.includes("about")) 
        navBarSection[5].classList.add('active')
    else if(currentUrl.includes("cart")) {
       
    }
    else if(currentUrl.includes("profile")) {
        let profilePincode=document.querySelector('.profile-pincode')
        
        let imgInput=document.querySelector('.profile-image-input')
        let imgTag=document.querySelector('.img-profile')

        imgInput.addEventListener('change',(e)=> {
            imgTag.src=URL.createObjectURL(e.target.files[0]);
        })
        imgTag.addEventListener('click',(e)=> {
            imgInput.click()
        })

        profilePincode.addEventListener('input',(event)=>{
            let xmlhttp = new XMLHttpRequest();
            let url = `https://api.postalpincode.in/pincode/${event.target.value}` 
            xmlhttp.onreadystatechange = function () {
                if(this.readyState == 4 && this.status == 200) {
                    let arrDetails = JSON.parse(this.responseText);
                    if(arrDetails[0].PostOffice!=null){
                        document.querySelector('.profile-state').value=arrDetails[0].PostOffice[0].State
                        document.querySelector('.profile-district').value=arrDetails[0].PostOffice[0].District
                        document.querySelector('.profile-country').value=arrDetails[0].PostOffice[0].Country
                    }
                }
            }
            xmlhttp.open("GET", url, true)
            xmlhttp.send()
        })       
    }
    else {
        navBarSection[0].classList.add('active')
    }
}

let menu = document.querySelector('#hamburger-menu')
let navbar = document.querySelector('.navbar-section')
let isMenuBtnClicked=false;

menu.onclick = () => {
    if(isMenuBtnClicked) {
        menu.classList.toggle('fa-bars')
        menu.classList.remove('fa-times')
        menu.style.background="linear-gradient(#ffd900, #ff340b)"
        menu.style.color="#fff"
        isMenuBtnClicked=false
    }
    else {
        menu.classList.toggle('fa-times')
        menu.classList.remove('fa-bars')
        menu.style.background="linear-gradient(#ffd900, #ff340b)"
        menu.style.color="#fff"
        isMenuBtnClicked=true
    }
    navbar.classList.toggle('active')
}

const cartButtons = document.querySelectorAll('.cart-button');

cartButtons.forEach(button => {
	button.addEventListener('click', cartClick);
});

let addToCart=(event)=> {
    let xhr
    if(window.XMLHttpRequest)
    {
        xhr=new XMLHttpRequest()
    }
    else
    {
        xhr=new ActiveXObject("Microsoft.XMLHTTP")
    }
   /*  xhr.onreadystatechange=()=>{
        if(xhr.readyState==4 && xhr.status==200) {
            console.log(xhr.responseText)
        }
        else {
            console.log(xhr.status)
        }
    } */
    var Food_id=event.target.querySelector('.Food_id').value;
    var User_id=event.target.querySelector('.User_id ').value;
    var params="Food_id=" + Food_id + "&User_id=" + User_id;
    xhr.open("POST","/addItemToCart/");
    xhr.setRequestHeader('content-type',"application/x-www-form-urlencoded");
    // xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}')
    // a.setRequestHeader('content-length',val.length);
    // a.setRequestHeader('connection',"close");
    event.preventDefault ? event.preventDefault() : (event.returnValue=false);
    // location.reload();
    xhr.send(params);
}

function cartClick() {
	let button = this;
	button.classList.add('clicked');
    // addToCart(this)
}

let count = 0;
$('.cart-button').on('click', function (){
    let cart = $('.icon-button');
    let imgtodrag = $(this).parent('form').parent('.dish-cart-img').find("img").eq(0);
    if(imgtodrag) {
        setTimeout(function(){
            var imgclone = imgtodrag.clone().offset({
                top: imgtodrag.offset().top,
                left: imgtodrag.offset().left
            }).css({
                'opacity': '0.9',
                'position': 'absolute',
                'height': '150px',
                'width': '150px',
                'z-index': '1000',
            }).appendTo($('body')).animate({
                'top': cart.offset().top + 20,
                'left': cart.offset().left + 30,
                'width': 75,
                'height': 75
            }, 1000, 'easeInOutExpo');
            setTimeout(function(){
                count++;
                $(".icon-button .icon-button__badge").text(count);
                /* $(".icon-button i").css({
                    'background':'linear-gradient(#ffd900, #ff340b)',
                    'transform':'rotate(360deg) skew(-2deg) scale(1.2)',
                    'transition':'all 0.4s ease-in',
                }) */
                /* setTimeout(function(){
                    $(".icon-button i").css({
                        'background':'#eee',
                        'transition':'all 0.4s ease-in',
                    })
                },200); */
            }, 1500);
            imgclone.animate({
                'width': 0,
                'height': 0
            }, function(){
                $(this).detach()
            });
        },1000);
    }
});

let section = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header .navbar-section a');

window.onscroll = () =>{

    menu.classList.remove('fa-times');
    navbar.classList.remove('active');

    section.forEach(sec =>{

        let top = window.scrollY;
        let height = sec.offsetHeight;
        let offset = sec.offsetTop - 150;
        let id = sec.getAttribute('id');

        if(top >= offset && top < offset + height){
        navLinks.forEach(links =>{
            links.classList.remove('active');
            document.querySelector('header .navbar-section a[href*='+id+']').classList.add('active');
        });
        };
    });
}

var swiper = new Swiper(".home-slider", {
    spaceBetween: 35,
    centeredSlides: true,
    autoplay: {
        delay: 7500,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    loop:true,
});

var swiper = new Swiper(".review-slider", {
    spaceBetween: 20,
    centeredSlides: true,
    autoplay: {
        delay: 7500,
        disableOnInteraction: false,
    },
    loop:true,
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        640: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});

/* let loginPopupBtn=document.querySelector('.login-popup-btn')
let isPopped=false

loginPopupBtn.onclick = (e) => { 
    if(isPopped) {
        loginPopupBtn.style.background="transparent"
        loginPopupBtn.style.color="#192a56"
        closeLoginPopup()
    }
    else {
        let container=document.body
        let popupWindow=document.createElement('div')
        popupWindow.setAttribute('class','login-popup-window')
        container.appendChild(popupWindow)
  
        let popupOuter=document.createElement('div')
        popupOuter.setAttribute('class','login-outer')
        popupWindow.appendChild(popupOuter)
  
        let closeIcon = document.createElement('div')
        closeIcon.setAttribute('class','fa fa-times')
        // closeIcon.textContent="X"
        closeIcon.setAttribute('title','close')
        closeIcon.addEventListener('click',closeLoginPopup)
        popupOuter.appendChild(closeIcon)
        
        let popupInner=document.createElement('div')
        popupInner.setAttribute('class','login-border')
        // popupInner.innerHTML=loginForm
        popupOuter.appendChild(popupInner)
        loginPopupBtn.style.background="linear-gradient(#ffd900, #ff340b)"
        loginPopupBtn.style.color="#fff"
        isPopped=true
        popupWindow.addEventListener('click',closeLoginPopup)
        popupOuter.addEventListener('click',function (event){
            event.stopPropagation();
        });
    }
    e.preventDefault()
}

let closeLoginPopup = () => {
    document.querySelector('.login-outer').style.transform="scale(0.4)"
    document.querySelector('.login-outer').style.transition="all .3s ease-out"
    document.querySelector('.login-popup-window').style.transition="all .3s ease-out"
    document.querySelector('.login-popup-window').style.transitionDelay=".3s"
    setTimeout(()=>{
        document.querySelector('.login-popup-window').remove()
        loginPopupBtn.style.background="linear-gradient(#ffd900, #ff340b)"
        loginPopupBtn.style.color="white"
        isPopped=false
    },200)
}  */

window.onscroll=()=>scrollIndicator();

let scrollIndicator=()=>{
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("myBar").style.width = scrolled + "%";
}

const draggables = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.cart-container .products .products')

let cartContainer=document.querySelector('.cart .cart-total')

draggables.forEach(draggable => {
    draggable.addEventListener('dragstart',()=> {
        draggable.classList.add('dragging')
    });
    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging')
        let foodId=document.querySelectorAll('.cart-buy-product .cart-product-item-list')
        totalCost=0
        totalItems=0
        if(foodId.length<1) {
            cartContainer.querySelector('a').setAttribute('disabled', 'disabled')
        }
        else {
            cartContainer.querySelector('a').removeAttribute('disabled')
        }
        for(let i=0;i<foodId.length;i++) {
            totalCost+=Number(foodId[i].querySelector('.total-cost').getAttribute('data-target'))
            foodId[i].querySelector('.cart-quantity-input').removeAttribute('disabled')
            totalItems++
        }
        cartContainer.querySelector('.total-cost-checkout').innerHTML='₹' + totalCost
        cartContainer.querySelector('.total-items').innerHTML=totalItems
        disableIncQuantity()
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', (e) => { 
        e.preventDefault()
        const afterElement = getDragAfterElement(container, e.clientY)
        const draggable = document.querySelector('.dragging')
        if (afterElement == null) {
            container.appendChild(draggable);
        } else {
            container.insertBefore(draggable, afterElement)
        }
    })
})

let getDragAfterElement=(container, y)=> {
    const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')];
    return draggableElements.reduce((closest,child)=>{
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2
        if(offset < 0 && offset > closest.offset){
            return {offset:offset,element:child};
        }
        else{
            return closest;
        }
    },{offset:Number.NEGATIVE_INFINITY}).element;
}

let totalCost=0 
let totalItems=0

cartContainer.querySelector('.total-items').innerHTML=totalItems
cartContainer.querySelector('.total-cost-checkout').innerHTML='₹ ' + totalCost

window.onload=()=>{
    
    // setInterval(()=>{
        let today=new Date()
        let date=today.getFullYear() + '-' + ('0'+Number(today.getMonth()+1)).slice(-2) + '-' +('0'+today.getDate()).slice(-2)
        let time=('0'+today.getHours()).slice(-2) + ":" + ('0'+today.getMinutes()).slice(-2)

        cartContainer.querySelector('#order-date-time').value=date + 'T' + time
        cartContainer.querySelector('#order-date-time').min=date + 'T' + time
    
        Date.prototype.addDays = function(days) {
            let date = new Date(this.valueOf())
            date.setDate(date.getDate() + days)
            return date
        }
        let maxDate=new Date()
        let addThreeDay =maxDate.addDays(3)
        date=addThreeDay.getFullYear() + '-' + ('0'+Number(addThreeDay.getMonth()+1)).slice(-2) + '-' +('0'+addThreeDay.getDate()).slice(-2)
        cartContainer.querySelector('#order-date-time').max=date + 'T00:00'
    // },1000)
    loadCartCalc()
    disableIncQuantity()
}

let disableIncQuantity=()=>{
    let foodId=document.querySelectorAll('.save-later-container .cart-product-item-list')
    for(let i=0;i<foodId.length;i++) {
        foodId[i].querySelector('.cart-quantity-input').setAttribute('disabled','disabled')
    }
}

let loadCartCalc=()=>{
    let foodId=document.querySelectorAll('.cart-buy-product .cart-product-item-list')
    let totalCostCalc=()=>{
        totalCost=0
        for(let i=0;i<foodId.length;i++) {
            totalCost+=Number(foodId[i].querySelector('.total-cost').getAttribute('data-target'))
        }
        cartContainer.querySelector('.total-cost-checkout').innerHTML='₹ ' + totalCost
    }
    if(foodId.length<1) {
        cartContainer.querySelector('a').setAttribute('disabled', 'disabled')
    }
    else {
        cartContainer.querySelector('a').removeAttribute('disabled')
    }
    for(let i=0;i<foodId.length;i++) {
        fetch("/food-details/", {
            body: JSON.stringify({ Food_id: foodId[i].getAttribute('data-target') }),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            }
        })
        .then((res) => res.json())
        .then((data) => {
//             available_status: true
console.log(data)
            foodId[i].querySelector('img').src=`/Media/${data.food_image.slice(1, data.food_image.length - 1)}`
            foodId[i].querySelector('.cart-quantity-input').max=data.food_available_quantity
            foodId[i].querySelector('.product-info .product-offer .current-rate').innerHTML=" ₹"+data.food_price
            foodId[i].querySelector('.product-info .product-offer .old-rate').innerHTML=" ₹"+data.food_old_price
            foodId[i].querySelector('.product-name').innerHTML=data.food_name
            foodId[i].querySelector('.total-cost').innerHTML='₹ ' + Number(data.food_price)
            foodId[i].querySelector('.expiry-date').innerHTML= data.expiry_days_count + ' days'
            foodId[i].querySelector('.total-cost').setAttribute('data-target',Number(data.food_price))
            totalCostCalc()

            foodId[i].querySelector('.cart-quantity-input').addEventListener('change',()=>{
                if(foodId[i].querySelector('.cart-quantity-input').value>data.food_available_quantity) {
                    foodId[i].querySelector('.cart-quantity-input').value=data.food_available_quantity
                }
                foodId[i].querySelector('.total-cost').innerHTML='₹ ' + foodId[i].querySelector('.cart-quantity-input').value*data.food_price
                foodId[i].querySelector('.total-cost').setAttribute('data-target',foodId[i].querySelector('.cart-quantity-input').value*data.food_price)
                totalCostCalc()
            })                      
        })
        totalItems++;
        cartContainer.querySelector('.total-items').innerHTML=totalItems
        totalCostCalc()
    }
} 

let loginRequest=(event)=> {
    let xhr
    if(window.XMLHttpRequest)
    {
        xhr=new XMLHttpRequest()
    }
    else
    {
        xhr=new ActiveXObject("Microsoft.XMLHTTP")
    }
    /* xhr.onreadystatechange=function()
    {
        if(xhr.readyState==4 && xhr.status==200)
        {
            alert(xhr.responseText);
        }
    } */
    alert("k")
    var username=document.querySelector('.container-login .user-name').value
    var password=document.querySelector('.container-login .password').value
    var params="username=" + username + "&password=" + password
    xhr.open("POST","/login/")
    xhr.setRequestHeader('content-type',"application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}')
    // a.setRequestHeader('content-length',val.length);
    // a.setRequestHeader('connection',"close");
    event.preventDefault ? event.preventDefault() : (event.returnValue=false);
    // location.reload();
    xhr.send(params);
}

(function ($) {
    "use strict"
    let input = $('.validate-input .input')
    $('.validate-form').on('submit',function(){
        let check = true
        for(let i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }
        return check;
    });


    $('.validate-form .input').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }
})(jQuery);

let usernameField=document.querySelector('.signup-username')
let emailField=document.querySelector('.signup-email')
let feedBackArea = document.querySelector(".invalid_feedback")
let emailFeedBackArea = document.querySelector(".emailFeedBackArea")
let usernameSuccessOutput = document.querySelector(".usernameSuccessOutput")
let submitBtn = document.querySelector(".signup-btn-create")

emailField.addEventListener("keyup", (e) => {
    let emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch("/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            if (data.email_error) {
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p style="margin-top:-30px;color:red;font-size:20px;">${data.email_error}</p>`;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });
    }
});

usernameField.addEventListener("keyup", (e) => {
    let usernameVal = e.target.value;

    usernameSuccessOutput.style.display = "block";

    usernameSuccessOutput.textContent = `${usernameVal} available`;

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/validate-username", {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            usernameSuccessOutput.style.display = "none";
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                submitBtn.disabled = true;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });
    }
});
