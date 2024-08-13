<template>
  <div class="container">
    <pre class="mermaid">{{ chart }}</pre>
  </div>
</template>

<script>
import { defineComponent, onMounted, watch } from 'vue';
import mermaid from 'mermaid';

export default defineComponent({
  name: 'MermaidCo',
  props: {
    chart: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const initializeMermaid = () => {
      mermaid.initialize({ startOnLoad: true });
      mermaid.init();
    };

    onMounted(() => {
      initializeMermaid();
    });

    watch(() => props.chart, () => {
      initializeMermaid();
    });

    return {
      ret_chart: props.chart
    };
  }
});
</script>
