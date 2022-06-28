let proceedPayment = (event)=>{
    event.preventDefault()
    let cartContainer=document.querySelector('.cart .cart-total')
    let cartItemSection=document.querySelector('.cart-container .cart-buy-product')
    let selectedItemsSection=cartItemSection.querySelectorAll('.cart-product-item-list')
    let orderArr=[]
    let totalPrice=0,noOfItems=0
    let id=1
    for(let i=0;i<selectedItemsSection.length;i++) {
        orderArr.push({
            "id":id,
            "Food_id":selectedItemsSection[i].getAttribute('data-target'),
            "Food_Name":selectedItemsSection[i].querySelector('.product-info .product-name').innerHTML,
            "Price":selectedItemsSection[i].querySelector('.product-info .product-offer .current-rate').innerHTML,
            "Quantity":selectedItemsSection[i].querySelector('.product-info .product-quantity input').value,
            "Total_Cost":selectedItemsSection[i].querySelector('.product-info .product-quantity .total-cost').innerHTML,
        })
        id++
    }
    noOfItems=cartContainer.querySelector('.total-items').innerHTML
    totalPrice= cartContainer.querySelector('.total-cost-checkout').innerHTML
    let purchasingDate = cartContainer.querySelector('#order-date-time').value

    if(selectedItemsSection.length>0) {
        fetch("/book-order/", {
            body: JSON.stringify({ 
                order_list : orderArr,
                total_price : Number(totalPrice.slice(2, totalPrice.length)),
                no_of_items : noOfItems,
                purchasing_date : purchasingDate,
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
                let options = {
						"key": "rzp_test_OVyyUIZk4uYtWE",
						"amount": Number(totalPrice.slice(2, totalPrice.length) * 100),
						"currency": "INR",
						"name": "SnackBar",
						"description": data.order_id,
						"image": "https://media.istockphoto.com/photos/appetizing-roasted-fillet-of-pork-picture-id467852533?s=612x612",
                        "prefill": {
                            "name": data.username,
                            "email": data.email,
                            "contact": data.phone_no
                        },
                        "notes": {
                            "address": ""
                        },
                        "theme": {
                            "color": "#ff340b"
                        },
						"handler": (response)=>{
							fetch("/payment-success/", {
                                body: JSON.stringify({ 
                                    order_id : data.order_id,
                                    amount : Number(totalPrice.slice(2, totalPrice.length) * 100),
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
                                    cartContainer.querySelector('.status-display').innerHTML=data.status
                                    cartContainer.querySelector('.status-display').style.color="green"
                                    setTimeout(()=>location.reload(),7000)
                                }
                                else {
                                    cartContainer.querySelector('.status-display').innerHTML="Payment Unsuccessfull"
                                    cartContainer.querySelector('.status-display').style.color="red"
                                }
                            })
						}
					}
				let paymentWindow = new Razorpay(options)
                paymentWindow.open()	
            }
            else {
                cartContainer.querySelector('.status-display').innerHTML=data.status
                cartContainer.querySelector('.status-display').style.color="red"
            }
        })
    }
    else {
        cartContainer.querySelector('.status-display').innerHTML="Cart is Empty"
        cartContainer.querySelector('.status-display').style.color="red"
    }
}

/* let today=new Date() 
let date=today.getFullYear() + '-' + ('0'+Number(today.getMonth()+1)).slice(-2) + '-' +('0'+today.getDate()).slice(-2)
let time=('0'+today.getHours()).slice(-2) + ":" + ('0'+today.getMinutes()).slice(-2)
purchased_date : date + 'T' + time */

let printItemsData=(event)=>{
    console.log("h")
}