document.getElementById("scanBtn").addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
    if (tab.url) {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: tab.url })
      });
  
      const data = await response.json();
      document.getElementById("result").textContent = `Rezultat: ${data.predicted_class}`;
    }
  });
  