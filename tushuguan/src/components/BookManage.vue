<!--Bname=title-->
<!--Author=author-->
<!--Pub=publisher-->
<!--Pyear=publishtime-->
<!--num=BID-->
<template>
  <div class="container">
    <Form ref="formInline" :model="formInline" :rules="ruleInline" inline >
      <FormItem prop="account">
        <Input type="text" v-model="formInline.title" placeholder="按书名查找">
        <!--<Icon type="ios-person-outline" slot="prepend"></Icon>-->
        </Input>
        <Input type="text" v-model="formInline.bid" placeholder="按书号查找"></Input>
        <Input type="text" v-model="formInline.isbn" placeholder="按ISBN查找"></Input>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="handleSubmit('formInline')">查找</Button>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="modal1 = true">新添书籍</Button>
      </FormItem>
    </Form>
    <!--
    data6为查找到的书籍信息
    -->
    <Table border :columns="columns7" :data="data6"></Table>
    <!--
    total is sum of data record
    page-size is the record number of a page
    -->
    <Page :total="total" :page-size="10" @on-change="changePage"></Page>

    <Modal
      v-model="modal1"
      title="新添书籍"
      width="800"
      scrollable="true"
      ok-text="添加"
      @on-ok="ok('formItem2')"
    >
      <Form ref="formItem2" :model="formItem2" :rules="ruleItem2" :label-width="80">
        <FormItem label="书号" prop="bid">
          <Input type="text" v-model="formItem2.bid" placeholder=""></Input>
        </FormItem>
        <FormItem label="书名" prop="title">
          <Input type="text" v-model="formItem2.title" placeholder=""></Input>
        </FormItem>
        <FormItem label="ISBN" prop="isbn">
          <Input type="text" v-model="formItem2.isbn" placeholder=""></Input>
        </FormItem>
        <FormItem label="状态" prop="sta">
          <Select v-model="formItem2.sta">
            <Option value="在架上">在架上</Option>
            <Option value="已借出">已借出</Option>
            <Option value="不外借">不外借</Option>
          </Select>
        </FormItem>
        <FormItem label="架位" prop="loc">
          <Input type="text" v-model="formItem2.loc" placeholder=""></Input>
        </FormItem>
        <FormItem label="作者" prop="author">
          <Input type="text" v-model="formItem2.author" placeholder=""></Input>
        </FormItem>
        <FormItem label="出版社" prop="publisher">
          <Input type="text" v-model="formItem2.publisher" placeholder=""></Input>
        </FormItem>
        <FormItem label="出版时间" prop="publishtime">
          <Input type="date" v-model="formItem2.publishtime" prop="publishtime"  placeholder="选择出版日期" style="width: 200px"></Input>
        </FormItem>
        <FormItem label="描述" prop="descri">
          <Input v-model="formItem2.descri" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="书籍描述..."></Input>
          <!--<quill-editor v-model="formItem2.descri" ref="VueQuillEditor"-->
                        <!--:content="content"-->
                        <!--@change="onEditorChange($event)">-->
          <!--</quill-editor>-->
        </FormItem>
      </Form>
    </Modal>

    <!--添加书籍副本-->
    <Modal
      v-model="modal2"
      title="新添书籍副本"
      ok-text="添加副本"
      @on-ok="ok2('formItem3')"
    >
      <Form ref="formItem3" :model="formItem3" :rules="ruleItem3" :label-width="80">
        <FormItem label="书号" prop="num">
          <Input type="text" v-model="formItem3.num" placeholder=""></Input>
        </FormItem>
        <FormItem label="状态" prop="sta">
          <Select v-model="formItem3.sta">
            <Option value="在架上">在架上</Option>
            <Option value="已借出">已借出</Option>
            <Option value="不外借">不外借</Option>
          </Select>
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
        //查询到的数据总数
        total: 0,
        condi: '',
        //增加图书，如果为true 则 会弹出增加图书的框
        modal1: false,
        //添加副本的框
        modal2: false,
        //添加书籍的描述框属性describe
        content:'',
        //最近被点击添加编号副本的图书编号
        currIndex: 0,
        //formInline 是查找的那个表格
        formInline: {
          title: '',
          bid: '',
          isbn: ''
        },
        //添加图书的表格
        formItem2: {
          title: '',
          author: '',
          publisher: '',
          publishtime: '',
          descri: '',
          loc: '',
          isbn: '',
          bid: '',
          sta:'',
        },
        ruleItem2: {
          isbn: [{
            required: true,
            message: '请填写ISBN！',
            trigger: 'blur'
          }],
          bid: [{
            required: true,
            message: '请填写书号！',
            trigger: 'blur'
          }],
          loc: [{
            required: true,
            message: '请填写架位！',
            trigger: 'blur'
          }],
          title: [{
            required: true,
            message: '请填写书名！',
            trigger: 'blur'
          }],
          author: [{
            required: true,
            message: '请填书籍作者',
            trigger: 'blur'
          }],
          publisher: [{
            required: true,
            message: '请填出版社',
            trigger: 'blur'
          }],
          publishtime: [{
            required: true,
            message: '请填写出版时间'
          }],
          descri: [{
            required: true,
            message: '请填书籍描述',
            trigger: 'blur'
          }]
        },
        //添加图书副本的bid
        formItem3: {
          num: '',
          sta: '',
        },
        ruleItem3: {
          num: [{
            required: true,
            message: '请填写书籍副本编号！',
            trigger: 'blur'
          }],
          sta: [{
            required: true,
            message: '请填写书籍状态！',
            trigger: 'blur'
          }],
        },
        //展示查找图书的信息的那几列属性值,在table中
        columns7: [
          {
            title: '编号',
            key: 'aid',
            render: (h, params) => {
              return h('div', [
                // h('Icon', {
                //   props: {
                //     type: 'document-text'
                //   }
                // }),
                h('strong', params.row.aid)
              ]);
            }
          },
          {
            title: '书名',
            key: 'title'
          },
          {
            title: '作者',
            key: 'author'
          },
          {
            title: '出版社',
            key: 'publisher'
          },
          {
            title: '状态',
            key: 'sta'
          },
          {
            title: '操作',
            key: 'action',
            width: 300,
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
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.modal2=true
                      // this.currIndex = this.data6[params.index].aid
                      this.currIndex = params.index

                    }
                  }
                }, '添加编号副本'),
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
              ]);
            }
          }
        ],
        //data6为查找到的书籍信息
        data6: [],
        data7: []
      }
    },
    mounted(){
      //request (currentPage=1)
      this.request(1);
    },
    methods: {
      handleSubmit(account) {
        //request (currentPage=1)
        this.request(1)
      },
      //点击查看图书信息
      show (index) {
        this.$Modal.info({
          title: '书籍信息',
          width: '1100',
          //content: `书名：${this.data6[index].title}<br>作者：${this.data6[index].author}<br>出版社：${this.data6[index].publisher}<br>出版时间：${this.data6[index].publishtime}<br>副本数量：${this.data6[index].num}<br>介绍：${this.data6[index].descri}`
          //副本数量：${this.data6[index].num}<br>可借数量：${this.data6[index].count}<br>可借副本编号：<span style="color:red;">${this.data6[index].suba}</span>
          content: `书号：${this.data6[index].aid}<br>ISBN：${this.data6[index].isbn}<br>书名：${this.data6[index].title}<br>作者：${this.data6[index].author}<br>出版社：${this.data6[index].publisher}<br>状态：${this.data6[index].sta}<br>架位：${this.data6[index].loc}<br>出版时间：${this.data6[index].publishtime}<br>介绍：${this.data6[index].descri}`

        })
      },
      //删除该条图书记录
      remove (index) {
        console.log(index)
        var that=this
        var delbid = that.data6[index].aid
        console.log(delbid)
        this.$http.get(that.GLOBAL.serverPath + '/delbook/'+delbid,
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
            that.formInline.isbn=res.data.isbn
            that.data6.splice(index, 1);
            //that.request(1)
          }

          })

      },
      request (currentPage){
        var that=this
        this.$http.post(that.GLOBAL.serverPath + '/render_bookQuery',
          {
            title: that.formInline.title,
            isbn: that.formInline.isbn,
            bid: that.formInline.bid,
            currentPage: currentPage
          },
          {
            emulateJSON: true
          }
        ).then(function (res) {
          console.log(res.data)
          // that.total=res.data.pageInfo.total
          that.total=1
          //data6为查找到的书籍信息
          that.data6=[]
          // that.data7=res.data.albums
          that.data7=res.data.books
          that.data7.forEach((e) => {
            let obj={}
            //aid 为图书号
            obj.aid = e.BID
            obj.title = e.Bname
            obj.author = e.Author
            obj.publisher = e.Pub
            obj.publishtime = e.Pyear
            obj.descri = e.Per
            obj.sta = e.Sta
            obj.isbn = e.ISBN
            obj.loc = e.Loc

            // var count=0
            // var s=''
            // e.subalbums.forEach((item)=>{
            //   if( item.condi===0 ){
            //     //count为可借数量
            //     count++
            //     //可借编号
            //     s=s+item.number+','
            //   }
            // })
            //count为可借数量
            // obj.count = count
            //可借编号
            // obj.suba = s
            that.data6.push(obj)
          })
        })
      },
      changePage: function(page){
        this.request(page)
      },
      // ok is  a function of  adding a book
      ok (name) {
        var that=this
        this.$refs[name].validate((valid) => {
          if (valid) {
            that.$http.post(that.GLOBAL.serverPath + '/bookadd',
              {
                bname: that.formItem2.title,
                isbn: that.formItem2.isbn,
                bid: that.formItem2.bid,
                loc: that.formItem2.loc,
                author: that.formItem2.author,
                pub: that.formItem2.publisher,
                pyear: that.formItem2.publishtime,
                per: that.formItem2.descri,
                sta:  that.formItem2.sta,
              },
              {
                emulateJSON: true
              }
            ).then(function (res) {
              console.log(res.data.status)
              if(res.data.status==='ok'){
                that.$Message.success('新增成功')
                that.$Notice.config({
                  top: 50,
                  duration: 3,
                  title: '通知',
                  desc: '新添书籍成功!'
                })
                that.formInline.isbn=res.data.isbn
                that.formItem2.title=''
                that.formItem2.author=''
                that.formItem2.publisher=''
                that.formItem2.publishtime=''
                that.formItem2.descri=''
                that.request(1)
              }

            }).catch((e) => {
              that.$Message.fail('网络有误！')
            })
          }
        })
      },
      ok2 (name) {
        var that=this
        this.$refs[name].validate((valid) => {
          if (valid) {
            var newindex=that.currIndex
            console.log(newindex)
            console.log(that.GLOBAL.serverPath + '/bookaddcopy?bid='+that.formItem3.num)
            // that.$http.get(that.GLOBAL.serverPath + '/bookaddcopy/'+that.formItem3.num,
            that.$http.post(that.GLOBAL.serverPath + '/bookaddcopy',
              {
                //bid为新增书籍的bid
                bid: that.formItem3.num,
                oldbid: that.data6[newindex].aid,
                // bname: that.data6[newindex].title,
                // author: that.data6[newindex].author,
                // pub: that.data6[newindex].publisher,
                // pyear: that.data6[newindex].publishtime,
                // per: that.data6[newindex].descri,
                // loc: that.data6[newindex].loc,
                sta: that.formItem3.sta,

              },
              {
                emulateJSON: true
              }
            ).then(function (res) {
              console.log(res.data.status)
              if(res.data.status==='ok'){
                that.$Message.success('新增成功')
                that.formInline.bid=res.data.bid
                that.formItem3.num=''
                that.request(1)
              }else{
                that.$Message.error('新增失败！查看是否存在相同编号')
              }

            }).catch((e) => {
              that.$Message.fail('网络有误！')
            })
          }
        })
      },
      onEditorChange({editor,html,text}){
        // 富文本编辑器，文本改变时，设置字段值
        console.log(editor,html,text)
        this.content = html
      }
    }
  }
</script>

