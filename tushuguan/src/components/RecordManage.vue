<!--Bname=title-->
<!--BID=bid-->
<!--RID=raccount-->
<!--Rname=rname-->
<!--botime=time-->
<!--Rbtime1=backtime-->
<template>
  <div class="container">
    <Form ref="formInline" :model="formInline" :rules="inputrule" inline>
      <FormItem prop="borrowRecord">
        <Input type="text" v-model="formInline.raccount" placeholder="借阅者学号">
          <!--<Icon type="ios-person-outline" slot="prepend"></Icon>-->
        </Input>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="handleSubmit('formInline')">查找</Button>
      </FormItem>
    </Form>
    <Table border :columns="columns7" :data="data6"></Table>
    <Page :total="total" :page-size="10" @on-change="changePage"></Page>
  </div>
</template>
<script type="es6">
  export default {
    name: 'RecordManage',
    data () {
      return {
        total: '',
        condi: '',
        nowtime:'',
        modal1: false,
        modal2: false,
        currIndex: 0,//最近被点击添加编号副本的图书编号
        formInline: {
          raccount: ''
        },
        inputrule: {
          raccount:[{
            required: true,
            message: '请填写借阅号！',
            trigger: 'blur'
          }]
        },
        columns7: [
          {
            title: '编号',
            key: 'bid',
            render: (h, params) => {
              return h('div', [
                // h('Icon', {
                //   props: {
                //     type: 'document-text'
                //   }
                // }),
                h('strong', params.row.bid)
              ]);
            }
          },
          {
            title: '书名',
            key: 'title'
          },
          // {
          //   title: '编号',
          //   key: 'number'
          // },
          // {
          //   title: '借阅者学号',
          //   key: 'raccount'
          // },
          // {
          //   title: '借阅者姓名',
          //   key: 'rname'
          // },
          {
            title: '借阅时间',
            key: 'time'
          },
          {
            title: '应归还时间',
            key: 'rbtime'
          },
          {
            title: '状态',
            key: 'condi'
          },
          {
            title: '操作',
            key: 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.show(params.index)
                    }
                  }
                }, '查看'),
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.reback(params.index)
                    }
                  }
                }, '确认归还')
              ]);
            }
          }
        ],
        data6: [],
        data7: [] //存放从后台请求过来的借阅记录
      }
    },
    mounted(){
      this.request(1);
    },
    methods: {
      handleSubmit(account) {
        this.request(1)
      },
      show (index) {
        this.$Modal.info({
          title: '书籍信息',
          content: `书籍号：${this.data6[index].bid}<br>书名：${this.data6[index].title}<br>借阅者学号：${this.data6[index].raccount}<br>借阅者姓名：${this.data6[index].rname}<br>借阅时间：${this.data6[index].time}<br>应归还时间：${this.data6[index].rbtime}<br>归还时间：${this.data6[index].backtime}<br>罚金：${this.data6[index].penalty}`
        })
      },
      reback (index) {
        //this.data6.splice(index, 1);
        var that=this
        this.$http.post(that.GLOBAL.serverPath + '/excise/reback',
          {
            bid: that.data6[index].bid,
            sid: that.data6[index].sid
          },
          {
            emulateJSON: true
          }
        ).then(function (res) {
          if(res.data.status === 'yes'){
            that.data6.splice(index,1)
            this.$Message.success('操作成功')
          }else{
            this.$Message.status('操作失败')
          }
        })
      },
      request (currentPage){
        var that=this
        var raccount = that.formInline.raccount
        this.$http.get(that.GLOBAL.serverPath + '/render_borrowHistory/'+raccount,
          {

            // currentPage: currentPage
          },
          {
            emulateJSON: true
          }
        ).then(function (res) {
          console.log(res.data.borrowrecords)
          // that.total=res.data.pageInfo.total
          that.data6=[]
          that.data7=res.data.borrowrecords
          var readername = res.data.readername
          // nowtime = res.data.time
          // console.log(nowtime)
          that.data7.forEach((e) =>{
            let obj = {}
            obj.bid = e.BID
            obj.title = e.Bname
            // obj.number = e.subalbum.number
            obj.raccount = e.RID
            obj.rname = readername
            obj.time = e.Botime
            obj.rbtime = e.Rbtime1
            obj.backtime = e.Rbtime2
            obj.penalty = e.Penalty
            obj.condi = e.Condi
            // var time = new Date().getTime();
            // if(  !e.Rbtime2 ){
            //   obj.condi = '未归还'
            // }
            //else{
            //   var delayDay = (nowtime-e.Rbtime1).days
            //   obj.condi = '已超期'
            // }
            that.data6.push(obj)
          })
        })
      },
      changePage: function(page){
        this.request(page)
      },
    }
  }
</script>

