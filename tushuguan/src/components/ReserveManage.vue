<template>
  <div class="container">
    <Form ref="formInline" :model="formInline" :rules="inputrule" inline>
      <FormItem prop="borrowRecord">
        <Input type="text" v-model="formInline.raccount" placeholder="借阅者号">
          <!--<Icon type="ios-person-outline" slot="prepend"></Icon>-->
        </Input>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="handleSubmit('formInline')">查找</Button>
      </FormItem>
    </Form>
    <Table border :columns="columns7" :data="data6"></Table>
    <Page :total="total" :page-size="10" @on-change="changePage"></Page>

    <Modal
      v-model="modal2"
      title="预约修改"
      ok-text="确定"
      @on-ok="ok2('formItem3')"
    >
      <Form ref="formItem3" :model="formItem3"  :label-width="80">
        <FormItem label="选择时间" prop="newretain">
          <Input type="date" v-model="formItem3.newretain" prop="newretain"  placeholder="选择日期" style="width: 200px"></Input>
        </FormItem>

      </Form>
    </Modal>

  </div>
</template>

<script type="es6">
  export default {
    name: 'ReserveManage',
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
      formItem3: {
        newretain:'',
      },
      columns7: [
        {
          title: '书号',
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
        {
          title: '开始预约时间',
          key: 'starttime'
        },
        {
          title: '预约保留至',
          key: 'retain'
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
                    this.modal2=true
                    this.currIndex = params.index
                  }
                }
              }, '修改'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.delrec(params.index)
                  }
                }
              }, '删除')
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
    ok2 (name) {
      var that=this
      this.$refs[name].validate((valid) => {
        if (valid) {
          var newindex=that.currIndex
          console.log(newindex)
          console.log(that.formItem3.newretain)
          that.$http.post(that.GLOBAL.serverPath + '/updateReserve',
            {
              newdate: that.formItem3.newretain,
              bid: that.data6[newindex].bid,
              rid: that.data6[newindex].rid,
              starttime: that.data6[newindex].starttime
            },
            {
              emulateJSON: true
            }
          ).then(function (res) {
            console.log(res.data.status)
            if(res.data.status==='ok'){
              that.$Message.success('更新成功')
              // that.formInline.raccount=res.data.rid
              that.request(1)
            }else{
              that.$Message.error('更新失败！')
            }

          }).catch((e) => {
            that.$Message.fail('网络有误！')
          })
        }
      })
    },
    delrec (index) {
      //this.data6.splice(index, 1);
      var that=this
      this.$http.post(that.GLOBAL.serverPath + '/delReserve',
        {
          bid: that.data6[index].bid,
          rid: that.data6[index].rid,
          starttime:that.data6[index].starttime,
        },
        {
          emulateJSON: true
        }
      ).then(function (res) {
        if(res.data.status === 'ok'){
          that.data6.splice(index,1)
          this.$Message.success('删除成功')
        }else{
          this.$Message.status('删除失败')
        }
      })
    },
    request (currentPage){
      var that=this
      var raccount = that.formInline.raccount
      this.$http.post(that.GLOBAL.serverPath + '/reserveRrecord',
        {
            rid: raccount,
        },
        {
          emulateJSON: true
        }
      ).then(function (res) {
        console.log(res.data.reserveRrecord)
        // that.total=res.data.pageInfo.total
        that.data6=[]

        that.data7=res.data.reserveRrecord
        that.data7.forEach((e) =>{
          let obj = {}
          obj.bid = e.BID
          obj.title = e.Bname
          obj.rid = e.RID
          obj.aptime1=e.Aptime1
          var d = new Date(e.Aptime1);
          console.log('================================')
          console.log(d)
          d.setHours(d.getHours() - 8)
          console.log('================================')
          console.log(d)
          console.log('================================')

          obj.starttime = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate()  ;//+ d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
          console.log(obj.starttime)
          var dd = new Date(e.Aptime2 );
          dd.setHours(dd.getHours() - 8)
          obj.retain = dd.getFullYear() + '-' + (dd.getMonth() + 1) + '-' + dd.getDate() ;//+ ' ' + dd.getHours() + ':' + dd.getMinutes() + ':' + dd.getSeconds();
          obj.condi = e.Status
          console.log(obj)
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

<style scoped>

</style>
