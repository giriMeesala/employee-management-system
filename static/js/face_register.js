const video = document.getElementById("video");
const canvas = document.getElementById("canvas");

document
.getElementById("startCamera")
.onclick = async () => {

    const stream =
    await navigator.mediaDevices.getUserMedia({

        video:true

    });

    video.srcObject = stream;

};

document
.getElementById("capture")
.onclick = async () => {

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(
        video,
        0,
        0
    );

    const image =
    canvas.toDataURL("image/jpeg");

    const response =
    await fetch("/receive-frame/",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            image:image
        })

    });

    const result =
    await response.json();

    alert(result.message);

};