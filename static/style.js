let token = "";

// 🔐 REGISTER
function register() {
    fetch("/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("auth-status").innerText = data.msg;
    });
}

// 🔐 LOGIN
function login() {
    fetch("/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        token = data.access_token;
        document.getElementById("auth-status").innerText = "Logged in!";
        loadFiles();
    });
}

// 📤 UPLOAD FILE
function uploadFile() {
    let file = document.getElementById("fileInput").files[0];
    let formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.msg);
        loadFiles();
    });
}

// 📥 DOWNLOAD FILE
function downloadFile(filename) {
    fetch(`/download/${filename}`, {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.blob())
    .then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = filename;
        a.click();
    });
}

// 📂 LOAD FILE LIST (YOU NEED BACKEND ROUTE)
function loadFiles() {
    fetch("/files", {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("fileList");
        list.innerHTML = "";

        data.files.forEach(file => {
            let li = document.createElement("li");
            li.innerHTML = `${file} 
                <button onclick="downloadFile('${file}')">Download</button>`;
            list.appendChild(li);
        });
    });
}
let dropZone = document.getElementById("dropZone");

dropZone.ondragover = (e) => {
    e.preventDefault();
};

dropZone.ondrop = (e) => {
    e.preventDefault();
    let file = e.dataTransfer.files[0];
    uploadFileDirect(file);
};

function uploadFileDirect(file) {
    let formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => alert("Uploaded with hash: " + data.hash));
}
const socket = io();

// 🔴 LIVE ACTIVITY
socket.on('activity', (data) => {
    let logs = document.getElementById("logs");
    logs.innerHTML += `
    [${data.user}] ${data.action} → ${data.file} 
    Hash: ${data.hash}\n`;
});

// ⚠️ ALERTS
socket.on('alert', (data) => {
    alert(data.msg);
});
function loadStats() {
    fetch("/stats")
    .then(res => res.json())
    .then(data => {
        document.getElementById("logs").innerHTML += 
        "\nTotal Uploads: " + data.uploads;
    });
}