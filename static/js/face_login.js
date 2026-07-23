const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const status = document.getElementById("status");

document.getElementById("startCamera").onclick = async () => {

    const stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });

    video.srcObject = stream;

    status.innerHTML = "Camera Started";

};

document.getElementById("faceLogin").onclick = async () => {

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video, 0, 0);

    const image = canvas.toDataURL("image/jpeg");

    const response = await fetch("/face-login-api/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            image: image
        })

    });

    const result = await response.json();

    if (result.status === "success") {

        alert(result.message);

        window.location.href = "/";

    }
    else {

        alert(result.message);

    }

};