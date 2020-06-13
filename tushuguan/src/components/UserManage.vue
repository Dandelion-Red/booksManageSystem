<template>
  <div class="container">
    <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
      <FormItem prop="account">
        <Input type="text" v-model="formInline.account" placeholder="学号">
          <!--<Icon type="ios-person-outline" slot="prepend"></Icon>-->
        </Input>
      </FormItem>
      <FormItem prop="name">
        <Input type="text" v-model="formInline.name" placeholder="姓名">
          <!--<Icon type="ios-person-outline" slot="prepend"></Icon>-->
        </Input>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="handleSubmit('formInline')">查找</Button>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="modal1 = true">新添用户</Button>
      </FormItem>
    </Form>
    <Table border :columns="columns7" :data="data6"></Table>
    <Page :total="total" :page-size="10" @on-change="changePage"></Page>

    <Modal
      v-model="modal1"
      title="新添用户"
      @on-ok="ok('formItem2')"
    >
      <Form ref="formItem2" :model="formItem2" :rules="ruleItem2" :label-width="80">
        <FormItem label="账号" prop="account">
          <Input v-model="formItem2.account" placeholder=""></Input>
        </FormItem>
        <FormItem label="姓名" prop="name">
          <Input v-model="formItem2.name" placeholder=""></Input>
        </FormItem>
        <!--<FormItem label="性别" prop="sex">-->
          <!--<RadioGroup v-model="formItem2.sex">-->
            <!--<Radio label="男">男</Radio>-->
            <!--<Radio label="女">女</Radio>-->
          <!--</RadioGroup>-->
        <!--</FormItem> -->
        <FormItem label="密码" prop="pwd">
          <Input type="password" v-model="formItem2.pwd" placeholder="请输入密码"></Input>
        </FormItem>
        <FormItem label="状态" prop="normal">
          <Select v-model="formItem2.normal">
            <Option value="0">异常</Option>
            <Option value="1">正常</Option>
          </Select>
        </FormItem>
        <FormItem label="备注" prop="remark">
          <Input type="text" v-model="formItem2.remark" placeholder="默认输入0"></Input>
        </FormItem>
        <FormItem label="邮箱" prop="ema">
          <Input type="text" v-model="formItem2.ema" placeholder=""></Input>
        </FormItem>
        <FormItem label="电话" prop="tel">
          <Input type="text" v-model="formItem2.tel" placeholder=""></Input>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script type="es6">
  export default {
    name: 'UserManage',
    data () {
      return {
        total: '',
        condi: '',
        modal1: false,
        formInline: {
          account: '',
          name:''
        },
        formItem2: {
          account: '',
          name: '',
          normal: '',
          tel: '',
          ema: '',
          pwd:'',
          remark: ''
        },
        ruleItem2: {
          account: [{
            required: true,
            message: '请填写账号！',
            trigger: 'blur'
          }],
          name: [{
            required: true,
            message: '请填写学生姓名',
            trigger: 'blur'
          }],
          pwd: [{
            required: true,
            message: '请填写密码',
            trigger: 'blur'
          }]
        },
        columns7: [
          {
            title: '账号',
            key: 'RID',
            render: (h, params) => {
              return h('div', [
                // h('Icon', {
                //   props: {
                //     type: 'person'
                //   }
                // }),
                h('strong', params.row.RID)
              ])
            }
          },
          {
            title: '姓名',
            key: 'Rname'
          },
          {
            title: '身份',
            key: 'condi'
          },
          {
            title: '状态',
            key: 'Normal'
          },
          {
            title: '备注',
            key: 'Remark'
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
                      this.remove(params.index)
                    }
                  }
                }, '删除')
              ])
            }
          }
        ],
        data6: []
      }
    },
    mounted () {
      this.request(1)
    },
    methods: {
      handleSubmit (account) {
        this.request(1)
      },
      show (index) {
        // if (this.data6[index].condi === 0) {
        //   this.condi = '学生'
        // } else {
        //   this.condi = '图书管理员'
        // }
        this.$Modal.info({
          title: '用户信息',
          content: `姓名：${this.data6[index].Rname}<br>账号：${this.data6[index].RID}<br>身份：${this.data6[index].condi}<br>状态：${this.data6[index].Normal}<br>电话：${this.data6[index].Rtel}<br>邮箱：${this.data6[index].Rem}<br>`
        })
      },
      remove (index) {
        console.log(index)
        var that=this
        var delrid = that.data6[index].RID
        console.log(delrid)
        this.$http.get(that.GLOBAL.serverPath + '/delreader/'+delrid,
          {
          },
          {
            emulateJSON: true
          }
        ).then(function (res) {
          console.log(res.data)
          if(res.data.status==='ok'){
            that.$Message.success('删除成功')
            that.$Notice.config({
              top: 50,
              duration: 3,
              title: '通知',
              desc: '删除书籍成功!'
            })
            that.formInline.account=res.data.rid
            that.data6.splice(index, 1);
            //that.request(1)
          }

        })

      },
      request (currentPage) {
        var that = this
        this.$http.post(that.GLOBAL.serverPath + '/render_readerQuery',
          {
            account: that.formInline.account,
            // currentPage: currentPage
            name: that.formInline.name
          },
          {
            emulateJSON: true
          }
        ).then(function (res) {
          console.log(res.data)
          // that.total = res.data.pageInfo.total
          that.data6 = res.data.readers
        }).catch((e) => {
          this.$Message.fail('网络有误！')
        })
      },
      changePage: function (page) {
        this.request(page)
      },
      ok (name) {
        var that = this
        this.$refs[name].validate((valid) => {
          if (valid) {
            that.$http.post(that.GLOBAL.serverPath + '/readeradd',
              {
                account: that.formItem2.account,
                name: that.formItem2.name,
                normal: that.formItem2.normal,
                tel: that.formItem2.tel,
                ema: that.formItem2.ema,
                pwd: that.formItem2.pwd,
                remark: that.formItem2.remark,
              },
              {
                emulateJSON: true
              }
            ).then(function (res) {
              console.log(res.data.status)
              if (res.data.status === 'ok') {
                that.$Message.success('新增成功')
                that.formInline.account =res.data.rid
                that.request(1)
              } else {
                that.$Message.error('已存在该学号的用户')
              }

            }).catch((e) => {
              that.$Message.fail('网络有误！')
            })
          }
        })
      }
    }
  }
</script>

