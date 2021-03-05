<template>
    <div>
        <a-select
            show-search
            placeholder="环境"
            option-filter-prop="children"
            style="width: 80px"
            v-model="env"
            @change="onSelectChange"
          >
            <a-select-option v-for="d in items" :key="d.value">
            {{ d.label }}
            </a-select-option>
          </a-select>
          <a-popconfirm
          	:title="`是否将${record.name}发布单流转到${env}环境?`"
          	ok-text="是" 
          	cancel-text="否"
            :visible="visible"
            @visibleChange="handleVisibleChange"
          	@confirm="handleChange">
          	<a-button type="danger">{{title}}</a-button>
          </a-popconfirm>
    </div>
</template>
<script>
export default {
    name:"envExchange",
    data(){
        return {
            env:"",
            visible:false
        }
    },
    props:{
        title:String,
        items: Array,
        record: Object
    },
    methods:{
        handleVisibleChange(visible) {
            if (!visible) {
                this.visible = false;
                return;
            }

            if (!this.env) {
                this.$message.error("请选择流转环境");
            } else {
                this.visible = true;
            }
        },
        onSelectChange(value){
            this.env = value
        },
        handleChange(){
            this.$emit("onChange",this.record,this.env)
            this.env = ""
        }
    }
}
</script>