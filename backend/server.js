const express = require("express");
const cors = require("cors");
const path = require("path");
const { spawn } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

const ROOT = path.join(__dirname, "..");

const python = process.platform === "win32"
    ? path.join(ROOT, "ai_engine", "venv", "Scripts", "python.exe")
    : path.join(ROOT, "ai_engine", "venv", "bin", "python");

const ragScript = path.join(
    ROOT,
    "ai_engine",
    "rag.py"
);


// ---------------------------------------------
// Basic routes
// ---------------------------------------------

app.get("/", (req, res) => {
    res.json({
        message: "Rulebook AI backend is running"
    });
});

app.get("/health", (req, res) => {
    res.json({
        status: "ok"
    });
});


// ---------------------------------------------
// Ask Rulebook
// ---------------------------------------------

app.post("/api/ask", (req, res) => {

    const { question } = req.body;

    if (!question || !question.trim()) {
        return res.status(400).json({
            error: "Question is required"
        });
    }

    console.log("\nQuestion:", question);

    const process = spawn(
        python,
        [ragScript, "--question", question],
        {
            cwd: ROOT
        }
    );

    let output = "";
    let errorOutput = "";

    // Python stdout
    process.stdout.on("data", (data) => {
        output += data.toString();
    });

    // Python stderr
    process.stderr.on("data", (data) => {
        errorOutput += data.toString();

        console.log(
            "Python:",
            data.toString().trim()
        );
    });

    process.on("close", (code) => {

        console.log("Python process exited:", code);

        if (code !== 0) {

            console.error(errorOutput);

            return res.status(500).json({
                error: "RAG engine failed",
                details: errorOutput
            });
        }

        try {

            const result = JSON.parse(output);

            res.json(result);

        } catch (error) {

            console.error(
                "Invalid Python output:",
                output
            );

            res.status(500).json({
                error: "Invalid response from RAG engine"
            });
        }
    });

    process.on("error", (error) => {

        console.error(
            "Failed to start Python:",
            error
        );

        res.status(500).json({
            error: "Could not start RAG engine",
            details: error.message
        });
    });
});


app.listen(5000, () => {

    console.log(
        "Server running on http://localhost:5000"
    );

});