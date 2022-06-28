setInterval(()=>{
    fetch("/notifications/", {
        body: JSON.stringify({ source:"snackbar" }),
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        }
    })
    .then((res) => res.json())
    .then((data) => {
        let dropDownNotification=document.querySelector('.dropdown-menu.notifications')
        let listValues=""
        listValues+=`<li class="head text-light p-3" style="background-color:rgb(255,116,0);font-size:15px;">
                        <div class="row">
                            <div class="col-lg-12 col-sm-12 col-12">
                                <span class="notification-unviewed-count"></span>
                                <a href="#" onclick="clearNotificationDB(event);" class="float-right clear-notification-db" style="color:white;">Clear All</a>
                            </div>
                        </div>
                    </li>`
        let unviewedCount=0
        if(data.length>0) {
            for(let i=0;i<data.length;i++) {
                let insertValue=data[i].fields
                if(!insertValue.is_viewed) {
                    unviewedCount++
                }
                let bgColor=insertValue.is_viewed ? "bg-white" : "bg-gray"
                listValues += `<li class="notification-box ${bgColor}">
                                    <div class="row" style="cursor: pointer;">
                                        <div class="col-lg-3 col-sm-3 col-3 py-2 text-center">
                                            <img src="https://e7.pngegg.com/pngimages/15/560/png-clipart-verified-badge-symbol-computer-icons-twitter-discord-flat-icon-blue-text.png" height="50px">
                                        </div>
                                        <div class="col-lg-8 col-sm-8 col-8">
                                            From : 
                                            <strong class="text-success">SnackBar</strong> 
                                            To : 
                                            <strong class="text-success">${insertValue.username} (you)</strong>
                                            <div>
                                                ${insertValue.message}
                                            </div>
                                            <small style="font-weight: bolder;" class="text-info">${insertValue.notification_date}</small>
                                        </div>
                                    </div>
                                </li>`
            }
        }
        else{
            listValues += `<li class="notification-box bg-white">
                                <div class="row" style="cursor: pointer;">
                                    <div style="font-size:17px;line-height:100px;">
                                        <div class="text-danger text-center">
                                            Empty
                                        </div>
                                    </div>
                                </div>
                            </li>`
        }
        listValues+=`<li style="background-color: orangered;" class="footer view-notification-btn text-center">
                    </li>`
        dropDownNotification.innerHTML=listValues
        document.querySelector('.notification-unviewed-count').innerHTML=`Notifications (${unviewedCount})`
        document.querySelector('.unviewed-icon-badge').innerHTML=unviewedCount
    })
},1000)

document.querySelector('.notification-view-btn-icon').addEventListener('click',()=>{
    fetch("/notification-viewing/", {
        body: JSON.stringify({ source:"snackbar" }),
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        }
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Viewed")
    })
})

let clearNotificationDB=(event)=>{
    event.preventDefault()
    fetch("/notification-delete/", {
        body: JSON.stringify({ source:"snackbar" }),
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        }
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Removed")
    })
}
