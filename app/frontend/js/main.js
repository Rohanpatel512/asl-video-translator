const video = document.getElementById("video");
const startBtn = document.getElementById("startBtn");
const recordBtn = document.getElementById("recordBtn");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
const translationText = document.getElementById("translation-text");
const clearBtn = document.getElementById("clear-btn");

let stream;
let mediaRecorder;
let signIntervals = []
let committedPrediction = null;
let candidatePrediction = null;
let candidateStartTime = null;
let lastTimeCommit = null;
let isProcessingFrames = true;

const CANDIDATE_STABILITY_MS = 200;

const API_BASED_URL = window.APP_CONFIG?.API_BASE_URL ?? "";

window.addEventListener("beforeunload", () => {
    console.log("Page unloading — stopping frame processing.");
    isProcessingFrames = false;
    if (video.srcObject) {
        const tracks = video.srcObject.getTracks();
        tracks.forEach(track => track.stop());
    }
});

async function startCamera() {

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false,
        });

        video.srcObject = stream;

        return new Promise((resolve) => {
            video.onloadedmetadata = () => {
                video.play();
                resolve();
            };
        })

    } catch (error) {
        console.error("Error accessing camera:", error);
    }

}

clearBtn.addEventListener("click", () => {
    translationText.innerHTML = "";
})


function captureFrame() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    return canvas;

}

async function initFrameProcessing() {
    
    while(isProcessingFrames) {
        const frame = captureFrame();

        if(!frame || frame.width == 0 || frame.height == 0) {
            console.error("Invalid frame captured!");
            await new Promise(resolve => setTimeout(resolve, 100));
            continue;
        }

        const blob = await new Promise(resolve => {
            frame.toBlob(resolve, "image/jpeg");
        });

        if(!blob) {
            console.warn("Skipping frame: toBlob returned null");
            await new Promise(resolve => setTimeout(resolve, 100));
            continue;
        }

        const formData = new FormData();
        formData.append("frame", blob, "frame.jpg");
        
        try {
            const start = performance.now();
            const response = await fetch(`${API_BASED_URL}/translate/translation/predict`, {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const data = await response.json();
            
            processPrediction(data);
                    

        } catch (error) {
            console.error("Error sending frame for translation:", error);
        }

        await new Promise(resolve => setTimeout(resolve, 100));
        
    }
}

// Fire everything off sequentially 
async function main() {
    await startCamera();
    initFrameProcessing();
}

function processPrediction(data) {
    
    if(!data || !data.hand_detected) {
        candidatePrediction = null;
        candidateStartTime = null;
        committedPrediction = null;
        return;
    }

    if(!data.letter) {
        candidatePrediction = null;
        candidateStartTime = null;
        return;
    }

    const letter = data.letter.trim().toLowerCase(); 

    if(letter === "nothing" || letter === committedPrediction) {
        candidatePrediction = null;
        candidateStartTime = null;
        return;
    }

    if(letter !== candidatePrediction) {
        candidatePrediction = letter;
        candidateStartTime = performance.now();
        return;
    }

    if(performance.now() - candidateStartTime >= CANDIDATE_STABILITY_MS) {
        
        commitPrediction(letter);
        committedPrediction = letter;
        candidatePrediction = null;
        candidateStartTime = null;
    }
}

function commitPrediction(letter) {

    /*let commitTime = performance.now()*/

    if(letter != null) {
        letter = letter.trim().toLowerCase();
        if(letter == "space") {
            document.getElementById("translation-text").innerHTML += " "
            displayNonTextSignal("Space");

        } else if(letter == "del") {
            let currentText = document.getElementById("translation-text").innerHTML;
            if(currentText.length == 0) {
                return;
            }
            document.getElementById("translation-text").innerHTML = currentText.slice(0, -1);
        } else if(letter == "nothing") {
            return;
        } else {
            document.getElementById("translation-text").innerHTML += letter
        }
    }
}

function displayNonTextSignal(signal) {
    const nonTextSignalDiv = document.getElementById("non-text-signal");

    nonTextSignalDiv.innerHTML = signal;

    nonTextSignalDiv.classList.add("show");

    setTimeout(() => {
        nonTextSignalDiv.classList.remove("show");
    }, 1000);
}

main();
