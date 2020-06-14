<template>
  <div class="container">
  <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
    <FormItem label="罚金单价"  prop="cost">
      <Input type="text" v-model="formInline.cost" ></Input>
    </FormItem>
    <FormItem label="借阅天数"  prop="cost">
      <Input type="text" v-model="formInline.borrowdays" ></Input>
      <br>
      <br>
      <Button type="primary" @click="updatedata()">更新</Button>
    </FormItem>
    <FormItem label="预约天数"  prop="cost">
      <Input type="text" v-model="formInline.reservedays" ></Input>
    </FormItem>
    <!--<FormItem>-->
      <!---->
    <!--</FormItem>-->
  </Form>
  </div>
</template>

<script>
  export default {
    name: 'Setting',
    data () {
      return {
        formInline: {
          cost: '',
          reservedays: '',
          borrowdays: ''
        }
      }
    },
    mounted () {
      this.request()
    },
    methods: {
      request () {
        var that = this
        this.$http.post(that.GLOBAL.serverPath + '/querySetting',
          {},
          {
            emulateJSON: true
          }
        ).then(function (res) {
          console.log(res.data)
          var result = res.data
          if (result.status === 'ok') {
            that.formInline.cost = result.cost
            that.formInline.borrowdays = result.borrowdays
            that.formInline.reservedays = result.reservedays
          } else {
            that.$Message.error('初始化成功！')
          }
        }).catch((e) => {
          that.$Message.fail('网络有误！')
        })
      },
      updatedata () {
        var that = this
        this.$http.post(that.GLOBAL.serverPath + '/updateSetting',
          {
            cost: that.formInline.cost,
            borrowdays: that.formInline.borrowdays,
            reservedays: that.formInline.reservedays
          },
          {
            emulateJSON: true
          }
        ).then(function (res) {
          console.log(res.data)
          var result = res.data
          if (result.status === 'ok') {
            that.formInline.cost = result.cost
            that.formInline.borrowdays = result.borrowdays
            that.formInline.reservedays = result.reservedays
            that.$Message.error('更新成功！')
          } else {
            that.$Message.error('更新失败！')
          }
        }).catch((e) => {
          that.$Message.fail('网络有误！')
        })
      }
    }
  }
</script>

<style scoped>

</style>
