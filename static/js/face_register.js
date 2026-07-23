const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const status = document.getElementById("status");

let registrationRunning = false;
let totalFrames = 0;

const MAX_FRAMES = 30;



// Start Camera
document.getElementById("startCamera").onclick = async () => {

    const stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });

    video.srcObject = stream;

    status.innerHTML = "Camera Started";

};



// Register Face
document.getElementById("registerFace").onclick = async () => {

    if (!video.srcObject) {

        alert("Please start the camera first.");

        return;

    }

    registrationRunning = true;

    totalFrames = 0;

    status.innerHTML = "Collecting face samples...";

    captureFrames();

};



// Automatically capture frames
async function captureFrames() {

    if (!registrationRunning)
        return;

    if (totalFrames >= MAX_FRAMES) {

        registrationRunning = false;

        status.innerHTML = "Face registration completed.";

        alert("Registration Completed");

        return;

    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video, 0, 0);

    const image = canvas.toDataURL("image/jpeg");

    const response = await fetch("/receive-frame/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            image: image
        })

    });

    const result = await response.json();

    console.log(result);

    totalFrames++;

    status.innerHTML =
        `Collecting Samples ${totalFrames}/${MAX_FRAMES}`;

    setTimeout(captureFrames, 200);

}