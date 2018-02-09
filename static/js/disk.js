var myPie = echarts.init(document.getElementById('disk'));

var option = {
    title : {
        text: '磁盘使用率',
        subtext: '双击666',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    color:['#D48265', '#91C7AE'],
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['已使用', '未使用']
    },
    series : [
        {
            name: '访问来源',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                {value:335, name:'已使用'},
                {value:310, name:'未使用'},
            ],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
myPie.setOption(option);