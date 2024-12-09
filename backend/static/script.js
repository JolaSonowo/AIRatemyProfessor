const API_URL = "http://127.0.0.1:5000";

async function addRating() {
    const professorName = document.getElementById("professor-name").value;
    const subjectName = document.getElementById("subject-name").value;
    const score = parseFloat(document.getElementById("score").value);

    const response = await fetch(`${API_URL}/add_professor_score`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ professor_name: professorName, subject_name: subjectName, score })
    });

    const result = await response.json();
    alert(result.message || result.error);
}

async function getScores() {
    const professorName = document.getElementById("search-professor-name").value;

    const response = await fetch(`${API_URL}/get_professor_scores/${professorName}`);
    const result = await response.json();

    if (result.error) {
        alert(result.error);
    } else {
        document.getElementById("result").textContent = JSON.stringify(result, null, 2);
    }
}
