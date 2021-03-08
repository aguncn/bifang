<template>
<div>
    <a-card :bordered="false">
      <div style="display: flex; flex-wrap: wrap">
          <head-info title="项目数量" content="25个" :bordered="true"/>
          <head-info title="应用数量" content="108个" :bordered="true"/>
          <head-info title="发布单数量" content="6572个"/>
      </div>
    </a-card>
        <a-row style="margin-top:20px">
            <a-col style="padding-right:2px" :xl="16" :lg="24" :md="24" :sm="24" :xs="24">
            <a-card class="project-list" style="margin-bottom: 24px;" :bordered="false" title="进度" :body-style="{padding: 0}">
                <a slot="extra">全部项目</a>
                <div>
                <a-card-grid :key="i" v-for="(item, i) in projects">
                    <a-card :bordered="false" :body-style="{padding: 0}">
                    <a-card-meta :description="item.desc">
                        <div slot="title" class="card-title">
                        <a-avatar size="small" :src="item.logo" />
                        <span>Alipay</span>
                        </div>
                    </a-card-meta>
                    <div class="project-item">
                        <a class="group" href="/#/">科学搬砖组</a>
                        <span class="datetime">9小时前</span>
                    </div>
                    </a-card>
                </a-card-grid>
                </div>
            </a-card>
            <a-card title="全部项目" :bordered="false">
                <a-list>
                <a-list-item :key="index" v-for="(item, index) in activities">
                    <a-list-item-meta>
                    <a-avatar slot="avatar" :src="item.avatar" />
                    <div slot="title" v-html="item.template" />
                    <div slot="description">9小时前</div>
                    </a-list-item-meta>
                </a-list-item>
                </a-list>
            </a-card>
            </a-col>
            <a-col style="padding-left: 12px" :xl="8" :lg="24" :md="24" :sm="24" :xs="24">
            <a-card title="快捷入口" style="margin-bottom: 24px" :bordered="false" :body-style="{padding: 0}">
                <div class="item-group">
                <a-tag color="red">
                    <a>发布单列表</a>
                </a-tag>
                <a-tag color="green">
                    <a>创建发布单</a>
                </a-tag>
                <a-tag color="blue">
                    <a>服务部署</a>
                </a-tag>
                <a-tag color="green">
                    <a>添加项目</a>
                </a-tag>
                <a-tag color="green">
                    <a>用户权限</a>
                </a-tag>
                </div>
            </a-card>
            <a-card title="运行动态" style="margin-bottom: 24px" :bordered="false">
                <div style="min-height: 400px;">
                <a-list>
                <a-list-item :key="index" v-for="(item, index) in activities">
                    <a-list-item-meta>
                    <a-avatar slot="avatar" :src="item.avatar" />
                    <div slot="title" v-html="item.template" />
                    <div slot="description">9小时前</div>
                    </a-list-item-meta>
                </a-list-item>
                </a-list>
                </div>
            </a-card>
            <a-card title="团队" :bordered="false">
                <div class="members">
                <a-row>
                    <a-col :span="12" v-for="(item, index) in teams" :key="index">
                    <a>
                        <a-avatar size="small" :src="item.avatar" />
                        <span class="member">{{item.name}}</span>
                    </a>
                    </a-col>
                </a-row>
                </div>
            </a-card>
            </a-col>
        </a-row>
</div>
</template>
<script>
import HeadInfo from '@/components/tool/headInfo'

const projects = [
    {
        logo:'https://gw.alipayobjects.com/zos/rmsportal/WdGqmHpayyMjiEhcKoVE.png',
        desc:'这是一个发布最多的项目咋滴啊 不服啊'
    },
    {
        logo:'https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png',
        desc:'这是一个最牛逼的的项目咋滴啊 不服啊 来啊 单挑啊'
    },
    {
        logo:'https://gw.alipayobjects.com/zos/rmsportal/dURIMkkrRFpPgTuzkwnB.png',
        desc:'这是一个吹的最多的的的项目咋滴啊 不服啊 来啊 单挑啊'
    }
]

const avatars = [
  'https://gw.alipayobjects.com/zos/rmsportal/cnrhVkzwxjPwAaCfPbdc.png',
  'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
  'https://gw.alipayobjects.com/zos/rmsportal/gaOngJwsRYRaVAuXXcmB.png',
  'https://gw.alipayobjects.com/zos/rmsportal/WhxKECPNujWoWEFNdnJE.png',
  'https://gw.alipayobjects.com/zos/rmsportal/ubnKSIfAJTxIgXOKlciN.png',
  'https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png'
]

const activities = [
    {
        avatar: avatars[0],
        template: 'XXXX创建了发布单'
    },
    {
        avatar: avatars[1],
        template: 'XXXX创建了发布单'
    },
    {
        avatar: avatars[2],
        template: 'XXXX创建了发布单'
    },
    {
        avatar: avatars[3],
        template: 'XXXX创建了发布单'
    },
    {
        avatar: avatars[4],
        template: 'XXXX创建了发布单'
    },
]
const teams = [
    {
        avatar: avatars[0],
        name: 'FED天团'
    },
    {
        avatar: avatars[1],
        name: 'FED天团'
    },
    {
        avatar: avatars[2],
        name: 'FED天团'
    },
    {
        avatar: avatars[3],
        name: 'FED天团'
    },
]
export default {
    name:"dashboard",
    components: {HeadInfo},
    data(){
        return {
            projects:projects,
            activities:activities,
            teams:teams
        }
    }
}
</script>
<style lang="less">
.project-list {
  .card-title {
    span{
      vertical-align: middle;
      &:last-child{
        margin-left: 12px;
      }
    }
  }
  .project-item {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    overflow: hidden;
    font-size: 12px;
    color: inherit;
    .group{
      color: @bf-text-color;
      flex: 1 1 0;
      &:hover {
        color: @bf-primary-color;
      }
    }
    .datetime {
      color: @bf-text-color-second;
      flex: 0 0 auto;
    }
  }
  .ant-card-meta-description {
    height: 44px;
    line-height: 22px;
    overflow: hidden;
  }
}
.item-group{
  padding: 20px 0 8px 24px;
  font-size: 0;
  span {
      margin: 5px;
  }
  a{
    color: inherit;
    display: inline-block;
    font-size: 14px;
    margin-bottom: 13px;
    width: 25%;
  }
}
.members {
  a {
    display: block;
    margin: 12px 0;
    color: @bf-text-color;
    &:hover {
      color: @bf-primary-color;
    }
    .member {
      vertical-align: middle;
      margin-left: 12px;
    }
  }
}

</style>