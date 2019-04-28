
var dom = document.getElementById("main");
var myChart = echarts.init(dom);
var thisYear = 2019
var heatData = [];
for (var i = 0; i < 200; ++i) {
    heatData.push([
        100 + Math.random() * 20,
        24 + Math.random() * 16,
        Math.random()
    ]);
}
for (var j = 0; j < 10; ++j) {
    var x = 100 + Math.random() * 16;
    var y = 24 + Math.random() * 12;
    var cnt = 30 * Math.random();
    for (var i = 0; i < cnt; ++i) {
        heatData.push([
            x + Math.random() * 2,
            y + Math.random() * 2,
            Math.random()
        ]);
    }
}

 option = {
    backgroundColor: '#1b1b1b',
    title : {
        text: '热力图结合地图',
        x:'center',
        textStyle: {
            color: 'white'
        }
    },
    tooltip : {
        trigger: 'item',
        formatter: '{b}'
    },
    series : [
        {
            name: '北京',
            type: 'map',
            mapType: 'china',
            roam: true,
            hoverable: false,
            data:[],
            heatmap: {
                minAlpha: 0.1,
                data: heatData
            },
            itemStyle: {
                normal: {
                    borderColor:'rgba(100,149,237,0.6)',
                    borderWidth:0.5,
                    areaStyle: {
                        color: '#1b1b1b'
                    }
                }
            }
        }
    ]
};

if (option && typeof option === "object") {
    myChart.setOption(option, true);
    
}
$(document).ready(function(){
    $('#zoomer').prev('div').hide()
    setTimeout(function(){$('#zoomer').next().hide()},2000)
    $('#tourismYear').change(function(){
        let val = $('#tourismYear').val()
        thisYear = val
        let url = '/static/config/heatPoint'+val+'.json'
        $.ajax({
            type:"GET",
            url: url,
            data: null,
            dataType:'json',
            cache:false,
            success: function(ret) {
                data = ret
                refreshData(data)
            },
            error: function(ret) {
                console.log(ret)
            }
    })
})
})
