/* let ctx1=document.querySelector('#myChart').getContext('2d')
let labels=[
    '2010',
    '2011',
    '2012',
    '2013',
    '2014',
    '2015',
    '2016',
    '2017',
    '2018',
]
let gradient=ctx1.createLinearGradient(0,0,0,400)
gradient.addColorStop(0,'rgba(58,123,213,1')
gradient.addColorStop(1,'rgba(0,210,255,0.3')
let data={
    labels,
    datasets:[
        {
            data:[211,326,365,350,420,370,500,375,415],
            label:"Sales",
            fill:true,
            backgroundColor:gradient,
            borderColor:'#fff',
            pointBackgroundColor:'rgb(189,195,199)',
            tension:0.5,
        },
    ]
}
let delayed;
let config= {
    type:'line',
    data:data,
    options: {
        responsive:true,
        radius:5,
        hitRadius:30,
        hoverRadius:12,
        animation: {
            onComplete:()=>{
                delayed=true
            },
            delay:(context)=>{
                let delay=0
                if(context.type=="data" && context.mode=="default" && !delayed) {
                    delay=context.dataIndex*300 + context.datasetIndex*100
                }
                return delay
            }
        },
        scales:{
            y: {
                ticks: {
                    callback:(value)=> {
                        return '$' + value + "m"
                    }
                }
            }
        }
    },
}

let myChart=new Chart(ctx1,config) */
