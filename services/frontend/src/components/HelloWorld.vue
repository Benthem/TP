<template>
<div>
  <table>
          <tr v-for="(row, id) in msg" :key="id">
              <td>{{ row['color'] }}</td>
              <td>{{ row['sum'] }}</td>
          </tr>
  </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      axios.get('/')
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
      console.log()
    },
  },
  created() {
    this.getMessage();
  },
};
</script>