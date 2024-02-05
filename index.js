const {spawn} = require("child_process")
const pythonCode = spawn("python", ["app.py", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Basketball.png/220px-Basketball.png"])
pythonCode.stdout.on("data", (data) => {
    console.log(data.toString())
})

pythonCode.on("close", (code) => {
    console.log(code)
})

