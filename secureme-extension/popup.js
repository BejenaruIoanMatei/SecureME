document.getElementById("scanButton").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;

  try {
    const response = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url })
    });

    if (!response.ok) throw new Error("Server error");

    const data = await response.json();
    document.getElementById("result").innerText = `Result: ${data.predicted_class}`;
  } catch (err) {
    document.getElementById("result").innerText = `Error: ${err.message}`;
  }
});
