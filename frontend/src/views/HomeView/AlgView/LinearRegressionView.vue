<template>
  <div style="display: flex">
    <div style="width: 340px">
      <span style="color: rgba(42,53,191,0.89)">数据：</span>
      <el-table :data="inputData" style="width: 340px; margin-top: 20px" border stripe fit show-header size="small">
        <el-table-column prop="0" label="X" width="170px">
          <template v-slot="scope">
            <el-input-number precision="1" v-model="inputData[scope.$index][0]" controls-position="right" />
          </template>
        </el-table-column>
        <el-table-column prop="1" label="Y" width="170px">
          <template v-slot="scope">
            <el-input-number precision="1" v-model="inputData[scope.$index][1]" controls-position="right" />
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="margin-left: 30px; width: 800px">
      <el-button type="primary" @click="get_linear_regression_result">计算</el-button>
      <div style="margin-top: 20px">
        <canvas id="InputChart" width="100" height="60"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto';

export default {
  name: 'LinearRegressionView',
  data() {
    return {
      inputData: [[1, 2], [2, 3], [3, 5], [4, 7], [5, 11], [6, 12], [7, 15], [8, 14], [9, 20], [10, 24], [11, 22], [12, 27]],
      predictData: null,
    }
  },
  mounted() {
    this.LinearRegressionChart();
  },
  methods: {
    LinearRegressionChart() {
      const ctx = document.getElementById('InputChart').getContext('2d');
      if (this.inputChartInstance) {
        this.inputChartInstance.destroy();
      }
      this.inputChartInstance = new Chart(ctx, {
        data: {
          datasets: [
            {
              type: 'scatter',
              label: '输入数据',
              data: this.inputData, // 使用你的输入数据
              backgroundColor: 'rgba(75, 192, 192, 0.4)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              pointRadius: 5,
              pointBackgroundColor: 'rgba(75, 192, 192, 1)',
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: 'rgba(75, 192, 192, 1)',
            },
            {
              type: 'line',
              label: '预测数据',
              data: this.predictData, // 使用你的预测数据
              backgroundColor: 'rgba(255, 99, 132, 0.4)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1,
              pointRadius: 5,
              pointBackgroundColor: 'rgba(255, 99, 132, 1)',
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: '线性回归'
            }
          }
        },
      });
    },
    get_linear_regression_result() {
      this.request.post('/alg/linear_regression', {
        inputData: this.inputData,
      }).then((res) => {
        this.predictData = res.data.predictData;
        this.$message.success('计算完成');
        this.LinearRegressionChart()
      }).catch((error) => {
        this.$message.error(error.response.data.message);
      })
    },
  }

}

</script>