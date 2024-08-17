<template>
  <div style="display: flex">
    <div style="width: 450px">
      <span style="color: rgba(42,53,191,0.89)">数据：</span>
      <el-table :data="inputData" style="width: 450px; margin-top: 20px" border stripe fit show-header size="small">
        <el-table-column prop="0" label="天气" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][0]" placeholder="请选择">
              <el-option label="晴天" value="晴天"></el-option>
              <el-option label="雨天" value="雨天"></el-option>
              <el-option label="阴天" value="阴天"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="1" label="温度" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][1]" placeholder="请选择">
              <el-option label="炎热" value="炎热"></el-option>
              <el-option label="适宜" value="适宜"></el-option>
              <el-option label="寒冷" value="寒冷"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="2" label="湿度" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][2]" placeholder="请选择">
              <el-option label="潮湿" value="潮湿"></el-option>
              <el-option label="适宜" value="适宜"></el-option>
              <el-option label="干燥" value="干燥"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="3" label="风速" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][3]" placeholder="请选择">
              <el-option label="强风" value="强风"></el-option>
              <el-option label="轻风" value="轻风"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="4" label="打羽毛球" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][4]" placeholder="请选择">
              <el-option label="合适" value="合适"></el-option>
              <el-option label="不宜" value="不宜"></el-option>
            </el-select>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="margin-left: 30px; width: 500px">
      <el-button type="primary" @click="get_decision_tree_ID3_result">计算</el-button>
      <div style="margin-top: 20px">
        <MyMermaid :chart="ID3_tree_mermaid_code" :key="componentKey"/>
      </div>
    </div>
  </div>
</template>

<script>

import MyMermaid from '@/components/Mermaid.vue';

export default {
  components: {
    MyMermaid,
  },
  name: 'DecisionTreeView',
  data() {
    return {
      componentKey: 0,
      inputData: [
        ['晴天', '炎热', '潮湿', '轻风', '不宜'],
        ['晴天', '炎热', '潮湿', '强风', '不宜'],
        ['阴天', '炎热', '潮湿', '轻风', '合适'],
        ['雨天', '适宜', '潮湿', '轻风', '合适'],
        ['雨天', '寒冷', '适宜', '轻风', '合适'],
        ['雨天', '寒冷', '适宜', '强风', '不宜'],
        ['阴天', '寒冷', '适宜', '强风', '合适'],
        ['晴天', '适宜', '潮湿', '轻风', '不宜'],
        ['晴天', '寒冷', '适宜', '轻风', '合适'],
        ['雨天', '适宜', '适宜', '轻风', '合适'],
        ['晴天', '适宜', '适宜', '强风', '合适'],
        ['阴天', '适宜', '潮湿', '强风', '合适'],
        ['阴天', '炎热', '适宜', '轻风', '合适'],
        ['雨天', '适宜', '潮湿', '强风', '不宜']
      ],

      featureName: ['天气', '温度', '湿度', '风速', '打羽毛球'],

      ID3_tree_mermaid_code: `
        graph TD
        Root([Root]) --> node0
        node0([湿度_适宜])
        node1([天气_阴天])
        node2["不宜"]
        node3["合适"]
        node1 -->|是| node2
        node1 -->|否| node3
        node4([风速_强风])
        node5["合适"]
        node6["不宜"]
        node4 -->|是| node5
        node4 -->|否| node6
        node0 -->|是| node1
        node0 -->|否| node4
      `,
    }
  },
  methods: {
    refresh_component() {
      this.componentKey += 1;
    },
    get_decision_tree_ID3_result() {
      this.request.post('/alg/decision_tree_id3', {
        inputData: this.inputData,
        featureName: this.featureName
      }).then((res) => {
        this.ID3_tree_mermaid_code = res.data.ID3_tree_mermaid_code;
        this.$message.success('计算完成');
        this.refresh_component();
      }).catch((error) => {
        this.$message.error(error.response.data.message);
      })
    },
  }
}
</script>
