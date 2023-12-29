<script>
import ImageUploader from './components/ImageUploader.vue';

export default {
  components: {
    ImageUploader
  }
};
</script>

<template>
  <div class="container">
    <div class="header">
      <div class="header__image">
        <img src="./assets/logo_transp.png" alt="Stardist logo" style="max-height: 100px; max-width: 100px;">
      </div>
      <div class="header__text">
        <div class="header__text--title">
          Stardist
        </div>
        <div class="header__text--content">
          Segmentation and particular counting with diamond or bubble
        </div>
      </div>
    </div>
    <div class="main">
      <image-uploader></image-uploader>
    </div>
  </div>
</template>

<style>
html {
  height: 100%;
}
body {
  margin: 0;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  position: relative;
}
.container {
  min-width: 100%;
  min-height: 100vh;
  background-color: black;
  display: flex;
  flex-direction: column;
}
.header {
  padding: 20px;
  display: flex;
  border-bottom: 2px solid lightgreen;
}
.header__text {
  color: #fff;
  margin-left: 30px;
  display: flex;
  flex-direction: column;
}
.header__text--title {
  font-size: 28px;
  font-weight: 700;
  color: lightgreen;
}
.header__text--content{
  margin-top: 10px;
  font-size: 20px;
  font-weight: 500;
}
.main {
  padding-left: 50px;
}
</style>

