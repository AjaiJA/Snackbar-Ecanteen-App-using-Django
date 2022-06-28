let tagsInput=document.querySelector('.tags-input')
let listArrTags=[]
let arr=[]
try {        
    tagsInput.addEventListener('keyup',(e)=>{
        if(e.keyCode===32){
            let inValue=e.target.value
            arr.push(inValue.replace(/\s/g,''))
            let newTagLi=''
            for(let i=0;i<arr.length;i++){
                newTagLi+=`<span>#${arr[i]}<i class="fa fa-times remove-tagicon" data-target="${i}"></i></span>`
            }
            document.querySelector('.tags').innerHTML=newTagLi
            tagsInput.value=''
        }
    })

    let xmlhttp = new XMLHttpRequest()
    xmlhttp.onreadystatechange = function () {
        if(this.readyState == 4 && this.status == 200) {
            let arrDetails = JSON.parse(this.responseText)
            listArrTags=arrDetails.existingtags
            arr.push(...listArrTags)
            let newTagLi=''
            for(let i=0;i<listArrTags.length;i++){
                newTagLi+=`<span>#${listArrTags[i]}<i class="fa fa-times remove-tagicon" data-target="${i}"></i></span>`
            }
            document.querySelector('.tags').innerHTML=newTagLi
        }
    };
    xmlhttp.open("GET", "/get-tags/", true);
    xmlhttp.send();

    document.querySelector('.save-tag').addEventListener('click',()=>{
        fetch("/add-tags/", {
            body: JSON.stringify({ tags: arr }),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            }
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.status==200) {
                console.log("Tags Added Successfully")
            }
        })
    })
} 
catch(error) {
    console.log(error)   
}

setInterval(()=>{
    let removeSection=document.querySelectorAll('.remove-tagicon')
    for(let i=0; i<removeSection.length; i++) {
        removeSection[i].addEventListener('click',removeTags)
    }
},3000)

let removeTags=(e)=>{
    arr.splice(e.target.getAttribute('data-target'),1)
    let newTagLi=''
    arr.forEach((element,index)=>{
        newTagLi+=`<span>#${element}<i class="fa fa-times remove-tagicon" data-target="${index}"></i></span>`
    })
    document.querySelector('.tags').innerHTML=newTagLi
}
