<template>
    <div class="upload">
        <div v-if="!model.image" class="upload-box" @click="openFileSelector" :class="notAllowed && 'not-allowed'">
            <spinner v-if="showSpinner"></spinner>
            <input ref="fileInput" type="file" @change="uploadImage" accept="image/*" style="display: none;" :disabled="notAllowed">
            <div class="upload__message">
                <span>Click to upload file</span>
            </div> 
        </div>
        <span v-if="!model.image" class="caution">Please upload image with jpg, png or tif format and less than 10mb</span>
        <div v-if="!model.image" class="sample">
            <span>SAMPLE IMAGES</span>
            <div class="sample__box">
                <div class="sample__item--diamond">
                    <div class="sample__img">
                        <img style="max-width: 400px; max-height: 400px;" src="../assets/sample/diamond/0.jpg" alt="">
                    </div>
                    <div class="diamond__small">
                        <div class="sample__img">
                            <img style="max-width: 400px; max-height: 200px;" src="../assets/sample/diamond/1.jpg" alt="">
                        </div>
                        <div class="sample__img">
                            <img style="max-width: 400px; max-height: 200px;" src="../assets/sample/diamond/2.jpg" alt="">
                        </div>
                    </div>
                </div>
                <div class="sample__item--bubble">
                    <div class="sample__img">
                        <img style="max-width: 400px; max-height: 400px;" src="../assets/sample/bubble/1.png" alt="">
                    </div>
                    <div class="sample__img">
                        <img style="max-width: 400px; max-height: 400px;" src="../assets/sample/bubble/0.png" alt="">
                    </div>
                </div>
            </div>
            
        </div>
        <div class="link-back">
            <span v-if="model.image" @click="this.model.image = null, this.model.imageRes = null">Try new image</span>
        </div>
        <div v-if="model.image" class="option-box">
            <div class="select-box">
                <label for="modelOption">Select type of model:</label>
                <select id="modelOption" v-model="model.type">
                    <option value="diamond" selected>Diamond</option>
                    <option value="bubble">Bubble</option>
                    <option value="2D_versatile_fluo">2D_versatile_fluo</option>
                </select>
            </div>
            <div class="select-box">
                <label for="modelOption">Select color map:</label>
                <select id="modelOption" v-model="model.colorMap">
                    <option value="plasma" selected>Plasma</option>
                    <option value="jet">Jet</option>
                    <option value="viridis">Viridis</option>
                    <option value="random_label_cmap">Random Label</option>
                </select>
            </div>
        </div>
        <div class="tool-bar">
            <div class="btn" @click="handleSegmentation" v-if="model.image" :class="notAllowed && 'not-allowed'">
                <spinner v-if="showSpinner" size="small" colorProp="grey"></spinner>
                <div class="btn-content" v-if="!showSpinner">
                    Submit
                </div>
            </div>
            <div class="tool" v-if="model.imageRes">
                Duration: {{ this.model.duration }} ms
            </div>
            <div class="tool result" v-if="model.imageRes">
                Objects Counted: {{ this.model.objectsCount }}
            </div>
            <div class="tool" v-if="model.imageRes" @click="downloadImage">
                <span>Download predicted</span>
            </div>
        </div>
        <div class="image-container"> 
            <Image v-if="model.image" title="Original Image" :source="model.image" alt="Uploaded Image"></Image>
            <ImageRes v-if="model.imageRes" 
                title="Predicted Image" 
                :source="model.imageRes" 
                alt="Predicted Image"
                :points="model.points"
                :coordArray="model.coord"
                :strokeLine="model.strokeLine"
                >
            </ImageRes>
        </div> 
    </div>
</template>

<script>
import axios from 'axios';
import Spinner from './Spinner.vue'
import Image from './Image.vue';
import ImageRes from './ImageRes.vue';
export default {
    components: {
        Spinner, Image, ImageRes
    },
    data() {
        return {
            panArr: [],
            panzoom: [],
            showSpinner: false,
            notAllowed : false,
            fileUpload: null,
            model: {
                type: "diamond",
                colorMap: "plasma",
                image: null,
                imageRes: null,
                duration: 0,
                objectsCount: 0,
                points:[],
                coord: [],
                strokeLine: '#000000',
            }
        };
    },
    methods: {
        openFileSelector() {
            this.$refs.fileInput.click();
        },
        async uploadImage(event) {
            this.showSpinner = true;
            this.notAllowed = true;
            const file = event.target.files[0];
            if (file) { 
                this.fileUpload = file;
                if (file.name.toLowerCase().includes("tiff") || file.name.toLowerCase().includes("tif")) {
                    const formData = new FormData();
                    formData.append('tiff_file', file);

                    try {
                        const response = await axios.post('http://127.0.0.1:5005/convert', formData, {
                            headers: {
                            'Content-Type': 'multipart/form-data'
                            },
                            responseType: 'arraybuffer'  // Set response type to arraybuffer to handle binary data
                        });

                        // Create a Blob from the array buffer received
                        const blob = new Blob([response.data], { type: 'image/png' });

                        // Create a URL for the Blob and set it as the image source
                        this.model.image = URL.createObjectURL(blob);
                    } catch (error) {
                        alert('Error uploading and converting the image, please try again')
                        console.error('Error uploading and converting the image', error);
                    }
                } else {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => {
                        this.model.image = reader.result;
                    };
                } 
            }
            this.showSpinner = false;
            this.notAllowed = false;
        },

        async handleSegmentation(){
            if (this.fileUpload != null && !this.notAllowed) {
                const formData = new FormData();
                formData.append('image', this.fileUpload);
                formData.append('type', this.model.type);
                formData.append('colorMap', this.model.colorMap);
                if (this.model.colorMap == 'random_label_cmap') {
                    this.model.strokeLine = '#FF0000';
                } else {
                    this.model.strokeLine = '#000000';
                }
                this.showSpinner = true;
                this.notAllowed = true;
                try {
                    var startTime = performance.now()
                    const response = await axios.post('http://127.0.0.1:5005/segmentation', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        },
                    });

                    this.model.imageRes = 'data:image/png;base64,' + response.data.imageBytes;
                    this.model.objectsCount = response.data.objectsCount; 
                    this.model.points = response.data.points;
                    this.model.coord = response.data.coord;
                    console.log(response.data);
                    this.model.duration = (performance.now() - startTime).toFixed(2);
                } catch (error) {
                    alert('An error occur when segmenting the image, please try again!')
                    console.error('Error uploading and converting the image', error);
                }
                this.showSpinner = false;
                this.notAllowed = false;
            }
        },

        downloadImage() {
            // Create an anchor element
            const link = document.createElement('a');

            // Set the anchor's href to the image URL
            link.href = this.model.imageRes;

            // Set the anchor's download attribute with the desired filename
            link.download = 'mask.png'; // Change the filename as needed

            // Trigger a click event on the anchor to initiate the download
            link.click();
        },
    }
};
</script>

<style scoped>
.link-back {
    margin-top: 50px;
    margin-left: 50px;
}
.link-back span {
    font-size: 20px;
    color: lightgreen;
    text-decoration: underline;
    cursor: pointer;
}
.link-back span:hover {
    color: darkgreen;
}
.upload-box {
    margin-top: 50px;
    position: absolute;
    width: 400px;
    height: 150px;
    color: #fff;
    border: 5px dashed lightgreen;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #282828;
    cursor: pointer;
}
.upload__message {
    font-size: 20px;
}
.not-allowed {
    cursor: not-allowed !important;
}

.option-box {
    display: flex;
    flex-direction: column;
    row-gap: 10px;
    margin-top: 10px;
    margin-left: 50px;
}
.select-box {
    color: #fff;
    font-size: 20px;
}
.select-box #modelOption {
    margin-left: 10px;
    font-size: 20px;
}

.image-container {
    display: flex;
    margin-right: 200px;
    margin-top: 50px;
    margin-left: 50px;
    column-gap: 100px;
}

@media only screen and (max-width: 900px) {
    .image-container {
        flex-direction: column;
        row-gap: 0px;
    }
}
.btn {
    position: relative;
    width: 100px;
    height: 50px;
    color: #000;
    background-color: lightgreen;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-left: 50px;
    margin-top: 20px;
}
.btn:hover {
    background-color: greenyellow;
}
.btn-content {
    font-size: 20px;
}

.tool-bar {
    display: flex;
    align-items: center;
    column-gap: 50px;
}
.tool {
    color: #fff;
    font-size: 20px;
    margin-top: 20px;
}
.tool span {
    color: lightgreen;
    text-decoration: underline;
    cursor: pointer;
}
.result {
    color: lightgreen;
}
.sample{
    position: absolute;
    top: 200px;
    left: 700px;
    color: #fff;
}
.sample span {
    font-size: 20px;
    font-weight: 500;
    color: lightgreen;
    font-style: italic;
}
.sample__box{
    margin-top: 20px;
    display: flex;
    column-gap: 30px;
}
.diamond__small{
    display: flex;
    column-gap:  5px;
}
.sample__item--bubble {
    display: flex;
    flex-direction: column;
    row-gap: 30px;
}
.caution {
    position: absolute;
    top: 450px;
    color: #fff;
    font-size: 16px;
}
</style>
