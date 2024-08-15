<template>
  <div style="display: flex">
    <div style="width: 450px">
      <span style="color: rgba(42,53,191,0.89)">数据：</span>
      <el-table :data="inputData" style="width: 450px; margin-top: 20px" border stripe fit show-header size="small">
        <el-table-column prop="0" label="天气" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][0]" placeholder="请选择">
              <el-option label="晴天" value="Sunny"></el-option>
              <el-option label="雨天" value="Rain"></el-option>
              <el-option label="阴天" value="Overcast"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="1" label="温度" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][1]" placeholder="请选择">
              <el-option label="炎热" value="Hot"></el-option>
              <el-option label="适宜" value="Mild"></el-option>
              <el-option label="寒冷" value="Cool"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="2" label="湿度" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][2]" placeholder="请选择">
              <el-option label="潮湿" value="High"></el-option>
              <el-option label="适宜" value="Normal"></el-option>
              <el-option label="干燥" value="Low"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="3" label="风速" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][3]" placeholder="请选择">
              <el-option label="强风" value="Strong"></el-option>
              <el-option label="轻风" value="Weak"></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="4" label="打羽毛球" width="90px">
          <template v-slot="scope">
            <el-select v-model="inputData[scope.$index][4]" placeholder="请选择">
              <el-option label="合适" value="Yes"></el-option>
              <el-option label="不宜" value="No"></el-option>
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
        ['Sunny', 'Hot', 'High', 'Weak', 'No'],
        ['Sunny', 'Hot', 'High', 'Strong', 'No'],
        ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
        ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Cool', 'Normal', 'Strong', 'No'],
        ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],
        ['Sunny', 'Mild', 'High', 'Weak', 'No'],
        ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'],
        ['Sunny', 'Mild', 'Normal', 'Strong', 'Yes'],
        ['Overcast', 'Mild', 'High', 'Strong', 'Yes'],
        ['Overcast', 'Hot', 'Normal', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'High', 'Strong', 'No']
      ],

      featureName: ['Outlook', 'Temperature', 'Humidity', 'Wind', 'PlayTennis'],

      ID3_tree_mermaid_code: `
        graph TD
        node0{Humidity_Normal <= 0.50}
        node1{Outlook_Overcast <= 0.50}
        node2["No"]
        node3["Yes"]
        node1 -->|True| node2
        node1 -->|False| node3
        node4{Wind_Strong <= 0.50}
        node5["Yes"]
        node6["No"]
        node4 -->|True| node5
        node4 -->|False| node6
        node0 -->|True| node1
        node0 -->|False| node4
      `,
    }
  },
  methods: {
    refresh_component(){
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
