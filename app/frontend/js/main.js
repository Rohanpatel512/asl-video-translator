const video = document.getElementById("video");
const startBtn = document.getElementById("startBtn");
const recordBtn = document.getElementById("recordBtn");

let stream;
let mediaRecorder;
let recordedChunks = [];

startBtn.addEventListener("click", async () => {
    stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
    });

    video.srcObject = stream;

    recordBtn.classList.add("active");
    recordBtn.disabled = false;

});

recordBtn.addEventListener("click", () => {
    if (!stream) return;

    if (recordBtn.textContent === "Start Recording") {
        recordedChunks = [];

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                recordedChunks.push(e.data);
            }
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: "video/webm" });
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "hand-sign-recording.webm";
            a.click();
        };

        mediaRecorder.start();
        recordBtn.textContent = "Stop Recording";

    } else {
        mediaRecorder.stop();
        recordBtn.textContent = "Start Recording";
    }
});